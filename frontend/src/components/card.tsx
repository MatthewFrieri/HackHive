type CardProps = {
  card?: string;
  width: number;
};

export default function Card({ card, width }: CardProps) {
  return (
    <img
      src={`/cards/${card ?? "back"}.svg`}
      style={{ width }}
      className="drop-shadow-md"
    />
  );
}
