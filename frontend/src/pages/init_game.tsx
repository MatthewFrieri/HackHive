import { useNavigate } from "react-router-dom";
import { startGame } from "@/api";
import InitForm from "@/components/init_form";

export default function InitGame() {
  const navigate = useNavigate();

  const handleSubmit = async (formData: any) => {
    try {
      await startGame(formData);
      navigate("/preview");
    } catch (err) {
      console.error("Failed to start game", err);
    }
  };

  return <InitForm onSubmit={handleSubmit} />;
}
