import { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';
import Card from './Card';

const socket = io("http://localhost:5000");

function App() {
  const [playerCards, setPlayerCards] = useState([]);
  const [opponentCards, setOpponentCards] = useState([]);
  const [tableCards, setTableCards] = useState([]);
  const [discardPile, setDiscardPile] = useState([]);
  const [deck, setDeck] = useState({cards: []});
  const [trumpCard, setTrumpCard] = useState();

  useEffect(() => {
    socket.on("connected", (_) => {
      socket.emit("auth", {
        "connected": true,
        "name": "Oleg"
      });
    });

    socket.on("disconnected", (_) => {
      socket.emit("auth", {
        "connected": false,
        "name": "Oleg"
      });
    });

    socket.on("game-state-changed", (message) => {
      console.log(message);
      const playerCards = message["players"][0]["cards"];
      const opponentCards = message["players"][1]["cards"];
      const table = message["table"];
      const discardPile = message["discard_pile"];
      const deck = message["deck"];
      const trumpCard = message["trump_card"];
      setPlayerCards(playerCards);
      setTableCards(table);
      setOpponentCards(opponentCards);
      setDiscardPile(discardPile);
      setDeck(deck);
      setTrumpCard(trumpCard);
    });
  })

  const playCard = (card) => {
    socket.emit("play-card", {
      suit: card["suit"],
      rank: card["rank"]
    });
  }

  return (
    <div className="background container">
        <div className="opponent row">
          {
            opponentCards.map((card) => <Card key={card["suit"] + card["rank"]} card={card} hidden={true} />)
          }
        </div>
        <div className="table row">
          <div className="discard-pile">

          </div>
          <div className="table-cards">
            {
              tableCards.map((card) => <Card key={card["suit"] + card["rank"]} card={card} />)
            }
          </div>
          <div className="deck">
            <Card card={trumpCard} />

            {
              deck["cards"].map((card) =>  <Card key={card["suit"] + card["rank"]} card={card} hidden={true} />)
            }
          </div>
        </div>
        <div className="me row">
          {
            playerCards.map((card) => <Card key={card["suit"] + card["rank"]} card={card} onSelect={() => playCard(card)} />)
          }
        </div>
    </div>
  );
}

export default App;
