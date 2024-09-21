import React, { useEffect, useState } from "react";
import SceneDisplay from "./components/Scenedisplay";

function Experience() {
  const [scenes, setScenes] = useState([]);
  const [currentScene, setCurrentScene] = useState(0);
  const [isFileProcessed, setIsFileProcessed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);

    await simulateFileProcessing(file);

    setIsLoading(false);
    setIsFileProcessed(true);

    // After processing, load the scenes
    loadScenes(9);
  };

  const simulateFileProcessing = (file) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        console.log(`Processed file: ${file.name}`);
        resolve();
      }, 2000);
    });
  };

  const loadScenes = async (sceneCount) => {
    const sceneData = [];
    for (let i = 1; i <= sceneCount; i++) {
      const imageSrc = `/image_outputs/scene_${i}.png`;
      const audioSrc = `/audio_outputs/scene_${i}.wav`;
      const summarySrc = `/summary_outputs/scene_${i}.txt`;

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

  const handlePrevious = () => {
    setCurrentScene((prev) => (prev > 0 ? prev - 1 : scenes.length - 1));
  };

  const handleNext = () => {
    setCurrentScene((prev) => (prev < scenes.length - 1 ? prev + 1 : 0));
  };

  if (isLoading) {
    return <div>Processing file...</div>;
  }

  if (!isFileProcessed) {
    return (
      <div className="p-4">
        <h2 className="mb-4">Upload a file to begin</h2>
        <input
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileUpload}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-violet-50 file:text-violet-700
            hover:file:bg-violet-100"
        />
      </div>
    );
  }

  if (scenes.length === 0) {
    return <div>Loading scenes...</div>;
  }

  return (
    <div className="p-4">
      <SceneDisplay
        {...scenes[currentScene]}
        onPrevious={handlePrevious}
        onNext={handleNext}
      />
    </div>
  );
}

export default Experience;
