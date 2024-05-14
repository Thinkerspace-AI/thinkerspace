<script lang="ts">
  import { SignIn, SignOut } from "@auth/sveltekit/components";
  import { page } from "$app/stores";

  import dark_logo from "$lib/assets/Thinkerspace_logo_dark.png";

  if ($page.data) {
    console.log("Page Data:", $page.data);
  }

  let email = "";
  let password = "";

  let statusMessage: HTMLParagraphElement;

  async function register(e: Event) {
    e.preventDefault();

    console.log("Registering new user");

    const res = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, pw_hash: password }),
    });

    console.log("Response: ", res);

    if (res.ok) {
      const data = await res.json();
      console.log(data);
      statusMessage.innerText = "Successfully registered";
    } else {
      console.error("Failed to register");
      statusMessage.innerText = "Failed to register";
    }
  }
</script>

<!-- website header is set to not display for this page (+layout.svelte[26]) -->

<div class="flex flex-col items-center justify-center overflow-hidden h-screen max-h-screen">
  <img class="h-36 w-fit mb-20" src={dark_logo} alt="logo" />
  {#if $page.data.session}
    <p>You are already logged in</p>
    <p>Go to <a href="/sessions">sessions</a></p>
    <SignOut>
      <div slot="submitButton">Sign out</div>
    </SignOut>
  {:else}
    <h1>Log In</h1>
    <!-- <SignIn provider="google">
      <div slot="submitButton">Sign in with Google</div>
    </SignIn>
    <SignIn provider="github">
      <div slot="submitButton">Sign in with GitHub</div>
    </SignIn>
    <SignIn provider="credentials">
      <div slot="credentials">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required />
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required />
      </div>
      <div slot="submitButton">Sign in with email</div>
    </SignIn> -->
    <SignIn>
      <div slot="submitButton">Sign in</div>
    </SignIn>
    <h2>Register</h2>
    <form>
      <label for="email">Email</label>
      <input type="email" id="email" bind:value={email} />

      <label for="password">Password</label>
      <input type="password" id="password" bind:value={password} />

      <button type="submit" on:click={register}>Register</button>

      <p bind:this={statusMessage}></p>
    </form>
  {/if}
</div>
