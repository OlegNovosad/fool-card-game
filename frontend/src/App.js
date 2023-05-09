import { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';

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
            opponentCards.map((card) => {
              let suit = card["suit"];
              let rank = card["rank"];

              return <img key={suit + rank} className="card" src={require("./assets/images/cards/default/SHKURA.png")} alt="card" />
            })
          }
        </div>
        <div className="table row">
          {
              tableCards.map((card) => {
                let imgName = "";
                let suit = card["suit"];
                let rank = card["rank"];

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
                return <img key={suit + rank} className="card" src={require("./assets/images/cards/default/" + imgName)} alt="card" />
              })
            }
        </div>
        <div className="me row">
            {
              playerCards.map((card) => {
                let imgName = "";
                let suit = card["suit"];
                let rank = card["rank"];

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
                return <img key={suit + rank} onClick={() => playCard(card)} className="card" src={require("./assets/images/cards/default/" + imgName)} alt="card" />
              })
            }
        </div>
    </div>
  );
}

export default App;
