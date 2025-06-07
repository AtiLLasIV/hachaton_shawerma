import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { MonitorPage } from "./pages/MonitorPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/monitor" element={<MonitorPage />} />
      </Routes>
    </Router>
  );
}

export default App;