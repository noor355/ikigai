import JournalHistoryPage from "./pages/JournalHistoryPage";
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import DashboardPage from "./pages/DashboardPage";
import ChatPage from "./pages/ChatPage";
import JournalPage from "./pages/JournalPage";
import RecommendationsPage from "./pages/RecommendationsPage";
import TestsPage from "./pages/TestsPage";
import Layout from "./components/Layout";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  return (
    <Router>
      <Routes>
        {/* Public Login Page */}
        <Route path="/" element={!token ? <AuthPage setToken={setToken} /> : <Navigate to="/dashboard" />} />
        
        {/* Protected App Pages (Wrapped inside the new Layout) */}
        <Route element={token ? <Layout setToken={setToken} /> : <Navigate to="/" />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/journal" element={<JournalPage />} />
          <Route path="/history" element={<JournalHistoryPage />} />
          <Route path="/tests" element={<TestsPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;