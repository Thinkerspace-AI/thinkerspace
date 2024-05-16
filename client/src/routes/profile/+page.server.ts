import { redirect, error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async (event) => {
  const session = await event.locals.auth();

  if (!session?.user) {
    throw redirect(303, "/login");
  }

  // Get Sessions
  const sessionReq = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/getsessions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: session.user.id,
    }),
  });

  if (!sessionReq.ok) {
    throw error(sessionReq.status, "Failed to fetch sessions");
  }

  const sessionsJson = (await sessionReq.json()) as {session_id: string}[]
  
  const sessions = sessionsJson.map(session => session.session_id);

  console.log(sessions);

  return { sessions };
}