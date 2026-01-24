import { Route, Routes } from "react-router-dom";

import PreviewPage from "./pages/preview";
import { GameDataProvider } from "./contexts/game_data_context";

function App() {
  return (
    <GameDataProvider>
      <Routes>
        <Route element={<PreviewPage />} path="/" />
      </Routes>
    </GameDataProvider>
  );
}

export default App;
