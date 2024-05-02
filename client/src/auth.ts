import { SvelteKitAuth } from "@auth/sveltekit";
import GitHub from "@auth/sveltekit/providers/github";
import Google from "@auth/sveltekit/providers/google";
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
    })
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

      return session;
    }
  }
});