import { useState } from "react";
import api from "../services/api";
import "./AttackSimulator.css";

function AttackSimulator() {

  const [attackType, setAttackType] = useState("Prompt Injection");
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const runAttack = async () => {

    if (!prompt.trim()) {
      setResponse("Please enter a prompt.");
      return;
    }

    setResponse("Running attack...");

    try {

      const result = await api.post(
        "/llm",
        {
          prompt: prompt,
          attack_type: attackType
        },
        {
          headers: {
            "x-api-key": "llm"
          }
        }
      );

      setResponse(
        JSON.stringify(result.data, null, 2)
      );

    } catch (error) {

      console.error("Backend Error:", error);

      if (error.response) {

        setResponse(
          `Backend Error ${error.response.status}: ${
            error.response.data?.detail ||
            "Request failed"
          }`
        );

      } else {

        setResponse(
          "Unable to connect to backend. Make sure the FastAPI server is running on port 8000."
        );

      }
    }
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
          <pre>{response || "Response will appear here..."}</pre>
        </div>

      </div>

    </div>
  );
}

export default AttackSimulator;