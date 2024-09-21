import React, { useState } from "react";
import SceneDisplay from "./components/Scenedisplay";
import InputScreen from "./components/InputScreen";
import Loader from "./components/Loader";

function Experience() {
  const [scenes, setScenes] = useState([]);
  const [currentScene, setCurrentScene] = useState(0);
  const [isFileProcessed, setIsFileProcessed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/create-story-from-file",
        {
          method: "POST",
          body: formData,
          headers: {
            // Remove the Content-Type header to let the browser set it automatically with the correct boundary
          },
        }
      );

      if (!response.ok) {
        throw new Error("File processing failed");
      }

      const data = await response.json();
      setIsLoading(false);
      setIsFileProcessed(true);

      // Load the scenes based on the returned scene count
      await loadScenes(data.sceneCount);
    } catch (error) {
      console.error("Error processing file:", error);
      setIsLoading(false);
    }
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
    return <Loader />;
  }

  if (!isFileProcessed) {
    return <InputScreen handleFileUpload={handleFileUpload} />;
  }

  if (scenes.length === 0) {
    return <div>Loading scenes...</div>;
  }

  return (
    <div className="p-0 h-dvh w-[100vw] bg-[#cbc2aa] bg-opacity-60 flex justify-center items-center">
      <SceneDisplay
        {...scenes[currentScene]}
        onPrevious={handlePrevious}
        onNext={handleNext}
        sceneCount={currentScene + 1}
        totalScenes={scenes.length}
      />
    </div>
  );
}

export default Experience;
