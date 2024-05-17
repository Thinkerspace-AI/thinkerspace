<script lang="ts">
    import dark_logo from "$lib/assets/Thinkerspace_logo_dark.png";
  
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";

    async function goToLogIn() {
        goto("/login");
    }
  
    console.log("Page Data:", $page.data);
  </script>

<div class="flex flex-col items-center justify-center overflow-hidden h-screen max-h-screen">
    <img class="h-32 w-fit mb-4" src={dark_logo} alt="logo" />
    <h1 class="mt-2 font-inter font-bold text-3xl">Where ideas take flight</h1>
    {#if !$page.data.session}
        <button class="mt-24 bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-md font-inter py-2 px-12 rounded-full w-fit" on:click={goToLogIn}>Log In</button>
    {/if}
</div>
  