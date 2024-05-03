<script lang="ts">
  import AgentCompletion from "$lib/components/AgentCompletion.svelte";
  import { RemoteRunnable } from "@langchain/core/runnables/remote";
  import type { AIMessageChunk } from "langchain/schema";
  import type { Session } from "@auth/core/types";
  import { onMount } from "svelte";

  export let data: {
    history: [agent: string, message: string, picked: boolean][];
    agents: string[];
    id: string;
    session: Session;
  };

  const sessionId = data.id;
  const clientSession = data.session;
  const userId = clientSession.user?.id as string;

  let completions: [string, [string, string][]][] = [];
  let agents: string[] = data.agents;

  onMount(() => {
    // Retrieve stored agents and history
    let history: [string, string, boolean][][] = [];
    let temp = data.history;

    while (temp.length) {
      history.push(temp.splice(0, agents.length + 1));
    }

    completions = history.map((completionSet) => {
      // @ts-ignore
      const prompt = completionSet.shift().message as string;

      console.log("Prompt: ", prompt);

      const completions = completionSet.map((completion) => {
        // @ts-ignore
        return [completion.agent, completion.message];
      }) as [string, string][];

      console.log("Completions: ", completions);

      return [prompt, completions];
    });
  });

  let inputElement: HTMLInputElement;
  let responses: HTMLDivElement;

  async function generateCompletion(
    agent: string,
    input: string,
    agentCompletions: [string, string],
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
          session_id: sessionId,
        },
      },
    )) as AsyncGenerator<AIMessageChunk>;

    console.log("Stream created. Res: ", res);

    for await (const chunk of res) {
      if (!chunk.content) continue;

      // console.log("Chunk: ", chunk);
      agentCompletions[1] += chunk.content;
      completions = completions;
    }
  }

  async function save(prompt: string, completions: [string, string][], pickedIndex: number) {
    console.log("Saving to history...");

    const agent = completions[pickedIndex][0];
    const message = completions[pickedIndex][1];

    const notPicked = completions.filter((_, idx) => idx !== pickedIndex);

    const saveResponse = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        session_id: sessionId,
        prompt: prompt,
        completion_agent: agent,
        completion_message: message,
        not_picked_1_agent: notPicked[0][0],
        not_picked_1_message: notPicked[0][1],
        not_picked_2_agent: notPicked[1][0],
        not_picked_2_message: notPicked[1][1],
      }),
    });

    console.log(saveResponse);
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
  <p>Session ID: {sessionId}</p>
  <input bind:this={inputElement} type="text" placeholder="Enter your prompt" />
  <button on:click={submit}>Submit</button>
  <div bind:this={responses} class="responses">
    {#each completions as completionSet}
      <p>{completionSet[0]}</p>
      <div class="completion-set">
        {#each completionSet[1] as completion, idx}
          <AgentCompletion
            {completion}
            save={() => save(completionSet[0], completionSet[1], idx)}
          />
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
    max-height: 80vh;
  }

  .completion-set {
    display: flex;
    flex-direction: row;
  }
</style>
