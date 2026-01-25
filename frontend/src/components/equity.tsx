type EquityProps = {
  equity: number;
};

export default function Equity({ equity }: EquityProps) {
  return (
    <div className="flex justify-center items-center bg-stone-100 mr-4 -mb-2 rounded-t-lg w-12 h-10 font-bold">
      {Math.round(equity)}%
    </div>
  );
}
