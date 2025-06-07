import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { MonitorPage } from "./pages/MonitorPage";
import ResultPage from "./pages/SummaryPage";

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