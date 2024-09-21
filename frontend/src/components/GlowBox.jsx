import React from "react";

const GlowBox = () => {
    const categories = [
        "Educational",
        "Children Stories",
        "Action/ Thriller",
        "Novels",
        "Fiction",
    ];
    return (
        <div className="relative p-1 w-[80vw] mx-auto flex mt-5">
            {/* Gradient border with glow effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-[#f97187] to-[#a98af7] rounded-3xl blur-[5px]"></div>

            {/* Main content */}
            <div className="relative flex gap-5 bg-[#1e1e1e] rounded-3xl p-6 md:p-8 overflow-hidden">
                <div className="flex flex-col justify-center items-center">
                    <h2 className="text-white text-2xl md:text-3xl font-bold mb-4">
                        Create amazing videos
                        <br />
                        across various categories
                    </h2>

                    {/* Categories */}
                    <div className="flex justify-center items-center flex-wrap gap-2 mb-6 mt-3">
                        {categories.map((category, index) => (
                            <div
                                key={index}
                                className="relative group my-1 mx-2"
                            >
                                <div className="absolute inset-0 bg-gradient-to-r from-[#f97187] to-[#a98af7] rounded-full blur-[2px] opacity-75 group-hover:opacity-100 group-hover:scale-105 transition-all duration-300"></div>
                                <span className="relative px-4 py-2 rounded-full text-sm bg-[#1e1e1e] text-white inline-block transition-all duration-300 group-hover:scale-105 w-[12vw] text-center">
                                    {category}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="relative flex justify-center items-center w-full aspect-video bg-[#1e1e1e] rounded-xl overflow-hidden">
                    <img
                        src="/landing_mobile.svg"
                        alt="Video scene"
                        className="w-full object-cover"
                    />
                </div>
            </div>
        </div>
    );
};

export default GlowBox;
