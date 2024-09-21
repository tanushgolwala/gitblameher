import React, { useState, useEffect, useRef } from "react";
import { PlayIcon, PauseIcon, ChevronLeftIcon, ChevronRightIcon, DownloadIcon } from "lucide-react";

const SceneDisplay = ({
  imageSrc,
  summary,
  audioSrc,
  onPrevious,
  onNext,
  sceneCount,
  totalScenes,
  isVideo = false
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);
  const videoRef = useRef(null);

  const togglePlay = () => {
    const mediaElement = isVideo ? videoRef.current : audioRef.current;
    if (isPlaying) {
      mediaElement.pause();
    } else {
      mediaElement.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleTimeUpdate = () => {
    const mediaElement = isVideo ? videoRef.current : audioRef.current;
    const progress = (mediaElement.currentTime / mediaElement.duration) * 100;
    setProgress(progress);
  };

  const handleSliderChange = (e) => {
    const mediaElement = isVideo ? videoRef.current : audioRef.current;
    const time = (duration / 100) * e.target.value;
    mediaElement.currentTime = time;
    setProgress(e.target.value);
  };

  useEffect(() => {
    const mediaElement = isVideo ? videoRef.current : audioRef.current;
    const handleEnded = () => setIsPlaying(false);
    const handleLoadedMetadata = () => setDuration(mediaElement.duration);

    mediaElement.addEventListener("ended", handleEnded);
    mediaElement.addEventListener("loadedmetadata", handleLoadedMetadata);
    mediaElement.addEventListener("timeupdate", handleTimeUpdate);

    return () => {
      mediaElement.removeEventListener("ended", handleEnded);
      mediaElement.removeEventListener("loadedmetadata", handleLoadedMetadata);
      mediaElement.removeEventListener("timeupdate", handleTimeUpdate);
    };
  }, [isVideo]);

  return (
    <div className="max-w-5xl mx-auto bg-gray-100 rounded-xl shadow-lg overflow-hidden">
      <div className="relative" style={{ paddingBottom: "56.25%" }}>
        {isVideo ? (
          <video
            ref={videoRef}
            className="absolute top-0 left-0 w-full h-full object-cover"
            src={imageSrc}
          />
        ) : (
          <img
            className="absolute top-0 left-0 w-full h-full object-cover"
            src={imageSrc}
            alt="Scene"
          />
        )}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
          <p className="text-white text-lg font-semibold">{summary}</p>
        </div>
      </div>
      <div className="p-4 flex flex-col bg-white">
        {isVideo && (
          <input
            type="range"
            min="0"
            max="100"
            value={progress}
            onChange={handleSliderChange}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer mb-4"
          />
        )}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={togglePlay}
              className="flex items-center justify-center w-10 h-10 rounded-full bg-blue-500 text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              {isPlaying ? (
                <PauseIcon className="h-5 w-5" />
              ) : (
                <PlayIcon className="h-5 w-5" />
              )}
            </button>
            {!isVideo && (
              <div>
                <p className="text-sm font-medium text-gray-900">Scene {sceneCount}</p>
                <p className="text-xs text-gray-500">{isPlaying ? "Playing" : "Paused"}</p>
              </div>
            )}
          </div>
          {!isVideo && (
            <div className="flex items-center space-x-2">
              <button
                onClick={onPrevious}
                className="p-1 rounded-full bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              >
                <ChevronLeftIcon className="h-6 w-6 text-gray-600" />
              </button>
              <button
                onClick={onNext}
                className="p-1 rounded-full bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              >
                <ChevronRightIcon className="h-6 w-6 text-gray-600" />
              </button>
            </div>
          )}
          <button className="flex items-center text-blue-500 hover:text-blue-600">
            <DownloadIcon className="h-5 w-5 mr-1" />
            <span className="text-sm font-medium">Download</span>
          </button>
        </div>
      </div>
      {!isVideo && <audio ref={audioRef} src={audioSrc} className="hidden" />}
    </div>
  );
};

export default SceneDisplay;