<script lang="ts">
  type SuggestedAgents = [string, string][];

  import { RemoteRunnable } from "@langchain/core/runnables/remote";

  import { onMount } from "svelte";

  import Modal from '$lib/components/Modal.svelte';
  import TitleDescription from "$lib/components/TitleDescription.svelte";
  import Slide from "$lib/components/Slide.svelte";
  import QuestionContent from "$lib/components/QuestionContent.svelte";

  const questions = [
    { id: 1,
      question: "What problem are you trying to solve?",
      description:
        "Explain the specific pain points or challenges you want to address.",
    },
    { id: 2,
      question: "Who is your ideal customer?",
      description:
        "Dive into the demographics and behaviors of your target audience.",
    },
    { id: 3,
      question: "What is your big idea?",
      description: "Share your vision.",
    },
  ];

  const allAgents = [
    "UI/UX Designer",
    "Software Developer",
    "Business Analyst",
    "Marketing Specialist",
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

  let confirmation_modal: Modal;

  onMount(() => {
    window.scrollTo(0, 0);
    slides = Array.from(slidesContainer.children);
  });

  function keydown(e: KeyboardEvent) {
    if (e.key === "Tab") {
      e.preventDefault();
    }
  }

  async function submit() {
    answers = [answer1, answer2, answer3];
    console.log("Submitting");
    console.log(answers);

    response = (await fetch("https://llm-app-whtpnrbuea-as.a.run.app/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        agent: "Test",
        userid: "Test",
      }),
    })
      .then((res) => res.json())
      .then((json) => json.id)
      .then((id) => {
        const chain = new RemoteRunnable({
          url: "https://llm-app-whtpnrbuea-as.a.run.app/convene",
        });

        console.log("Session ID: %s", id);

        sessionId = id;

        return chain.invoke(
          {
            human_input: answers.join("\n"),
          },
          {
            configurable: {
              session_id: id,
            },
          }
        );
      })
      .then((res) => {
        // @ts-ignore
        selectedAgents = res.agents;
        // @ts-ignore
        return res.agents.map((e, i) => [e, res.reasons[i]]);
      })) as SuggestedAgents;

    if (slides[slides.length - 1]) {
      slides[slides.length - 1].scrollIntoView({ behavior: "smooth" });
    }

    console.log(response);
  }

  async function confirmAgents() {
    console.log("Confirming");
    console.log(selectedAgents);

    const confirmResponse = await fetch(
      "https://llm-app-whtpnrbuea-as.a.run.app/select",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          agents: selectedAgents,
          session_id: sessionId,
        }),
      }
    );

    console.log(confirmResponse);
  }
</script>

<div class="slides-container" bind:this={slidesContainer}>
  <Slide>
    <div class="question">
      <h1>What problem are you trying to solve?</h1>
      <h6>Explain the specific pain points or challenges you want to address.</h6>
      <textarea bind:value={answer1}
        placeholder="Type here..."
      />
    </div>
  
    <div class="question">
      <h1>Who is your ideal customer?</h1>
      <h6>Dive into the demographics and behaviors of your target audience.</h6>
      <textarea bind:value={answer2} 
        placeholder="Type here..."
      />
    </div>
  
    <div class="question">
      <h1>What is your big idea?</h1>
      <h6>Share your vision.</h6>
      <textarea bind:value={answer3}
        placeholder="Type here..."
      />
    </div>
  
    <button on:keydown={keydown} on:click={() => confirmation_modal.open()}>Submit</button>
  
    <Modal bind:this={confirmation_modal}>
      <h1>Would you like to submit your answers?</h1>
      <button on:keydown={keydown} on:click={submit}>Submit</button>
      <button on:keydown={keydown} on:click={() => confirmation_modal.close()}>Close</button>
    </Modal>
  </Slide>
  
  <Slide>
    <h1>Here's what I think.</h1>
    <p>The following agents would be most helpful:</p>
    <div class="agents">
      {#if response.length === 0}
        <p>Loading...</p>
      {:else}
        {#each response as [name, description]}
          <div class="agent">
            <label>
              <input
                type="checkbox"
                name="agents"
                value={name}
                bind:group={selectedAgents}
                checked={true}
              />
              {name}
              {#if description}
                <p>{description}</p>
              {:else}
                <p>No description</p>
              {/if}
            </label>
          </div>
        {/each}
      {/if}
    </div>
    <p>Any recommended agents not to your liking? You might want help from these agents instead:</p>
    <div class="agents">
      {#each allAgents as agent}
        {#if !response.find(([name]) => name === agent)}
          <div class="agent">
            <label>
              <input
                type="checkbox"
                name="agents"
                value={agent}
                bind:group={selectedAgents}
              />
              {agent}
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </label>
          </div>
        {/if}
      {/each}
    </div>
    <div id="agents-info">
      {#if selectedAgents.length > 3}
        <p>Too many agents selected. Please select up to to three only.</p>
      {:else if selectedAgents.length > 0}
        <p>Selected agents: {selectedAgents.join(", ")}</p>
      {/if}
      <button on:click={confirmAgents}>Confirm</button>
    </div>
  </Slide>
</div>

<style>
  :global(body) {
    overflow: hidden;
  }

  button {
    background: var(--white);
    padding: 12px 24px;

    align-self: center;
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

  .agents {
    padding: 1rem 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    width: 70vw;
  }

  .agent {
    background: var(--white);
    padding: 1rem;
    border: 1px solid var(--gray);
    border-radius: 8px;
    text-align: justify;

    user-select: none;
  }

  .question {
    margin: auto;
    width: 70vw;
  }

  textarea {
    padding: 10px 10px;
    resize: none;
    height: 16vh;
    width: 70vw;
  }
</style>
