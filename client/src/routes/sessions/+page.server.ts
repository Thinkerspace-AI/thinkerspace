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

  const sessions = await sessionReq.json();

  console.log(sessions);

  return { sessions };
}