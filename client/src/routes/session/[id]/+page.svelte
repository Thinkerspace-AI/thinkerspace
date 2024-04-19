<script lang="ts">
  import { RemoteRunnable } from "@langchain/core/runnables/remote";
  import type { AIMessageChunk } from "langchain/schema";

  export let data: { id: string };

  let inputElement: HTMLInputElement;
  let responses: HTMLDivElement;
  let completions: [string, [string, string][]][] = [];

  let agents: string[] = [
    "UI/UX Designer",
    "Technical Engineer",
    "Financial Analyst",
  ];

  async function generateCompletion(
    agent: string,
    input: string,
    agentCompletions: [string, string]
  ) {
    const chain = new RemoteRunnable({
      url: "https://llm-app-whtpnrbuea-as.a.run.app/agent",
    });

    console.log("Chain created");
    console.log("Input: ", input);
    console.log("Agent: ", agent);
    console.log("Session ID: ", data.id);

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
          <div class="completion">
            <h2>{completion[0]}</h2>
            <p>{completion[1]}</p>
          </div>
        {/each}
      </div>
    {/each}
  </div>
</div>

<style>
  .responses {
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
  }

  .completion-set {
    display: flex;
    flex-direction: row;
  }

  .completion {
    margin: 1rem;
    padding: 1rem;
    border: 1px solid black;
  }
</style>
