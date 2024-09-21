import React from 'react';
import { Facebook, Instagram, Linkedin, Twitter } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="flex justify-between items-end p-3 bg-gradient-to-r from-pink-400 to-purple-400">
            <div className="flex">
                <h1 className="text-4xl font-normal text-black">
                    Story<span className="font-bold italic">Scape</span>
                </h1>
                <h6 className="ml-[2vw] text-sm text-black items-end">Made by <span className='font-bold italic'>@gitblameher</span></h6>
            </div>
            <div className="flex items-center space-x-2">
                <Facebook size={20} color="black" />
                <Instagram size={20} color="black" />
                <Linkedin size={20} color="black" />
                <Twitter size={20} color="black" />
            </div>
            <div className="text-black text-start">
                <h3 className="font-bold">Names</h3>
                <ul className="text-sm">
                    <li>Manah Shah</li>
                    <li>Ansh Mehta</li>
                    <li>Tanush Golwala</li>
                    <li>Sameer Palkar</li>
                </ul>
            </div>
        </footer>
    );
};

export default Footer;