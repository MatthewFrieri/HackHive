import { Route, Routes } from "react-router-dom";

import PreviewPage from "./pages/preview";
import { GameDataProvider } from "./contexts/game_data_context";
import InitGamePage from "./pages/init_game";

function App() {
  return (
    <GameDataProvider>
      <Routes>
        <Route element={<InitGamePage />} path="/" />
        <Route element={<PreviewPage />} path="/preview" />
      </Routes>
    </GameDataProvider>
  );
}

export default App;
