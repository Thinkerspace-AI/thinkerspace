<script lang="ts">
    import { goto } from '$app/navigation';

    async function openSession(){
        goto('/session/000000');
    }
</script>


<div class="flex flex-col overflow-hidden h-screen max-h-screen">
    <div class="m-auto w-fit h-fit flex flex-none flex-col items-center justify-center overflow-y-scroll">
        <div class="mr-8">
            <div class="flex flex-row items-center justify-center mb-3">
                <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
                    <h1 class="font-bold font-inter text-2xl pb-1 pl-1">Session #000001</h1>
                    <h6 class="">[----- Latest prompt submitted -----]</h6>
                </div>
                <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit" tabindex="-1" on:click={openSession}>
                    Open
                </button>
            </div>
            <div class="flex flex-row items-center justify-center mb-3">
                <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
                    <h1 class="font-bold font-inter text-2xl pb-1 pl-1">Session #000002</h1>
                    <h6 class="">[----- Latest prompt submitted -----]</h6>
                </div>
                <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit" tabindex="-1" on:click={openSession}>
                    Open
                </button>
            </div>
            <div class="flex flex-row items-center justify-center mb-3">
                <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
                    <h1 class="font-bold font-inter text-2xl pb-1 pl-1">Session #000003</h1>
                    <h6 class="">[----- Latest prompt submitted -----]</h6>
                </div>
                <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit" tabindex="-1" on:click={openSession}>
                    Open
                </button>
            </div>
            <div class="flex flex-row items-center justify-center mb-3">
                <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
                    <h1 class="font-bold font-inter text-2xl pb-1 pl-1">Session #000004</h1>
                    <h6 class="">[----- Latest prompt submitted -----]</h6>
                </div>
                <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit" tabindex="-1" on:click={openSession}>
                    Open
                </button>
            </div>
            <div class="flex flex-row items-center justify-center mb-3">
                <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
                    <h1 class="font-bold font-inter text-2xl pb-1 pl-1">Session #000005</h1>
                    <h6 class="">[----- Latest prompt submitted -----]</h6>
                </div>
                <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit" tabindex="-1" on:click={openSession}>
                    Open
                </button>
            </div>
            <div class="flex flex-row items-center justify-center mb-3">
                <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
                    <h1 class="font-bold font-inter text-2xl pb-1 pl-1">Session #000006</h1>
                    <h6 class="">[----- Latest prompt submitted -----]</h6>
                </div>
                <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit" tabindex="-1" on:click={openSession}>
                    Open
                </button>
            </div>
        </div>
    </div>
</div>

