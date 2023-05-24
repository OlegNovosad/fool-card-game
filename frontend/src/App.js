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
            {
              discardPile.map((card) => {                const angle = Math.floor(Math.random() * 360);
                const left = Math.floor(Math.random() * 50);
                const top = Math.floor(Math.random() * 50);
                return (
                  <div style={{
                    position: "absolute",
                    top: top,
                    left: left,
                    transform: `rotate(${angle}deg)`
                  }}>
                    <Card key={card["suit"] + card["rank"]} card={card} hidden={true} />
                  </div>
                )
              })
            }
          </div>
          <div className="table-cards">
            {
              tableCards.map((cardPair) => {
                const played_card = cardPair["played_card"];
                const beaten_card = cardPair["beaten_card"];

                return (
                  <div className="card-pair">
                    <div style={{
                      position: "absolute"
                    }}>
                      <Card key={played_card["suit"] + played_card["rank"]} card={played_card} />
                    </div>
                    {
                      beaten_card
                      ? <div style={{
                        position: "absolute",
                        top: 32,
                        left: 32
                      }}>
                          <Card key={beaten_card["suit"] + beaten_card["rank"]} card={beaten_card} />
                        </div>
                      : <></>
                    }
                  </div>
                )
              })
            }
          </div>
          <div className="deck">
            <div style={{
              transform: "rotate(90deg)",
              position: "absolute",
              left: -64,
            }}>
              <Card card={trumpCard} />
            </div>
            {
              deck["cards"].map((card, index) => {
                const offset = index * 1;
                return (
                  <div style={{
                    position: "absolute",
                    left: offset,
                    top: offset
                  }}>
                    <Card key={card["suit"] + card["rank"]} card={card} hidden={true} />
                  </div>
                )
              })
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
