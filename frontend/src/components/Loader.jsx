export default function Loader() {
  return (
    <section className="w-screen h-screen flex flex-col justify-center items-center bg-[#1E1E1E]">
      <div className="">STORYSCAPE</div>
      <h1 className="absolute top-0 left-0 p-4 text-white font-bold text-2xl transition-transform duration-300 ease-in-out hover:scale-105 hover:cursor-default">
        Story<span className="font-bold italic">Scape</span>
      </h1>
      <img src="clouds-spinner.gif" alt="Loading..." />
      <h1 className="text-5xl font-bold m-2 bg-gradient-to-r from-pink-500 to-purple-500 text-transparent bg-clip-text">
        Your text is being converted...
      </h1>
    </section>
  );
}
