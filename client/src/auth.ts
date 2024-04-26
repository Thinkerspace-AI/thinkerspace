import { SvelteKitAuth } from "@auth/sveltekit";
import GitHub from "@auth/sveltekit/providers/github";
import { GITHUB_ID, GITHUB_SECRET } from "$env/static/private";

export const { handle, signIn, signOut } = SvelteKitAuth({
  providers: [GitHub({
    clientId: GITHUB_ID,
    clientSecret: GITHUB_SECRET
  })]
});