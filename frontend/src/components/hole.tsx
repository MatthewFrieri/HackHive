import Card from "./card"

type HoleProps = {
    cards: string[]
}

export default function Hole({ cards }: HoleProps) {

    return (
        <div className="flex gap-x-2">
            {cards.map((card, index) => <Card key={index} card={card} width={80}/>)}
        </div>
    )
}
