import { useState } from "react";
import "./AttackSimulator.css";

function AttackSimulator() {

  const [attackType, setAttackType] = useState("Prompt Injection");
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const runAttack = () => {
    setResponse("Backend not connected yet...");
  };

  return (
    <div className="attack-container">

      <h1>⚔ Attack Simulator</h1>

      <div className="attack-card">

        <label>Attack Type</label>

        <select
          value={attackType}
          onChange={(e) => setAttackType(e.target.value)}
        >
          <option>Prompt Injection</option>
          <option>Jailbreak</option>
          <option>Role Play Attack</option>
          <option>Data Leakage</option>
          <option>Instruction Override</option>
        </select>

        <label>Prompt</label>

        <textarea
          rows="8"
          placeholder="Enter malicious prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <button onClick={runAttack}>
          Run Attack
        </button>

      </div>

      <div className="result-card">

        <h2>LLM Response</h2>

        <div className="response-box">
          {response || "Response will appear here..."}
        </div>

      </div>

    </div>
  );
}

export default AttackSimulator;