import { useState } from "react";
import { Input, Button, Card, CardBody } from "@heroui/react";

type InitFormData = {
  players: string[];
  smallBlind: number;
  bigBlind: number;
  buyIn: number;
};

type InitFormProps = {
  onSubmit?: (data: InitFormData) => void;
};

export default function InitForm({ onSubmit }: InitFormProps) {
  const [playersRaw, setPlayersRaw] = useState("");
  const [smallBlind, setSmallBlind] = useState<number>(0);
  const [bigBlind, setBigBlind] = useState<number>(0);
  const [buyIn, setBuyIn] = useState<number>(0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const players = playersRaw
      .split(",")
      .map((p) => p.trim())
      .filter((p) => p.length > 0);

    const data: InitFormData = {
      players,
      smallBlind,
      bigBlind,
      buyIn,
    };

    onSubmit?.(data);
  };

  return (
    <Card className="mx-auto max-w-md">
      <CardBody>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input
            label="Player names"
            placeholder="Alice, Bob, Charlie"
            value={playersRaw}
            onChange={(e: any) => setPlayersRaw(e.target.value)}
            description="Comma separated list"
            isRequired
          />

          <Input
            label="Small Blind"
            type="number"
            value={smallBlind.toString()}
            onChange={(e: any) => setSmallBlind(Number(e.target.value))}
            isRequired
          />

          <Input
            label="Big Blind"
            type="number"
            value={bigBlind.toString()}
            onChange={(e: any) => setBigBlind(Number(e.target.value))}
            isRequired
          />

          <Input
            label="Buy In"
            type="number"
            value={buyIn.toString()}
            onChange={(e: any) => setBuyIn(Number(e.target.value))}
            isRequired
          />

          <Button color="primary" type="submit">
            Start Game
          </Button>
        </form>
      </CardBody>
    </Card>
  );
}
