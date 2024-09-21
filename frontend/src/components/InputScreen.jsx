import React from "react";
import Navbar from "./Navbar";

const Experience = ({ handleFileUpload }) => {
  return (
    <div className="flex flex-col min-h-screen w-screen items-center bg-[#1E1E1E] text-white">
      <Navbar />
      <img src="experience_hero.svg" className="w-screen h-auto" alt="Hero" />
      <main className="flex-grow flex flex-col items-center justify-center p-4 bg-[#1E1E1E]">
        <div className="w-11/12 max-w-8xl">
          <div className="flex justify-between items-start mb-8">
            <div>
              <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-pink-500 to-purple-500 text-transparent bg-clip-text">
                AUDIO-VISUAL EXPERIENCE
              </h1>
              <h2 className="text-xl text-white">For immersive storytelling</h2>
            </div>
            <div className="text-white text-left">
              <p>
                1. Select a file from your computer (.docx, .pdf, .txt
                supported)
              </p>
              <p>2. Click on Start Conversion</p>
            </div>
          </div>

          <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 mb-6 flex flex-col items-center justify-center">
            <svg
              className="w-12 h-12 mb-4 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              ></path>
            </svg>
            <p className="text-xl font-semibold mb-2 text-white">
              Upload a File
            </p>
            <p className="text-sm text-gray-400 mb-4">
              .docx, .pdf, .txt supported
            </p>
            <label className="px-4 py-2 bg-white text-black rounded-full cursor-pointer hover:bg-gray-200 transition duration-300">
              Choose a File
              <input
                type="file"
                className="hidden"
                onChange={handleFileUpload}
                accept=".pdf,.docx,.doc,.txt"
              />
            </label>
          </div>

          <button
            className="w-full py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-full font-semibold hover:from-pink-600 hover:to-purple-600 transition duration-300"
            onClick={() => {
              /* Handle conversion start */
            }}
          >
            Start Conversion
          </button>
        </div>
      </main>
    </div>
  );
};

export default Experience;
