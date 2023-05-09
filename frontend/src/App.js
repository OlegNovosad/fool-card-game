import { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';
import Card from './Card';

const socket = io("http://localhost:5000");

function App() {
  const [playerCards, setPlayerCards] = useState([]);
  const [opponentCards, setOpponentCards] = useState([]);
  const [tableCards, setTableCards] = useState([]);

  useEffect(() => {
    socket.on("connected", (message) => {
      console.log(message);
    });

    socket.on("disconnected", (message) => {
      console.log(message);
    });

    socket.on("game-state-changed", (message) => {
      console.log(message);
      const playerCards = message["players"][0]["cards"];
      const opponentCards = message["players"][1]["cards"];
      const table = message["table"];
      setPlayerCards(playerCards);
      setTableCards(table);
      setOpponentCards(opponentCards);
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
          {
            tableCards.map((card) => <Card key={card["suit"] + card["rank"]} card={card} />)
          }
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
