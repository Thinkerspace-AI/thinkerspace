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

    nextSlide(n);

    const chain = new RemoteRunnable({
      url: "http://localhost:8000/openai",
    });

    const result = await chain.invoke(
      {
        human_input: "cats",
      },
      {
        configurable: {
          session_id: "57988dfa-34bf-4ac7-838f-624ec550a802",
        },
      }
    );

    console.log(result);
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
  <button on:click={() => nextSlide(3)}>Next</button>
</div>
<div class="slide" id="slide4">
  <h1>Do you wanna build a snowman?</h1>
  <h6>Come on let's go and play</h6>

  <textarea name="q4" id="q4" rows="10" placeholder="Type here..."></textarea>
  <button on:click={() => submit(4)}>Submit</button>
</div>
<div class="slide" id="slide5">
  <h1>Here's what I understood:</h1>
  <p>
    <span class="agent">CONVENER:</span> Your business idea is lorem ipsum dolor
    sit amet. I've identified areas that you'd need to build on:
  </p>
  <p>
    <span class="agent">CONVENER:</span> Your business idea is lorem ipsum dolor
    sit amet
  </p>
  <p>
    <span class="agent">CONVENER:</span> Your business idea is lorem ipsum dolor
    sit amet
  </p>
  <p>
    <span class="agent">CONVENER:</span> Your business idea is lorem ipsum dolor
    sit amet
  </p>
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
