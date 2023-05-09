import { useEffect, useState } from 'react';
import './App.css';
import io from 'socket.io-client';

const socket = io("http://localhost:5000");

function App() {
  const [playerCards, setPlayerCards] = useState([{"suit": "spades", "rank": 14}, {"suit": "diamonds", "rank": 2}, {"suit": "hearts", "rank": 13}, {"suit": "hearts", "rank": 8}, {"suit": "diamonds", "rank": 11}, {"suit": "diamonds", "rank": 5}])
  const [opponentCards, setOpponentCards] = useState([{"suit": "diamonds", "rank": 13}, {"suit": "hearts", "rank": 11}, {"suit": "spades", "rank": 8}, {"suit": "diamonds", "rank": 2}, {"suit": "hearts", "rank": 6}, {"suit": "diamonds", "rank": 12}])
  const [tableCards, setTableCards] = useState([]);

  useEffect(() => {
    socket.on("connected", (message) => {
      console.log(message);
    });

    socket.on("disconnected", (message) => {
      console.log(message);
    });

    socket.on("game-started", (message) => {
      const data = JSON.parse(message["player_cards"]);
      console.log(data);
      setPlayerCards(data);
    });
  })

  const playCard = (card) => {
    socket.emit("play-card", {
      card: card
    });
  }

  return (
    <div className="background container">
        <div className="opponent row">
          {
            opponentCards.map((card) => {
              return <img className="card" src={require("./assets/images/cards/default/SHKURA.png")} alt="card" />
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
                return <img className="card" src={require("./assets/images/cards/default/" + imgName)} alt="card" />
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
                return <img onClick={() => playCard(card)} className="card" src={require("./assets/images/cards/default/" + imgName)} alt="card" />
              })
            }
        </div>
    </div>
  );
}

export default App;
