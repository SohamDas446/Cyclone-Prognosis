function AIChat() {
  return (
    <div className="ai-chat">

      <div className="ai-message">

        <div className="ai-avatar">
          AI
        </div>

        <div className="ai-message-content">

          <span className="ai-label">
            CYCLONE AI
          </span>

          <p>
            Based on the current cyclone observations,
            weather conditions and machine-learning
            forecast, the selected region currently
            has a moderate estimated risk.
          </p>

        </div>

      </div>


      <div className="chat-input">

        <input
          type="text"
          placeholder="Ask about the cyclone..."
        />

        <button>
          →
        </button>

      </div>

    </div>
  );
}

export default AIChat;