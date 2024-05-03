<script lang="ts">
    import "../app.css";
    import light_logo from "$lib/assets/Thinkerspace_logo_light.png";
    import Modal from "$lib/components/Modal.svelte";

    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

    let signOutModal: Modal;

    async function openSignOutModal() {
        signOutModal.open();
    }

    async function closeSignOutModal() {
        signOutModal.close();
    }

    async function confirmSignOut() {
        goto('/');
        closeSignOutModal();
    }

</script>

{#if $page.url.pathname != "/"}
    <nav class="fixed bg-Tpurple-100 w-full h-20 flex items-center justify-center">
        <img class="ml-4 mr-auto h-16 w-fit" src={light_logo} alt="logo" />
        <div class="ml-auto mr-4 w-fit">
            <ul class="flex flex-row flex-end items-center justify-center">
                {#if $page.url.pathname != "/session-creation"}
                <li class="text-Tyellow-100">
                    <a href="/session-creation" class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit">New Session</a>
                </li>
                {:else}
                <li class="text-Tyellow-100">
                    <a href="/session-creation" class="underline decoration-Tyellow-100 decoration-4 underline-offset-4 bg-Tpurple-100 hover:bg-Tyellow-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit">New Session</a>
                </li>
                {/if}
                {#if $page.url.pathname != "/session-select"}
                <li class="text-Tyellow-100">
                    <a href="/session-select" class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit">Session List</a>
                </li>
                {:else}
                <li class="text-Tyellow-100">
                    <a href="/session-select" class="underline decoration-Tyellow-100 decoration-4 underline-offset-4 bg-Tpurple-100 hover:bg-Tyellow-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit">Session List</a>
                </li>
                {/if}
                <li class="text-Tyellow-100">
                    <button class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit" on:click={openSignOutModal}>Sign Out</button>
                </li>
            </ul>
        </div>
    </nav>
{/if}

<Modal bind:this={signOutModal}>
    <h1 class="font-bold font-inter text-2xl pb-1">Do you want to log out?</h1>
    <div>
      <button class="bg-white hover:bg-Tyellow-100 text-Tpurple-100 hover:text-Tpurple-100 text-lg font-inter font-bold py-2 px-4 mr-3 rounded-full w-fit" on:click={closeSignOutModal}>Cancel</button>
      <button class="bg-Tyellow-100 hover:bg-Tpurple-100 text-Tpurple-100 hover:text-Tyellow-100 font-inter py-2 px-3 my-2 mx-1 rounded-full w-fit" on:click={confirmSignOut}>Confirm</button>
    </div>
  </Modal>

<slot />