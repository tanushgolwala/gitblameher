import React, { useState } from "react";
import Navbar from "./Navbar"; 4
import SceneDisplay from "./Scenedisplay";
import Footer from "./Footer";

const Music = () => {
    const [currentScene, setCurrentScene] = useState(1);
    const totalScenes = 5; // Example total number of scenes

    const handlePrevious = () => {
        setCurrentScene(prev => Math.max(prev - 1, 1));
    };

    const handleNext = () => {
        setCurrentScene(prev => Math.min(prev + 1, totalScenes));
    };

    return (
        <div className="w-[100vw] h-dvh flex flex-col items-center m-0 overflow-x-hidden bg-[#1e1e1e] overflow-scroll">
            <Navbar />
            <div className="w-full max-w-5xl mt-[20vh]">
                <SceneDisplay
                    imageSrc="/path/to/your/image/or/video.jpg" // change placeholder
                    summary={`Julius Caesar and Queen Cleopatra lived happily ever after.`}
                    audioSrc="/path/to/your/audio.mp3"
                    onPrevious={handlePrevious}
                    onNext={handleNext}
                    sceneCount={currentScene}
                    totalScenes={totalScenes}
                    isVideo={false}
                />
            </div>
        </div>
    );
}

export default Music;