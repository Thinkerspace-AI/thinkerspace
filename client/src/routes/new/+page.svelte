<script lang="ts">
  type SuggestedAgents = [string, string][];

  import { RemoteRunnable } from "@langchain/core/runnables/remote";

  import { onMount } from "svelte";

  import TitleDescription from "$lib/components/TitleDescription.svelte";
  import Slide from "$lib/components/Slide.svelte";
  import QuestionContent from "$lib/components/QuestionContent.svelte";

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

  const allAgents = [
    "UI/UX Designer",
    "Software Developer",
    "Business Analyst",
    "Marketing Specialist",
    "End User",
    "Product Manager",
  ];

  let answers: string[] = [];
  let response: SuggestedAgents = [];
  let selectedAgents: string[] = [];
  let sessionId: string;

  let slidesContainer: HTMLDivElement;
  let slides: Element[];

  onMount(() => {
    window.scrollTo(0, 0);
    slides = Array.from(slidesContainer.children);
  });

  function nextSlide(n: number) {
    const currentSlide = slides[n];
    const currentInput = currentSlide.querySelector(
      "input"
    ) as HTMLInputElement;

    answers = [...answers, currentInput.value];

    const nextSlide = slides[n + 1];

    if (nextSlide) {
      nextSlide.scrollIntoView({ behavior: "smooth" });

      const nextInput = (nextSlide.querySelector("input") ||
        nextSlide.querySelector("button")) as HTMLElement;

      if (nextInput) {
        setTimeout(() => {
          nextInput.focus();
        }, 500);
      }
    }
  }

  function keydown(e: KeyboardEvent) {
    if (e.key === "Tab") {
      e.preventDefault();
    }
  }

  async function submit() {
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
        return res.agents.map((e, i) => [e, res.reasons[i]]);
      })) as SuggestedAgents;

    if (slides[slides.length - 1]) {
      slides[slides.length - 1].scrollIntoView({ behavior: "smooth" });
    }

    console.log(response);
  }

  async function confirm() {
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
  {#each Object.entries(questions) as [id, { question, description }], i (id)}
    <Slide>
      <QuestionContent {question} {description} next={() => nextSlide(i)} />
    </Slide>
  {/each}
  <Slide>
    <h1>Here's what you said</h1>
    <h6>Let's make sure we got it right</h6>

    {#each answers as answer, i}
      <TitleDescription title={questions[i].question} description={answer} />
    {/each}

    <button on:keydown={keydown} on:click={submit}>Next</button>
  </Slide>
  <Slide>
    <h1>Here's what I think</h1>
    <p>You might need help from the following agents:</p>
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
    <p>You might also want help from other agents</p>
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
      <button on:keydown={keydown} on:click={confirm}>Confirm</button>
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

  .agents {
    padding: 1rem 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .agent {
    padding: 1rem;
    border: 1px solid var(--gray);
    border-radius: 8px;
    text-align: justify;

    user-select: none;
  }
</style>
