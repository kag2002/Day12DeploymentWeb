import { ChatResponse, Message } from "../types/chat";

const API_BASE = "/api";
const AGENT_API_KEY = process.env.NEXT_PUBLIC_AGENT_API_KEY || "dev-key-change-me";

export async function sendChatMessage(
  messages: Message[],
  temperature: number = 0.7,
  sessionId?: string
): Promise<ChatResponse> {
  const payload = {
    messages: messages.map(m => ({
      role: m.role,
      content: m.content
    })),
    temperature,
    session_id: sessionId
  };

  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": AGENT_API_KEY
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `HTTP Error ${response.status}`);
  }

  return response.json();
}
