import { SvelteKitAuth } from "@auth/sveltekit";
import GitHub from "@auth/sveltekit/providers/github";
import Google from "@auth/sveltekit/providers/google";
import Credentials from "@auth/sveltekit/providers/credentials";
import { GITHUB_ID, GITHUB_SECRET, AUTH_GOOGLE_ID, AUTH_GOOGLE_SECRET } from "$env/static/private";

import getUuid from "uuid-by-string";

export const { handle, signIn, signOut } = SvelteKitAuth({
  providers: [
    GitHub({
      clientId: GITHUB_ID,
      clientSecret: GITHUB_SECRET
    }),
    Google({
      clientId: AUTH_GOOGLE_ID,
      clientSecret: AUTH_GOOGLE_SECRET,
    }),
    Credentials({
      credentials: {
        email: { type: 'email', label: 'Email' },
        password: { type: 'password', label: 'Password' },
      },
      authorize: async (credentials) => {
        let user = null;

        const userResponse = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: credentials.email, pw_hash: credentials.password }), // TODO: Hash password
        });

        console.log(userResponse);

        if (!userResponse.ok) {
          return null;
        }

        user = await userResponse.json();

        console.log(user);

        return user;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token;
        token.provider = account.provider;
      }

      return token;
    },
    async session({ session, token }) {
      // @ts-ignore
      session.access_token = token.accessToken;
      // @ts-ignore
      session.provider = token.provider;
      session.user.id = getUuid(token.provider + session.user.email)

      // Register User
      try {
        console.log("Attempting to register as new user");

        const res = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: session.user.email, pw_hash: session.user.id, user_id: session.user.id }),
        });

        console.log("Response: ", res);

        if (res.ok) {
          const data = await res.json();
          console.log(data);
        } else {
          console.error("Failed to register");
        }
      } catch(e) {
        console.error(e);
      }

      return session;
    }
  }
});