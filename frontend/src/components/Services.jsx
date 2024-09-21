import React from "react";

const Services = () => {
    return (
        <div className="mt-10 flex flex-col justify-center items-center w-full">
            <h1 className="text-white text-5xl text-center">
                OUR{" "}
                <span className="font-semibold text-5xl bg-gradient-to-r from-[#f97187] to-[#a98af7] text-transparent bg-clip-text">
                    SERVICES
                </span>
            </h1>
            <div className="flex w-full h-[40vh] gap-5 p-5 mt-5">
                <div className="w-1/2 h-full relative rounded-2xl overflow-hidden hover:scale-105 duration-300">
                    <img
                        src="/experience.svg"
                        alt="A/V Experience"
                        className="w-full z-0"
                    />
                    <h1 className="z-10 absolute bottom-10 text-white text-4xl font-bold w-full text-center">Audio-Visual Experience</h1>
                </div>
                <div className="w-1/2 h-full relative rounded-2xl overflow-hidden hover:scale-105 duration-300">
                    <img
                        src="/musicvideo.svg"
                        alt="A/V Experience"
                        className="w-full"
                    />
                    <h1 className="z-10 absolute bottom-10 text-white text-4xl font-bold w-full text-center">Music Video Generator</h1>
                </div>
            </div>
        </div>
    );
};

export default Services;
