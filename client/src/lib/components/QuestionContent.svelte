<!-- unused in this version -->

<script lang="ts">
  export let question = "";
  export let description = "";
  export let next: () => void;
  export let previous: () => void;

  let inputElement: HTMLInputElement;
  let buttonElement: HTMLButtonElement;

  function keydown(e: KeyboardEvent) {
    if (e.key === "Enter") {
      next();
      return;
    }

    if (e.target === buttonElement && e.key === "Tab") {
      e.preventDefault();
      inputElement.focus();
    }
  }
</script>

<h1>{question}</h1>
<h6>{description}</h6>

<input
  type="text"
  on:keydown={keydown}
  bind:this={inputElement}
  placeholder="Type here..."
/>

<button on:keydown={keydown} on:click={next} bind:this={buttonElement}
  >Next</button
>

{#if question != "What problem are you trying to solve?"}
  <button on:keydown={keydown} on:click={previous} bind:this={buttonElement}
    >Previous</button
  >
{/if}

<style>
  input {
    width: 100%;
    padding: 24px;
    margin-top: 24px;
    resize: none;

    border: none;
    box-shadow: 0 0 24px rgba(0, 0, 0, 0.1);

    /* overflow: auto;      Need to convert into textarea */
  }

  input:focus {
    outline: none;
    scale: 1.02;
  }

  button {
    background: var(--white);
    padding: 12px 24px;

    float: right;
    margin-top: 24px;

    border: none;
    border-radius: 24px;
  }

  button:hover,
  button:focus {
    scale: 1.1;
    background: var(--gray);

    outline: none;
  }

  button:active {
    scale: 1.1;
  }
</style>
