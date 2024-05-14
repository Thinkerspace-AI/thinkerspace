<script lang="ts">
  import AgentCompletion from "$lib/components/AgentCompletion.svelte";
  import { RemoteRunnable } from "@langchain/core/runnables/remote";
  import type { AIMessageChunk } from "langchain/schema";

  import { onMount } from "svelte";

  export let data: { id: string };

  const sessionId = data.id;

  let userinput: string;
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

    const input = userinput;

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
    // var promptfield = document.getElementById('promptarea');
    // if(promptfield) {
    //   promptfield.value =
    // }
    userinput = "";

  }


</script>

<div class="session max-h-screen flex flex-col items-center">
  <div class="w-3/4 pb-2 h-screen flex flex-col justify-center">
    <h1 class="font-bold font-inter text-2xl mt-4 cpb-1 w-full text-center">Session Name (set by User)</h1>
    <div bind:this={responses} class="responses bg-white w-full h-3/5 overflow-y-scroll mt-2 mb-6 px-2 flex flex-col flex-end"></div>
      <div class="mt-auto relative bottom-0 flex flex-col flex-end">
        {#each completions as completionSet}
          <div class="h-fit">
            <p class="text-justify px-2 my-2">You entered: "{completionSet[0]}"</p>
            <div class="completion-set grid grid-cols-3 gap-1">
              {#each completionSet[1] as completion}
                <AgentCompletion prompt={completionSet[0]} {sessionId} {completion} />
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
    <div class="w-full h-fit flex items-center">
      <textarea id="promptarea" placeholder="Type your prompt here..." bind:value={userinput} class="h-24 w-full resize-none text-justify p-2 overflow-y-scroll"></textarea>
      <div class="px-5 w-fit h-fit flex flex-col items-center justify-center h-fit">
        <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 font-inter py-2 px-4 my-2 mx-2 rounded-full w-fit" tabindex="-1" on:click={submit}>Submit</button>
        <p class="text-xs">Session ID</p>
        <p class="text-xs">#{data.id}</p>
      </div>
    </div>
  </div>
</div>

