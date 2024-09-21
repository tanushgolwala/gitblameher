import React from "react";
import Navbar from "./components/Navbar";

const Landing = () => {
    return (
        <div className="w-[100vw] h-dvh flex flex-col items-center m-0 overflow-x-hidden bg-[#1e1e1e]">
            <Navbar />
            <div className="min-h-[100vh]">
                <img
                    src="/landing_image.svg"
                    alt="landing"
                    className="w-full rounded-b-3xl"
                />
                <div className="hero flex flex-row items-center justify-between w-full px-20 pt-14 pb-5">
                    <div className="heading">
                        <h1 className="font-semibold text-white text-4xl">
                            YOUR FAVOURITE STORIES
                        </h1>
                        <h1 className="font-semibold text-5xl bg-gradient-to-r from-[#f97187] to-[#a98af7] text-transparent bg-clip-text">
                            JUST BECAME IMMERSIVE
                        </h1>
                    </div>
                    <div className="relative inline-block">
                        <div className="absolute inset-0 bg-gradient-to-r from-[#f97187] to-[#a98af7] rounded-full blur-[2px]"></div>
                        <button className="relative bg-[#1e1e1e] text-white py-2 px-6 rounded-full transition-all duration-300 ease-in-out hover:shadow-md flex justify-between items-center w-72">
                            <span className="text-lg">Get Started</span>
                            <span className="text-lg font-bold">&gt;</span>
                        </button>
                    </div>
                </div>
                <h1 className="ml-20 self-start text-2xl text-white">
                    Turn your stories into a captivating{" "}
                    <span className="font-semibold bg-gradient-to-r from-[#f97187] to-[#a98af7] text-transparent bg-clip-text">
                        Audio Visual Experience
                    </span>
                </h1>
            </div>
        </div>
    );
};

export default Landing;
