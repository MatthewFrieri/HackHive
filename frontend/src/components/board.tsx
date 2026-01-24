import Card from "./card"

type BoardProps = {
    cards: string[]
}

export default function Board({ cards }: BoardProps) {
    cards.length = 5
    cards = [...cards]

    return (
        <div className="flex gap-x-5">
            {cards.map((card, index) => <Card key={index} card={card} width={100}/>)}
        </div>
    )
}
