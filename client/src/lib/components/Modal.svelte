<script>
    let shown = false;
    export function open() {
        shown = true;
    }
    export function close() {
        shown = false;
    }
</script>

<style>
    .modal-wrapper {
        background-color: rgb(0, 0, 0, 0.8);
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
    }

    .modal {
        background-color: #fcc454;
        max-width: 65vw;
        padding: 1rem;
        margin: 15% auto;
    }
</style>

{#if shown}
    <div class="modal-wrapper">
        <div class="modal">
            <slot />
        </div>
    </div>
{/if}