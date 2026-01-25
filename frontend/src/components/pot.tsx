type PotProps = {
  pot: number;
};

export default function Pot({ pot }: PotProps) {
  return (
    <div className="p-2 text-white text-xl text-center">
      <p>Pot:</p>
      <h1 className="text-shadow-[3px_3px_4px_rgba(0,0,0,0.5)] text-shadow-black font-bold text-8xl">
        ${pot}
      </h1>
    </div>
  );
}
