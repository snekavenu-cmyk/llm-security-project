import "./Analytics.css";

function Analytics() {

    return (

        <div className="analytics-container">

            <h1>📊 Analytics Dashboard</h1>

            <div className="metric-grid">

                <div className="metric-card">
                    <h2>Total Attacks</h2>
                    <p>500</p>
                </div>

                <div className="metric-card">
                    <h2>Blocked</h2>
                    <p>98</p>
                </div>

                <div className="metric-card">
                    <h2>Defense Accuracy</h2>
                    <p>91%</p>
                </div>

                <div className="metric-card">
                    <h2>Average Latency</h2>
                    <p>0.18 s</p>
                </div>

            </div>

            <div className="chart-grid">

                <div className="chart-card">

                    <h2>📈 Attack Trend</h2>

                    <div className="chart-placeholder">
                        Chart will appear here
                    </div>

                </div>

                <div className="chart-card">

                    <h2>⚡ Latency</h2>

                    <div className="chart-placeholder">
                        Chart will appear here
                    </div>

                </div>

                <div className="chart-card">

                    <h2>🎯 Risk Distribution</h2>

                    <div className="chart-placeholder">
                        Chart will appear here
                    </div>

                </div>

                <div className="chart-card">

                    <h2>🛡 Defense Performance</h2>

                    <div className="chart-placeholder">
                        Chart will appear here
                    </div>

                </div>

            </div>

        </div>

    );
}

export default Analytics;