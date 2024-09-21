import React from "react";
import Navbar from "./components/Navbar";

const Landing = () => {
    return (
        <div className="w-[100vw] h-dvh flex flex-col items-center m-0 overflow-x-hidden">
            <Navbar />
            <div className="min-h-[100vh]">
                <img
                    src="/landing_image.svg"
                    alt="landing"
                    className="w-full rounded-b-3xl"
                />
                <div className="hero flex flex-row items-center justify-between w-full px-20">
                    <div className="heading mt-20">
                        <h1 className="font-bold text-5xl">
                            YOUR FAVOURITE STORIES
                        </h1>
                        <h1 className="font-semibold text-4xl text-[#295F98]">
                            JUST BECAME IMMERSIVE
                        </h1>
                    </div>
                    <div className="buttons">
                        <button className="bg-[#CDC2A5] text-white py-2 px-6 items-center rounded-lg transition-all duration-300 ease-in-out hover:shadow-md flex justify-between w-[12vw]">
                            Get Started
                            <p className="text-lg font-bold">&gt;</p>
                        </button>
                    </div>
                </div>
            </div>
            <h1 className="ml-20 self-start text-2xl">
                Turn your stories into a captivating{" "}
                <span className="font-semibold">Audio Visual Experience</span>
            </h1>
        </div>
    );
};

export default Landing;
