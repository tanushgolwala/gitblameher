import React from "react";

const Navbar = () => {
    return (
        <nav className="w-[70vw] h-[7vh] z-10 bg-white bg-opacity-50 backdrop-blur-md rounded-xl flex items-center justify-between absolute mt-5 shadow-lg transition-all duration-300 ease-in-out hover:bg-opacity-70">
            <ul className="flex w-full justify-between items-center text-black mx-5">
                <h1 className="text-black text-2xl transition-transform duration-300 ease-in-out hover:scale-105 hover:cursor-default">
                    Story<span className="font-bold italic">Scape</span>
                </h1>
                <div className="flex items-center space-x-6">
                    <NavItem>Home</NavItem>
                    <NavItem>Services</NavItem>
                    <NavItem>Kids Mode</NavItem>
                    <button className="bg-gradient-to-r from-[#f97187] to-[#a98af7] text-white py-2 px-8 rounded-lg transition-all duration-300 ease-in-out hover:bg-[#1e4571] hover:shadow-md">
                        Login
                    </button>
                </div>
            </ul>
        </nav>
    );
};

const NavItem = ({ children }) => (
    <li className="relative group">
        <a className="cursor-pointer transition-colors duration-300 ease-in-out hover:bg-gradient-to-r hover:from-[#f97187] hover:to-[#a98af7] hover:text-transparent hover:bg-clip-text">
            {children}
        </a>
        <span className="absolute bottom-0 left-0 w-0 h-0.5 hover:bg-gradient-to-r hover:from-[#f97187] hover:to-[#a98af7] transition-all duration-300 ease-in-out group-hover:w-full"></span>
    </li>
);

export default Navbar;