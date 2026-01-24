import { createContext, useContext, useState, ReactNode } from "react";

type GameDataContextType = {
  gameData: any;
  setGameData: React.Dispatch<React.SetStateAction<any>>;
};

const GameDataContext = createContext<GameDataContextType | undefined>(undefined);

type GameDataProviderProps = {
  children: ReactNode;
};

export const GameDataProvider = ({ children }: GameDataProviderProps) => {
  const [gameData, setGameData] = useState<any>(undefined);

  return (
    <GameDataContext.Provider value={{ gameData, setGameData }}>
      {children}
    </GameDataContext.Provider>
  );
};

export const useGameData = () => {
  const context = useContext(GameDataContext);
  if (!context) {
    throw new Error("useGameData must be used within a GameDataProvider");
  }
  return context;
};
