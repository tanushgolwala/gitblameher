import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Experience from "./Experience";
import Landing from "./Landing";
import Music from "./components/Music";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/experience" element={<Experience />} />
          <Route path="/about" element={<h1>hello</h1>} />
          <Route path="/music" element={<Music />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
