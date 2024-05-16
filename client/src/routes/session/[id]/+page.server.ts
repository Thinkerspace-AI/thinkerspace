import { redirect, error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async (event) => {
  const id = event.params.id
  const session = await event.locals.auth();

  if (!session?.user) {
    throw redirect(303, "/login");
  }

  // Fetch History
  const historyReq = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/history", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: id,
      user_id: session.user.id,
    }),
  });

  if (!historyReq.ok) {
    throw error(historyReq.status, "Failed to fetch history");
  }

  // Fetch Agents
  const agentsReq = await fetch("https://llm-app-whtpnrbuea-as.a.run.app/getagents", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: id,
      user_id: session.user.id,
    }),
  });

  if (!agentsReq.ok) {
    throw error(agentsReq.status, "Failed to fetch agents");
  }

  const history = await historyReq.json();
  const agents = (await agentsReq.json()).agents;

  const title = history.title;
  const messages = history.messages;

  return { title, messages, agents, session, id }
};