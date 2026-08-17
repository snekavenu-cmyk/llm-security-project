import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import AttackSimulator from "./pages/AttackSimulator";
import Analytics from "./pages/Analytics";
import LiveLogs from "./pages/LiveLogs";
import DefensePipeline from "./pages/DefensePipeline";
import Reports from "./pages/Reports";
import AdminPanel from "./pages/AdminPanel";

function App() {

  return (
    <BrowserRouter>
    <Navbar />

<div className="app-container">

    <Sidebar />

    <div className="page-content">

      <Routes>

        <Route
         path="/"
          element={<Home />}
           />

        <Route
          path="/attack"
          element={<AttackSimulator />}
        />

        <Route
          path="/analytics"
          element={<Analytics />}
        />

        <Route
          path="/logs"
          element={<LiveLogs />}
        />

        <Route
          path="/defense"
          element={<DefensePipeline />}
        />

        <Route
          path="/reports"
          element={<Reports />}
        />

        <Route
          path="/admin"
          element={<AdminPanel />}
        />

      </Routes>
    </div>
  </div>

    </BrowserRouter>
  );
}

export default App;