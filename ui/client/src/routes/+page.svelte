<script lang="ts">
    import dark_logo from "$lib/assets/Thinkerspace_logo_dark.png";

    import { goto } from '$app/navigation';

    let username: String;
    let password: String;

    function verify() {
        if(username && password){
            goto('/session-select');
        }
    }

</script>

<div class="flex flex-col items-center justify-center overflow-hidden h-screen max-h-screen">
    <img class="h-36 w-fit mb-20" src={dark_logo} alt="logo" />
    <div class="w-fit pb-2 flex flex-col items-center justify-center ">
        <div>
            <h1 class="font-bold font-inter text-xl pb-1">Email</h1>
            <input placeholder="Type here..." bind:value={username} class="h-8 w-56 resize-none text-justify p-1 mb-1 overflow-hidden" tabindex="-1">
        </div>
        <div>
            <h1 class="font-bold font-inter text-xl pb-1">Password</h1>
            <input type="password" placeholder="Type here..." bind:value={password} class="h-8 w-56 resize-none text-justify p-1 overflow-hidden" tabindex="-1">
        </div>

        <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-1 px-3 mt-4 rounded-full w-fit" tabindex="-1" on:click={verify}>
            Sign In
        </button>
    </div>
</div>