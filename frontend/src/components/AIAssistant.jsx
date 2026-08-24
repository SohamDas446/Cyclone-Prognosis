import { useEffect, useRef, useState } from "react";

const SUGGESTED_QUESTIONS = [
  "What's the current risk level?",
  "How's the weather looking?",
  "Any cyclones nearby?",
  "What does the forecast show?",
];

function buildLocalAnswer(question, analysis) {
  const q = question.toLowerCase();
  const risk = analysis?.risk;
  const weather = analysis?.weather;
  const cyclones = analysis?.nearby_cyclones || [];
  const forecast = analysis?.forecast;

  if (q.includes("risk")) {
    if (!risk) return "I don't have a risk assessment yet — run an analysis first.";
    return `The current risk level is ${risk.level || "unknown"} (${risk.score ?? "N/A"}/100). ${
      risk.ai_explanation || ""
    }`.trim();
  }

  if (q.includes("weather")) {
    if (!weather?.available) return "Weather data isn't available for this location right now.";
    return `It's currently ${weather.temperature ?? "N/A"}°C with wind at ${
      weather.wind_speed ?? "N/A"
    } and ${weather.relative_humidity ?? "N/A"}% humidity.`;
  }

  if (q.includes("cyclone") || q.includes("nearby") || q.includes("storm")) {
    if (cyclones.length === 0) return "No cyclones are currently tracked within the selected radius.";
    return `There ${cyclones.length === 1 ? "is" : "are"} ${cyclones.length} nearby system${
      cyclones.length === 1 ? "" : "s"
    }: ${cyclones.map((c) => c.name || "unnamed").join(", ")}.`;
  }

  if (q.includes("forecast")) {
    if (!forecast?.available) return "No forecast is available yet — run an analysis first.";
    const first = forecast.predictions?.[0];
    return first
      ? `The model projects ${first.cyclone || "the tracked system"} moving toward ${
          first.predicted_latitude
        }, ${first.predicted_longitude} with winds near ${first.predicted_wind ?? "N/A"}.`
      : "A forecast is available, but no predicted positions were returned.";
  }

  return null;
}

function AIAssistant({ analysis, hasAnalyzed }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [thinking, setThinking] = useState(false);
  const logRef = useRef(null);
  const seededExplanation = useRef(null);

  useEffect(() => {
    const explanation = analysis?.ai_explanation;
    if (explanation && explanation !== seededExplanation.current) {
      seededExplanation.current = explanation;
      setMessages((prev) => [...prev, { role: "ai", text: explanation }]);
    }
  }, [analysis]);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [messages, thinking]);

  function send(question) {
    const text = (question ?? input).trim();
    if (!text || thinking) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setThinking(true);

    // No standalone chat endpoint exists on the backend yet — see
    // src/api/client.js. Until one does, the assistant answers from
    // the data already returned by /live-analysis rather than
    // fabricating a network call.
    setTimeout(() => {
      const answer =
        buildLocalAnswer(text, analysis) ||
        (hasAnalyzed
          ? "I can currently answer questions about the risk level, weather, nearby cyclones and forecast from your last analysis. A fully conversational assistant needs a dedicated chat endpoint on the backend."
          : "Run an analysis first so I have live data to answer from.");
      setMessages((prev) => [...prev, { role: "ai", text: answer }]);
      setThinking(false);
    }, 550 + Math.random() * 400);
  }

  return (
    <section className="card ai-section" id="ai">
      <div className="card-label">ARTIFICIAL INTELLIGENCE</div>
      <h2>AI Assistant</h2>
      <p style={{ color: "var(--text-secondary)", fontSize: 13.5, marginTop: 8, marginBottom: 18 }}>
        Live cyclone data combined with RAG knowledge and the local model explains the current
        situation and answers follow-up questions.
      </p>

      <div className="ai-chat">
        {messages.length === 0 && (
          <div className="empty-state" style={{ padding: "20px 10px" }}>
            <p>Run an analysis, then ask the assistant about the results.</p>
          </div>
        )}

        {messages.length > 0 && (
          <div className="chat-log" ref={logRef}>
            {messages.map((message, index) => (
              <div className={`chat-message ${message.role}`} key={index}>
                <div className="chat-avatar">{message.role === "ai" ? "AI" : "YOU"}</div>
                <div className="chat-bubble">
                  {message.role === "ai" && <span className="chat-label">CYCLONE AI</span>}
                  <p>{message.text}</p>
                </div>
              </div>
            ))}

            {thinking && (
              <div className="chat-message ai">
                <div className="chat-avatar">AI</div>
                <div className="chat-bubble">
                  <span className="chat-label">CYCLONE AI</span>
                  <div className="typing-dots">
                    <span /><span /><span />
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="suggested-questions">
          {SUGGESTED_QUESTIONS.map((question) => (
            <button key={question} onClick={() => send(question)} disabled={thinking}>
              {question}
            </button>
          ))}
        </div>

        <div className="chat-input">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && send()}
            placeholder="Ask about the cyclone…"
            disabled={thinking}
          />
          <button onClick={() => send()} disabled={thinking || !input.trim()} aria-label="Send message">
            →
          </button>
        </div>
        <p className="chat-hint">Answers are drawn from your latest analysis, not a live model call per message.</p>
      </div>
    </section>
  );
}

export default AIAssistant;
