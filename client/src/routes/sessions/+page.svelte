<script lang="ts">
  export let data: {
    sessions: string[];
  };

  const sessions = data.sessions;
</script>

{#each sessions as session}
  <p><a href="/session/{session}">{session}</a></p>
{/each}
