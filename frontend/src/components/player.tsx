import { useGameData } from "@/contexts/game_data_context";
import Action from "./action";
import { BigBlind, SmallBlind } from "./blinds";
import CurrPlayerIcon from "./curr_player_icon";
import Hole from "./hole";
import FormatAction from "./action";
import Equity from "./equity";

type PlayerProps = {
  pos: string;
};

export default function Player({ pos }: PlayerProps) {
  const { gameData, setGameData } = useGameData();

  const name: string = gameData.positions.players[pos];
  const holeCards: string[] = gameData.cards.holes[pos];
  const equity: number = gameData.equities[pos];
  const stack: number = gameData.state.stacks[pos];
  const lastAction: string = gameData.state.last_actions[pos];
  const isSB = gameData.positions.small_blind_pos == Number(pos);
  const isBB = gameData.positions.big_blind_pos == Number(pos);
  const isCurr = gameData.state.curr_player == pos;

  return (
    <div className="flex flex-col -ml-30 w-72">
      <div className="-z-10 fixed ml-4">
        <Hole cards={holeCards} />
      </div>
      <span className="flex ml-48 h-10">
        <Equity equity={equity} />
        {isSB && <SmallBlind />}
        {isBB && <BigBlind />}
      </span>
      <div className="border-1 border-stone-200 rounded-lg overflow-hidden">
        <span className="flex justify-between items-center bg-stone-800 px-4 py-2 text-white uppercase">
          <p>{name}</p>
          {isCurr && <CurrPlayerIcon />}
        </span>
        <div className="flex justify-between bg-stone-600 px-4 py-2">
          <p className="text-stone-400">Stack</p>
          <p className="text-white">${stack}</p>
        </div>
        <div className="flex justify-between bg-stone-600 px-4 py-2">
          <p className="text-stone-400">Last Action</p>
          <p className="text-white uppercase">{FormatAction(lastAction)}</p>
        </div>
      </div>
    </div>
  );
}
