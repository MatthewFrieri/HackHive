import { useGameData } from "@/contexts/game_data_context";

export default function GameMeta() {
  const { gameData, setGameData } = useGameData();

  const buy_in: number = gameData.meta.buy_in;
  const small_blind: number = gameData.meta.small_blind;
  const big_blind: number = gameData.meta.big_blind;

  return (
    <div className="text-stone-200 text-xl">
      <p>Buy In: ${buy_in}</p>
      <p>
        ${small_blind} SB / ${big_blind} BB
      </p>
    </div>
  );
}
