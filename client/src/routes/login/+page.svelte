<script lang="ts">
  import { SignIn, SignOut } from "@auth/sveltekit/components";
  import { page } from "$app/stores";

  if ($page.data.session) {
    console.log("Session:", $page.data.session);
  }
</script>

{#if $page.data.session}
  <p>You are already logged in</p>
  <SignOut>
    <div slot="submitButton">Sign out</div>
  </SignOut>
{:else}
  <h1>Log In</h1>
  <SignIn provider="github" />
{/if}
