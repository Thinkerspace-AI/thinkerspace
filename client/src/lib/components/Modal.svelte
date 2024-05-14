<script>
    let shown = false;
    export function open(){
        shown = true;
    }
    export function close() {
        shown = false;
    }
</script>

{#if shown}
    <div class="backdrop-blur bg-gray-950 bg-opacity-25 fixed t-0 l-0 w-full h-full flex items-center">
        <div class="bg-white max-w-50 mx-auto p-10 flex flex-col items-center rounded-3xl">
            <slot />
        </div>
    </div>
{/if}
