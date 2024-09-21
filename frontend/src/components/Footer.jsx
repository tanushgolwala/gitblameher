import React from 'react';
import { Facebook, Instagram, Linkedin, Twitter } from 'lucide-react';

const Footer = () => {
    return (
        // <footer className="flex w-full justify-between items-end p-3 bg-gradient-to-r from-[#f97187] to-[#a98af7] mt-10">
        //     <div className="flex justify-center items-center">
        //         <h1 className="text-4xl font-normal text-black">
        //             Story<span className="font-bold italic">Scape</span>
        //         </h1>
        //         <h6 className="ml-[2vw] text-sm text-black items-center">Made by <span className='font-bold italic'>@gitblameher</span></h6>
        //     </div>
        //     <div className="flex w-[30vw] items-center justify-between space-x-2">
        //         <Facebook size={20} color="black" />
        //         <Instagram size={20} color="black" />
        //         <Linkedin size={20} color="black" />
        //         <Twitter size={20} color="black" />
        //     </div>
        //     <div className="text-black text-start">
        //         <h3 className="font-bold">Names</h3>
        //         <ul className="text-sm">
        //             <li>Manah Shah</li>
        //             <li>Ansh Mehta</li>
        //             <li>Tanush Golwala</li>
        //             <li>Sameer Palkar</li>
        //         </ul>
        //     </div>
        // </footer>
        <img src="/footer.svg" alt="Footer" className='w-full mt-10' />
    );
};

export default Footer;