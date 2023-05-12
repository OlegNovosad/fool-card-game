export default function Card(props) {
    if (!props || !props.card) {
        return;
    }

    let imgName = "";
    let suit = props.card["suit"];
    let rank = props.card["rank"];

    if (suit == "diamonds") {
        suit = "DZVUNA";
    } else if (suit == "clubs") {
        suit = "KRESTA";
    } else if (suit == "spades") {
        suit = "PIKA";
    } else if (suit == "hearts") {
        suit = "SERCE";
    }

    if (rank == 11) {
        rank = "VALET";
    } else if (rank == 12) {
        rank = "DAMA";
    } else if (rank == 13) {
        rank = "KOROL";
    } else if (rank == 14) {
        rank = "TUZ";
    }
    imgName += suit;
    imgName += rank;
    imgName += ".png";
    
    if (props.hidden) {
        return <img onClick={props.onSelect} className="card" src={require("./assets/images/cards/default/SHKURA.png")} alt="card" />
    } else {
        return <img onClick={props.onSelect} className="card" src={require("./assets/images/cards/default/" + imgName)} alt="card" />
    }
}