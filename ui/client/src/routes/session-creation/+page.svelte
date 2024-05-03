<script lang="ts">
  type SuggestedAgents = [string, string][];

  import { RemoteRunnable } from "@langchain/core/runnables/remote";

  import { goto } from '$app/navigation';

  import { onMount } from "svelte";

  import Slide from "$lib/components/Slide.svelte";
  import Modal from "$lib/components/Modal.svelte";

  const questions = [
    {
      question: "What problem are you trying to solve?",
      description:
        "Explain the specific pain points or challenges you want to address.",
    },
    {
      question: "Who is your ideal customer?",
      description:
        "Dive into the demographics and behaviors of your target audience.",
    },
    {
      question: "What is your big idea?",
      description: "Share your vision.",
    },
  ];

  const allAgents1 = [
    "UI/UX Designer",
    "Marketing Specialist",
    "Business Analyst",
  ];
  const allAgents2  = [
    "Software Developer",
    "End User",
    "Product Manager",
  ];

  let answer1: string;
  let answer2: string;
  let answer3: string;
  let answers: string[] = [];
  let response: SuggestedAgents = [];
  let selectedAgents: string[] = [];
  let sessionId: string;

  let slidesContainer: HTMLDivElement;
  let slides: Element[];

  let submitModal: Modal;
  let agentModal: Modal;

  onMount(() => {
    window.scrollTo(0, 0);
    slides = Array.from(slidesContainer.children);
  });

  function keydown(e: KeyboardEvent) {
    if (e.key === "Tab") {
      e.preventDefault();
    }
  }

  async function openSubmitModal() {
    submitModal.open();
  }

  async function closeSubmitModal() {
    submitModal.close();
  }

  async function confirmAnswers() {
    submitModal.close();
    submit();
  }

  async function confirmAgents() {
    agentModal.close();
    confirm();
  }

  async function openAgentModal() {
    agentModal.open();
  }

  async function closeAgentModal() {
    agentModal.close();
  }

  async function submit() {
    answers = [answer1, answer2, answer3];
    console.log("Submitting");
    console.log(answers);

    // response = (await fetch("https://llm-app-whtpnrbuea-as.a.run.app/create", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({
    //     agent: "Test",
    //     userid: "Test",
    //   }),
    // })
    //   .then((res) => res.json())
    //   .then((json) => json.id)
    //   .then((id) => {
    //     const chain = new RemoteRunnable({
    //       url: "https://llm-app-whtpnrbuea-as.a.run.app/convene",
    //     });

    //     console.log("Session ID: %s", id);

    //     sessionId = id;

    //     return chain.invoke(
    //       {
    //         human_input: answers.join("\n"),
    //       },
    //       {
    //         configurable: {
    //           session_id: id,
    //         },
    //       }
    //     );
    //   })
    //   .then((res) => {
    //     // @ts-ignore
    //     selectedAgents = res.agents;
    //     // @ts-ignore
    //     return res.agents.map((e, i) => [e, res.reasons[i]]);
    //   })) as SuggestedAgents;

    if (slides[slides.length - 1]) {
      slides[slides.length - 1].scrollIntoView({ behavior: "smooth" });
    }

    console.log(response);
  }

  async function confirm() {

    console.log("Confirming");
    console.log(selectedAgents);

		goto('/session/00001101');

    // const confirmResponse = await fetch(
    //   "https://llm-app-whtpnrbuea-as.a.run.app/select",
    //   {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       agents: selectedAgents,
    //       session_id: sessionId,
    //     }),
    //   }
    // );

    // console.log(confirmResponse);


  }
</script>

<div class="slides-container flex flex-col overflow-hidden max-h-screen" bind:this={slidesContainer}>
  <Slide>
    <div class="m-auto w-8/12 h-screen flex flex-none flex-col items-center justify-center">
      <div class="slide-content pb-2 w-full">
        <h1 class="font-bold font-inter text-2xl pb-1 pl-1">{questions[0].question}</h1>
        <h6 class="pb-1 pl-1">{questions[0].description}</h6>
        <textarea placeholder="Type here..." bind:value={answer1} class="h-20 w-full resize-none text-justify p-2 overflow-y-scroll focus:h-48" tabindex="-1"></textarea>
      </div>
      <div class="slide-content pb-2 w-full">
        <h1 class="font-bold font-inter text-2xl pb-1 pl-1">{questions[1].question}</h1>
        <h6 class="pb-1 pl-1">{questions[1].description}</h6>
        <textarea placeholder="Type here..." bind:value={answer2} class="h-20 w-full resize-none text-justify p-2 overflow-y-scroll focus:h-48" tabindex="-1"></textarea>
      </div>
      <div class="slide-content pb-8 w-full">
        <h1 class="font-bold font-inter text-2xl pb-1 pl-1">{questions[2].question}</h1>
        <h6 class="pb-1 pl-1">{questions[2].description}</h6>
        <textarea placeholder="Type here..." bind:value={answer3} class="h-20 w-full resize-none text-justify p-2 overflow-y-scroll focus:h-48" tabindex="-1"></textarea>
      </div>
      <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit" tabindex="-1" on:click={openSubmitModal}>
        Submit
      </button>
    </div>
  </Slide>

  <Modal bind:this={submitModal}>
    <h1 class="font-bold font-inter text-2xl pb-1">This action will start the session.</h1>
    <h1 class="font-bold font-inter text-2xl pb-6">Are you satisfied with your answers?</h1>    <div>
      <button class="bg-white hover:bg-Tyellow-100 text-Tpurple-100 hover:text-Tpurple-100 text-lg font-inter font-bold py-2 px-4 mr-3 rounded-full w-fit" on:click={closeSubmitModal}>Cancel</button>
      <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit" on:click={confirmAnswers}>Confirm</button>
    </div>
  </Modal>

  <Slide>
    <div class="m-auto w-8/12 h-screen flex flex-col items-center justify-center">
      <h1 class="font-inter text-2xl pb-1">Here's what I think.</h1>
      <p class="font-inter text-xl pb-4">You might need help from the following agents:</p>
      <div class="agents grid grid-cols-3 gap-4 pb-6 text-justify">
        {#each allAgents1 as agent}
          <div class="agent border-solid border-2 h-40 overflow-y-scroll bg-white select-none">
            <label class="font-domine">
              <input
                type="checkbox"
                name="agents"
                value={agent}
                bind:group={selectedAgents}
                tabindex="-1"
              />
              {agent}
              <p>This is a sample description for demo purposes. This is a sample description for demo purposes. This is a sample description for demo purposes. This is a sample description for demo purposes. This is a sample description for demo purposes.</p>
            </label>
          </div>
        {/each}
      </div>
      <p class="font-inter text-xl pb-4">Are any of the recommended agents not to your liking? You can choose these agents instead:</p>
      <div class="agents grid grid-cols-3 gap-4 pb-6 text-justify">
        {#each allAgents2 as agent}
          {#if !response.find(([name]) => name === agent)}
            <div class="agent border-solid border-2 h-40 overflow-y-scroll bg-white select-none">
              <label>
                <input
                  type="checkbox"
                  name="agents"
                  value={agent}
                  bind:group={selectedAgents}
                  tabindex="-1"
                />
                {agent}
                <p>This is a sample description for demo purposes. This is a sample description for demo purposes. This is a sample description for demo purposes. This is a sample description for demo purposes. This is a sample description for demo purposes.</p>
              </label>
            </div>
          {/if}
        {/each}
      </div>
      <div id="agents-info" class="flex flex-col items-center h-20">
        {#if selectedAgents.length > 3}
          <p class="font-inter text-xl pb-4">Too many agents selected. Please select up to to three only.</p>
        {:else if selectedAgents.length > 0}
          <p class="font-inter text-xl pb-4">Selected agents: {selectedAgents.join(", ")}</p>
          <button on:click={openAgentModal} tabindex="-1" class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 m-2 rounded-full w-fit">Open Session</button>
        {/if}
        
      </div>
    </div>
  </Slide>

  <Modal bind:this={agentModal}>
    <h1 class="font-bold font-inter text-2xl pb-1">This action will finalize your agents.</h1>
    <h1 class="font-bold font-inter text-2xl pb-6">Are you sure with your selection?</h1>    <div>
      <button class="bg-white hover:bg-Tyellow-100 text-Tpurple-100 hover:text-Tpurple-100 text-lg font-inter font-bold py-2 px-4 mr-3 rounded-full w-fit" on:click={closeAgentModal}>Cancel</button>
      <button class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit" on:click={confirmAgents}>Confirm</button>
    </div>
  </Modal>
</div>
