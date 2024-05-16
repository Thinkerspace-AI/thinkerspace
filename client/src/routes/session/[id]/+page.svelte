<script lang="ts">
  import AgentCompletion from "$lib/components/AgentCompletion.svelte";
  import { RemoteRunnable } from "@langchain/core/runnables/remote";
  import type { AIMessageChunk } from "langchain/schema";
  import type { Session } from "@auth/core/types";
  import { onMount } from "svelte";

  export let data: {
    title: string;
    messages: [agent: string, message: string, picked: boolean][];
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
    let temp = data.messages;

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

  let promptinput: string;
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

    const input = promptinput;

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

<div class="session max-h-screen flex flex-col items-center">
  <div class="w-3/4 pb-2 h-screen flex flex-col justify-center">
    <h1 class="font-bold font-inter text-2xl mt-4 pb-1 w-full text-center">{data.title}</h1>
    <!-- <p class="text-sm pb-1 w-full text-center">Session ID: {sessionId}</p> -->
    <div
      bind:this={responses}
      class="responses bg-white w-full xl:h-1/2 2xl:h-3/5 overflow-y-scroll mt-2 mb-6 px-2 flex flex-col flex-end"
    >
      <div class="mt-auto relative bottom-0 flex flex-col flex-end">
        {#each completions as completionSet}
          <div class="h-fit">
            <p class="font-domine text-md text-justify px-2 my-2">{completionSet[0]}</p>
            <div class="completion-set grid grid-cols-3 gap-1">
              {#each completionSet[1] as completion, idx}
                <AgentCompletion
                  {completion}
                  save={() => save(completionSet[0], completionSet[1], idx)}
                />
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>

    <div class="w-full h-fit flex items-center">
      <textarea
        class="h-24 w-full resize-none text-justify p-2 overflow-y-scroll"
        bind:value={promptinput}
        placeholder="Enter your prompt"
      />
      <div class="px-5 w- h-fit flex flex-col items-center justify-center h-fit">
        <button
          class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-2 px-4 my-2 mx-2 rounded-full w-fit"
          tabindex="-1"
          on:click={submit}>Submit</button
        >
      </div>
    </div>
  </div>
</div>

<!-- <style>
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
</style> -->
