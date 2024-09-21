import { useState, useEffect, useRef } from "react";
import {
  PlayIcon,
  PauseIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/react/solid";

const SceneDisplay = ({
  imageSrc,
  summary,
  audioSrc,
  onPrevious,
  onNext,
  sceneCount,
  totalScenes,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  const togglePlay = () => {
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  useEffect(() => {
    const audioElement = audioRef.current;
    const handleEnded = () => setIsPlaying(false);
    audioElement.addEventListener("ended", handleEnded);
    return () => {
      audioElement.removeEventListener("ended", handleEnded);
    };
  }, []);

  return (
    <div className="max-w-5xl mx-auto bg-black rounded-xl shadow-lg overflow-hidden">
      <div className="relative" style={{ paddingBottom: "56.25%" }}>
        {" "}
        {/* 16:9 aspect ratio */}
        <img
          className="absolute top-0 left-0 w-full h-full object-cover"
          src={imageSrc}
          alt="Scene"
        />
        <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-30 flex items-center justify-between px-4">
          <button
            onClick={() => {
              setIsPlaying(false);
              onPrevious();
            }}
            className="bg-white bg-opacity-50 hover:bg-opacity-75 rounded-full p-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white"
          >
            <ChevronLeftIcon className="h-8 w-8 text-gray-800" />
          </button>
          <button
            onClick={() => {
              setIsPlaying(false);
              onNext();
            }}
            className="bg-white bg-opacity-50 hover:bg-opacity-75 rounded-full p-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white"
          >
            <ChevronRightIcon className="h-8 w-8 text-gray-800" />
          </button>
        </div>
      </div>
      <div className="p-6">
        <div className="uppercase tracking-wide text-sm text-indigo-500 font-semibold mb-2">
          Scene {`${sceneCount} of ${totalScenes}`}
        </div>
        <p className="text-gray-500 text-sm mb-4">{summary}</p>
        <div className="flex items-center">
          <button
            onClick={togglePlay}
            className="flex items-center justify-center w-12 h-12 rounded-full bg-indigo-500 text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {isPlaying ? (
              <PauseIcon className="h-6 w-6" aria-hidden="true" />
            ) : (
              <PlayIcon className="h-6 w-6" aria-hidden="true" />
            )}
          </button>
          <span className="ml-3 text-sm text-gray-500">
            {isPlaying ? "Playing" : "Paused"}
          </span>
          <audio ref={audioRef} src={audioSrc} loop className="hidden" />
        </div>
      </div>
    </div>
  );
};

export default SceneDisplay;
