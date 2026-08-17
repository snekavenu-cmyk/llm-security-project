import "./LiveLogs.css";

function LiveLogs() {

  const logs = [
    {
      id: 1,
      attack: "Prompt Injection",
      score: 95,
      blocked: "Yes",
      latency: "0.21 s",
      time: "09:30 AM"
    },
    {
      id: 2,
      attack: "Jailbreak",
      score: 88,
      blocked: "Yes",
      latency: "0.18 s",
      time: "09:35 AM"
    },
    {
      id: 3,
      attack: "Role Play",
      score: 60,
      blocked: "No",
      latency: "0.14 s",
      time: "09:40 AM"
    },
    {
      id: 4,
      attack: "Data Leakage",
      score: 98,
      blocked: "Yes",
      latency: "0.25 s",
      time: "09:45 AM"
    }
  ];

  return (

    <div className="logs-container">

      <h1>📋 Live Attack Logs</h1>

      <table>

        <thead>

          <tr>
            <th>ID</th>
            <th>Attack</th>
            <th>Risk Score</th>
            <th>Blocked</th>
            <th>Latency</th>
            <th>Time</th>
          </tr>

        </thead>

        <tbody>

          {logs.map((log) => (

            <tr key={log.id}>

              <td>{log.id}</td>

              <td>{log.attack}</td>

              <td>{log.score}</td>

              <td>{log.blocked}</td>

              <td>{log.latency}</td>

              <td>{log.time}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );
}

export default LiveLogs;