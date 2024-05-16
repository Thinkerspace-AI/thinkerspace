<script lang="ts">
  export let data: {
    sessions: {
      session_id: string;
      title: string;
      last_message: string;
      timestamp: string;
    }[];
  };

  const sessions = data.sessions;
</script>

<div class="flex flex-col overflow-hidden h-screen max-h-screen">
  <div class="m-auto m w-fit h-2/3 flex flex-col items-center overflow-y-scroll">
    <div class="mr-8">
      {#each sessions as session}
        <div class="flex h-fit flex-row items-center justify-center mb-3">
          <div class="h-fit mr-40 w-full flex flex-col items-left justify-center">
            <h1 class="font-bold font-inter text-2xl pb-1 pl-1">
              <a href="/session/{session.session_id}">{session.title}</a>
            </h1>
            <h6 class="">{session.last_message}</h6>
          </div>
          <button
            class="bg-Tpurple-100 hover:bg-Tyellow-100 outline outline-offset-1 outline-Tpurple-100 text-Tyellow-100 hover:text-Tpurple-100 text-lg font-inter py-2 px-4 rounded-full w-fit h-fit"
            tabindex="-1"><a href="/session/{session.session_id}">Open</a></button
          >
        </div>
      {/each}
    </div>
  </div>
</div>
