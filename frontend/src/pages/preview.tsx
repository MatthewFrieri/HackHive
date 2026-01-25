import Table from "@/components/table";
import { useEffect } from "react";
import { getData } from "../api"
import { useGameData } from "@/contexts/game_data_context";

export default function PreviewPage() {
    const { gameData, setGameData } = useGameData();

    useEffect(() => {
        const fetchData = async () => {
        try {
            const data = await getData();
            setGameData(data);
        } catch (error) {
            console.error("Failed to fetch data:", error);
        }
        };

        fetchData();
    }, []);

    return (
        <>
            {gameData && <Table/>}
        </>
    )
}   
