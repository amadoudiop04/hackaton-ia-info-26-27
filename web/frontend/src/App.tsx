// Layout + orchestration : Sidebar + ChatWindow + ChatInput.
// Owner: Amadou (feat/backend-api / intégration)

import { useState } from "react";
import { ChatInput } from "./components/ChatInput";
import { ChatWindow } from "./components/ChatWindow";
import { Sidebar } from "./components/Sidebar";
import { useChat } from "./hooks/useChat";
import type { ChatParams } from "./types/chat";
import "./styles/global.css";
import "./styles/chat.css";
import "./styles/sidebar.css";

const DEFAULT_PARAMS: ChatParams = {
  temperature: 0.7,
  maxTokens: 512,
  model: "phi3.5-financial",
};

export default function App() {
  const [params, setParams] = useState<ChatParams>(DEFAULT_PARAMS);
  const { messages, loading, sendMessage, clear } = useChat(params);

  return (
    <div className="app">
      <Sidebar
        params={params}
        messages={messages}
        onChange={setParams}
        onClear={clear}
      />
      <main className="app__main">
        <header className="app__header">TechCorp — Phi-3.5-Financial</header>
        <ChatWindow messages={messages} loading={loading} model={params.model} />
        <ChatInput
          params={params}
          onParamsChange={setParams}
          onSend={sendMessage}
          disabled={loading}
        />
      </main>
    </div>
  );
}
