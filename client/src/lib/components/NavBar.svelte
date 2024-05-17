<script lang="ts">
  import { signOut } from "@auth/sveltekit/client";

  import light_logo from "$lib/assets/Thinkerspace_logo_light.png";

  import Modal from "$lib/components/Modal.svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  let signOutModal: Modal;

  async function openSignOutModal() {
    signOutModal.open();
  }

  async function closeSignOutModal() {
    signOutModal.close();
  }

  async function confirmSignOut() {
    signOut();
    closeSignOutModal();
    goto("/login");
  }

  console.log("Page Data:", $page.data);
</script>

<nav class="fixed bg-Tpurple-100 w-full h-20 flex items-center justify-center">
  {#if $page.url.pathname != "/"}
  {#if $page.url.pathname != "/login"}
  <img class="ml-4 mr-auto h-16 w-fit" src={light_logo} alt="logo" />
  {/if}
  {/if}
  <div class="ml-auto mr-4 w-fit">
    <ul class="flex flex-row flex-end items-center justify-center">
      {#if $page.data.session?.user}
        {#if $page.url.pathname != "/profile"}
          <li class="text-Tyellow-100">
            <a
              href="/profile"
              class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit"
              >Profile</a
            >
          </li>
        {:else}
          <li class="text-Tyellow-100">
            <a
              href="/profile"
              class="underline decoration-Tyellow-100 decoration-4 underline-offset-4 bg-Tpurple-100 hover:bg-Tyellow-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit"
              >Profile</a
            >
          </li>
        {/if}
        <li class="text-Tyellow-100">
          <button
            class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit"
            on:click={openSignOutModal}>Sign Out</button
          >
        </li>
      {:else if $page.url.pathname != "/login"}
        <li class="text-Tyellow-100">
          <a
            href="/login"
            class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit"
            >Sign In</a
          >
        </li>
      {:else}
        <li class="text-Tyellow-100">
          <a
            href="/login"
            class="underline decoration-Tyellow-100 decoration-4 underline-offset-4 bg-Tpurple-100 hover:bg-Tyellow-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit"
            >Sign In</a
          >
        </li>
      {/if}
    </ul>
  </div>
</nav>

<Modal bind:this={signOutModal}>
  <h1 class="font-bold font-inter text-2xl pb-1">Do you want to log out?</h1>
  <div>
    <button
      class="bg-white hover:bg-Tyellow-100 text-Tpurple-100 hover:text-Tpurple-100 text-lg font-inter font-bold py-2 px-4 mr-3 rounded-full w-fit"
      on:click={closeSignOutModal}>Cancel</button
    >
    <button
      class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit"
      on:click={confirmSignOut}>Confirm</button
    >
  </div>
</Modal>
