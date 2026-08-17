import "./Reports.css";

function Reports() {

    const reportHistory = [
        {
            id: 1,
            name: "Benchmark_Report.pdf",
            date: "01 Jul 2026"
        },
        {
            id: 2,
            name: "Attack_Logs.csv",
            date: "01 Jul 2026"
        },
        {
            id: 3,
            name: "Performance_Report.pdf",
            date: "30 Jun 2026"
        }
    ];

    return (

        <div className="reports-container">

            <h1>📄 Reports Center</h1>

            <div className="button-container">

                <button>📄 Generate PDF Report</button>

                <button>📊 Export CSV Logs</button>

                <button>📈 Benchmark Report</button>

            </div>

            <div className="history">

                <h2>Recent Reports</h2>

                <table>

                    <thead>

                        <tr>
                            <th>ID</th>
                            <th>Report Name</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>

                    </thead>

                    <tbody>

                        {reportHistory.map((report) => (

                            <tr key={report.id}>

                                <td>{report.id}</td>

                                <td>{report.name}</td>

                                <td>{report.date}</td>

                                <td>✅ Ready</td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>

    );
}

export default Reports;