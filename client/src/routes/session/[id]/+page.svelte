<script lang="ts">
  import AgentCompletion from "$lib/components/AgentCompletion.svelte";
  import { RemoteRunnable } from "@langchain/core/runnables/remote";
  import type { AIMessageChunk } from "langchain/schema";

  import { onMount } from "svelte";

  export let data: { id: string };

  const sessionId = data.id;

  let inputElement: HTMLInputElement;
  let responses: HTMLDivElement;
  let completions: [string, [string, string][]][] = [];

  let agents: string[] = [
    "UI/UX Designer",
    "Technical Engineer",
    "Financial Analyst",
  ];

  // onMount(async () => {
  //   console.log("Mounted!");

  //   const result = await fetch(
  //     "https://llm-app-whtpnrbuea-as.a.run.app/getagents",
  //     {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         session_id: sessionId,
  //       }),
  //     }
  //   );

  //   console.log("Result: ", result);
  // });

  async function generateCompletion(
    agent: string,
    input: string,
    agentCompletions: [string, string]
  ) {
    const chain = new RemoteRunnable({
      url: "https://llm-app-whtpnrbuea-as.a.run.app/agent",
    });

    const res = (await chain.stream(
      {
        human_input: input,
      },
      {
        configurable: {
          agent: agent,
          session_id: data.id,
        },
      }
    )) as AsyncGenerator<AIMessageChunk>;

    console.log("Stream created. Res: ", res);

    for await (const chunk of res) {
      if (!chunk.content) continue;

      // console.log("Chunk: ", chunk);
      agentCompletions[1] += chunk.content;
      completions = completions;
    }
  }

  async function submit() {
    console.log("Submitting...");

    const input = inputElement.value;

    const newCompletions: [string, string][] = agents.map((agent) => {
      return [agent, ""];
    });

    completions = [...completions, [input, newCompletions]];

    console.log("Before Completions: ", completions);

    agents.forEach((agent, idx) => {
      console.log("Passed to generateCompletion: ", newCompletions[idx]);
      generateCompletion(agent, input, newCompletions[idx]);
    });

    completions = completions;
  }
</script>

<div class="session">
  <h1>Session</h1>
  <p>Session ID: {data.id}</p>
  <input bind:this={inputElement} type="text" placeholder="Enter your prompt" />
  <button on:click={submit}>Submit</button>
  <div bind:this={responses} class="responses">
    {#each completions as completionSet}
      <p>{completionSet[0]}</p>
      <div class="completion-set">
        {#each completionSet[1] as completion}
          <AgentCompletion prompt={completionSet[0]} {sessionId} {completion} />
        {/each}
      </div>
    {/each}
  </div>
</div>

<style>
  .responses {
    display: flex;
    flex-direction: column;
  }

  .completion-set {
    display: flex;
    flex-direction: row;
  }
</style>
