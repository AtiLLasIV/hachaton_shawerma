import React from 'react';
import ResultsPage from './pages/SummaryPage';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { MonitorPage } from "./pages/MonitorPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/monitor" element={<MonitorPage />} />
        <Route path="/summary" element={<ResultPage />} />
      </Routes>
    </Router>
  );
}
export default App;