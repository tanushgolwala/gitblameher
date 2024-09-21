import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Experience from "./Experience";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<h1>hello</h1>} />
          <Route path="/experience" element={<Experience />} />
          <Route path="/about" element={<h1>hello</h1>} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
