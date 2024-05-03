<script lang="ts">
  export let sessionId: string;
  export let prompt: string;
  export let completion: [string, string];
  export let hasSave: boolean = true;

  $: [agent, response] = completion;

  async function save() {
    console.log("Saving to history...");

    const saveResponse = await fetch(
      "https://llm-app-whtpnrbuea-as.a.run.app/save",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          prompt: prompt,
          completion: response,
        }),
      }
    );

    console.log(saveResponse);
  }
</script>

<div class="completion mx-1 mb-6 px-1 py-3 border border-Tpurple-100 flex flex-col items-center text-justify">
  <h2 class="agent font-inter bg-Tpurple-100 text-Tyellow-100 px-1">{agent}</h2>
  <p class="response font-domine w-full h-full max-h-48 px-3 my-3 overflow-y-scroll">{response}</p>

  {#if hasSave}
    <button class="relative mt-auto bg-Tpurple-100 hover:bg-Tyellow-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter px-2 rounded-full w-fit" on:click={save}>Save to History</button>
  {/if}
</div>

<!-- <style>
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
</style> -->
