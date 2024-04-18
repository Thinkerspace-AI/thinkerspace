<div class="slide">
  <div class="slide-content">
    <slot />
  </div>
</div>

<style>
  .slide {
    height: 100vh;
    width: 100vw;
    padding-top: 10px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
