import { useGameData } from "@/contexts/game_data_context";
import Player from "./player";
import Pot from "./pot";
import Board from "./board";
import { useEffect, useState } from "react";

export default function Table() {
  const { gameData } = useGameData();

  const positions: string[] = Object.keys(gameData.positions.players);
  const pot: number = gameData.state.pot;
  const board_cards: string[] = gameData.cards.board;

  // Rectangle dimensions
  const [screenWidth, setScreenWidth] = useState<number>(window.innerWidth);

  const cx = screenWidth / 2;
  const cy = 350;
  const a = 500;
  const b = 250;

  // Update centerX on window resize
  useEffect(() => {
    const handleResize = () => setScreenWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="relative flex flex-col pt-20">
      <div className="flex justify-center mb-20">
        <Board cards={board_cards} />
      </div>
      <div className="flex justify-center">
        <Pot pot={pot} />
      </div>
      {positions.map((k, i) => {
        // Arc from left (π) to right (0)
        const thetaStart = Math.PI;
        const thetaEnd = 0;
        const theta =
          thetaStart +
          (thetaEnd - thetaStart) *
            ((positions.length - i - 1) / (positions.length - 1));

        // Elliptical coordinates
        const x = cx + a * Math.cos(theta);
        const y = cy + b * Math.sin(theta);

        return (
          <div
            key={k}
            className="absolute"
            style={{
              left: x,
              top: y,
            }}
          >
            <Player pos={k} />
          </div>
        );
      })}
    </div>
  );
}
