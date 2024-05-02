<script lang="ts">
  export let completion: [string, string];
  export let hasSave: boolean = true;
  export let save: () => void;

  $: [agent, response] = completion;

  // async function save() {
  //   console.log("Saving to history...");

  //   const saveResponse = await fetch(
  //     "https://llm-app-whtpnrbuea-as.a.run.app/save",
  //     {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         session_id: sessionId,
  //         prompt: prompt,
  //         completion: response,
  //       }),
  //     }
  //   );

  //   console.log(saveResponse);
  // }
</script>

<div class="completion">
  <h2 class="agent">{agent}</h2>
  <p class="response">{response}</p>

  {#if hasSave}
    <button on:click={save}>Save to History</button>
  {/if}
</div>

<style>
  .completion {
    margin: 1rem;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
  }

  .agent {
    font-size: 1.5rem;
  }

  .response {
    font-size: 1rem;
  }
</style>
