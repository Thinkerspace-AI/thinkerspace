<script lang="ts">
  import { SignIn, SignOut } from "@auth/sveltekit/components";
  import { page } from "$app/stores";

  if ($page.data) {
    console.log("Page Data:", $page.data);
  }
</script>

{#if $page.data.session}
  <p>You are already logged in</p>
  <SignOut>
    <div slot="submitButton">Sign out</div>
  </SignOut>
{:else}
  <h1>Log In</h1>
  <SignIn>
    <div slot="submitButton">Sign in</div>
  </SignIn>
{/if}
