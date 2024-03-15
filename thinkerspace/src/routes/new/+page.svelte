<script lang="ts">
  import { RemoteRunnable } from "@langchain/core/runnables/remote";
  // import QuestionSlide from "$lib/components/QuestionSlide.svelte";

  function nextSlide(n: number) {
    const textarea = document.getElementById(`q${n}`) as HTMLTextAreaElement;

    if (!textarea.value) {
      textarea.style.boxShadow = "0 0 24px var(--20)";
      textarea.focus();
      return;
    }

    const next = document.getElementById(`slide${n + 1}`);

    if (!next) {
      console.log("No next slide");
      return;
    }

    next.style.display = "block";

    window.scrollBy({
      top: window.innerHeight,
      behavior: "smooth",
    });
  }

  async function submit(n: number) {
    console.log("Submitting");

    const chain = new RemoteRunnable({
      url: "https://llm-app-whtpnrbuea-as.a.run.app/agent",
    });

    const answers = Array.from(document.getElementsByTagName("textarea")).map(
      (textarea) => textarea.value
    );

    const result = (await chain.invoke(
      {
        human_input: answers.join("\n"),
      },
      {
        configurable: {
          session_id: "57988dfa-34bf-4ac7-838f-624ec550a802",
          agent: "UI/UX Designer"
        },
      }
    )) as any;

    console.log(result);

    const resText = document.getElementById("response") as HTMLParagraphElement;

    resText.innerText = result;

    const data = {
      agents: ["UI/UX Designer", "Marketing Specialist", "Product Manager"],
      session_id: "test-session"
    }

    const createResult = (await fetch(
      "https://llm-app-whtpnrbuea-as.a.run.app/select/",
      {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      }
    )).json()

    console.log(createResult)

    nextSlide(n);
  }
</script>

<div class="slide" id="slide1">
  <h1>What problem are you trying to solve?</h1>
  <h6>Explain the specific pain points or challenges you want to address.</h6>

  <textarea name="q1" id="q1" rows="10" placeholder="Type here..."></textarea>
  <button on:click={() => nextSlide(1)}>Next</button>
</div>
<div class="slide" id="slide2">
  <h1>Who is your ideal customer?</h1>
  <h6>Dive into the demographics and behaviors of your target audience.</h6>

  <textarea name="q2" id="q2" rows="10" placeholder="Type here..."></textarea>
  <button on:click={() => nextSlide(2)}>Next</button>
</div>
<div class="slide" id="slide3">
  <h1>What is your big idea?</h1>
  <h6>Share your vision.</h6>

  <textarea name="q3" id="q3" rows="10" placeholder="Type here..."></textarea>
  <button on:click={() => submit(3)}>Submit</button>
</div>
<div class="slide" id="slide4">
  <h1>Here's what I understood:</h1>
  <p id="response"></p>
</div>

<style>
  /* :global(body) {
    overflow: hidden;
  } */

  .slide {
    height: 100vh;
    width: 100%;

    padding: 240px;
  }

  .slide:not(.slide:first-of-type) {
    display: none;
  }

  textarea {
    width: 100%;
    padding: 24px;
    margin-top: 24px;
    resize: none;

    border: none;
    box-shadow: 0 0 24px rgba(0, 0, 0, 0.1);
  }

  textarea:focus {
    outline: none;
    scale: 1.02;
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
