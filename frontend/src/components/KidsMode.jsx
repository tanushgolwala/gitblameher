import React from "react";

const KidsMode = () => {
    return (
        <div className="mt-10 flex flex-col justify-center items-center w-full">
            <h1 className="text-white text-5xl text-center">
                KIDS{" "}
                <span className="font-semibold text-5xl bg-gradient-to-r from-[#f97187] to-[#a98af7] text-transparent bg-clip-text">
                    MODE
                </span>
            </h1>
            <div className="flex w-full h-[40vh] gap-5 p-5 mt-5">
                <div className="w-full h-full relative rounded-2xl overflow-hidden">
                    <img
                        src="/kidsmode.svg"
                        alt="A/V Experience"
                        className="w-full z-0"
                    />
                    <div className="absolute z-10 top-10 left-10">
                        <h1 className="z-10 m-0 text-white text-4xl font-bold w-full text-left">
                            All Kids Content
                        </h1>
                        <h1 className="z-10 m-0 text-white text-3xl w-full text-left">
                            At One Place
                        </h1>
                        <button className="bg-[#d1f46f] px-4 py-2 rounded-lg mt-5 hover:scale-105 duration-300">Explore Kids Mode</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default KidsMode;
