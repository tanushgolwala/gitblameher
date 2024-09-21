import { useEffect, useState } from "react";
import "./App.css";
import SceneDisplay from "./components/Scenedisplay";

function App() {
  const [scenes, setScenes] = useState([]);
  const [currentScene, setCurrentScene] = useState(0);

  useEffect(() => {
    const loadScenes = async () => {
      const sceneData = [];
      const sceneCount = 9; // Update this based on the number of scenes you have

      for (let i = 1; i <= sceneCount; i++) {
        const imageSrc = `/image_outputs/scene_${i}.png`; // Updated path
        const audioSrc = `/audio_outputs/scene_${i}.wav`; // Updated path
        const summarySrc = `/summary_outputs/scene_${i}.txt`;

        // Fetch the summary text from the .txt file
        const response = await fetch(summarySrc);
        const summary = await response.text();

        sceneData.push({
          imageSrc,
          summary,
          audioSrc,
        });
      }

      setScenes(sceneData);
    };

    loadScenes();
  }, []);

  const handlePrevious = () => {
    setCurrentScene((prev) => (prev > 0 ? prev - 1 : scenes.length - 1));
  };

  const handleNext = () => {
    setCurrentScene((prev) => (prev < scenes.length - 1 ? prev + 1 : 0));
  };

  if (scenes.length === 0) {
    return <div>Loading scenes...</div>;
  }

  return (
    <div className="App p-4">
      <SceneDisplay
        {...scenes[currentScene]}
        onPrevious={handlePrevious}
        onNext={handleNext}
      />
    </div>
  );
}

export default App;
