// Layout + orchestration : Sidebar + accueil/conversation + composer.
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
  temperature: 0.6,
  maxTokens: 1024,
  model: "phi3.5-financial",
};

const GREETING = "Bonjour, par quoi commençons-nous ?";

export default function App() {
  const [params, setParams] = useState<ChatParams>(DEFAULT_PARAMS);
  const { messages, loading, sendMessage, clear } = useChat(params);
  const isEmpty = messages.length === 0;

  const composer = (
    <ChatInput
      params={params}
      onParamsChange={setParams}
      onSend={sendMessage}
      disabled={loading}
    />
  );

  return (
    <div className="app">
      <Sidebar onClear={clear} />
      <main className="app__main">
        <header className="app__header" />

        {isEmpty ? (
          <div className="home">
            <h1 className="home__greeting">{GREETING}</h1>
            <div className="home__composer">{composer}</div>
          </div>
        ) : (
          <>
            <ChatWindow messages={messages} loading={loading} />
            <div className="composer-dock">
              <div className="composer-dock__inner">{composer}</div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
