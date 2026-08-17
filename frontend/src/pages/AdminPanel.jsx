import "./AdminPanel.css";

function AdminPanel() {

    return (

        <div className="admin-container">

            <h1>👨‍💼 Admin Dashboard</h1>

            <div className="stats">

                <div className="stat-card">
                    <h2>Total Attacks</h2>
                    <p>120</p>
                </div>

                <div className="stat-card">
                    <h2>Blocked</h2>
                    <p>110</p>
                </div>

                <div className="stat-card">
                    <h2>Accuracy</h2>
                    <p>91%</p>
                </div>

                <div className="stat-card">
                    <h2>Latency</h2>
                    <p>0.18 s</p>
                </div>

            </div>

            <div className="dashboard-grid">

                <div className="panel">

                    <h2>🖥 System Health</h2>

                    <ul>

                        <li>🟢 LLM Engine</li>
                        <li>🟢 Attack Engine</li>
                        <li>🟢 Defense Pipeline</li>
                        <li>🟢 Benchmark Engine</li>
                        <li>🟢 SQLite Database</li>
                        <li>🟢 FastAPI Server</li>

                    </ul>

                </div>

                <div className="panel">

                    <h2>📋 Recent Activity</h2>

                    <p><strong>Last Attack:</strong> Prompt Injection</p>

                    <p><strong>Last Report:</strong> Benchmark_Report.pdf</p>

                    <p><strong>Last Login:</strong> Today 09:45 AM</p>

                    <p><strong>Current User:</strong> Admin</p>

                </div>

            </div>

            <div className="actions">

                <button>⚔ Run Attack</button>

                <button>📊 Analytics</button>

                <button>📄 Reports</button>

            </div>

        </div>

    );

}

export default AdminPanel;