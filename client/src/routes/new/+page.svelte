<script lang="ts">
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

  let answers: string[] = [];

  let slidesContainer: HTMLDivElement;
  let slides: Element[];

  onMount(() => {
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

  let response = "";

  async function test(): Promise<string> {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve("done!");
      }, 1000);
    });
  }

  async function submit() {
    console.log("Submitting");
    console.log(answers);

    if (slides[slides.length - 1]) {
      slides[slides.length - 1].scrollIntoView({ behavior: "smooth" });
    }

    console.log(response);
    response = await test();
    console.log(response);
  }

  // async function submit(n: number) {
  //   console.log("Submitting");

  //   const chain = new RemoteRunnable({
  //     url: "http://localhost:8000/openai",
  //   });

  //   const answers = Array.from(document.getElementsByTagName("textarea")).map(
  //     (textarea) => textarea.value
  //   );

  //   const result = (await chain.invoke(
  //     {
  //       human_input: answers.join("\n"),
  //     },
  //     {
  //       configurable: {
  //         session_id: "57988dfa-34bf-4ac7-838f-624ec550a802",
  //       },
  //     }
  //   )) as any;

  //   console.log(result);

  //   const resText = document.getElementById("response") as HTMLParagraphElement;

  //   resText.innerText = result.content;
  // }
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
    {#await response}
      <p>Loading...</p>
    {:then res}
      <p>{res}</p>
    {:catch error}
      <p>{error}</p>
    {/await}
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
</style>
