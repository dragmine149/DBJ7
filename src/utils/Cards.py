import logging
import random

logger = logging.getLogger("src.utils.Cards")
logger.info("Initalised")


"""
Cards, lets you spawn in a deck of cards whenever.

shuffle_cards -> Makes a deck completly full of random cards in a random order
Draw_Card -> Draws a random card.
Get_Deck_Card -> Returns the card at X in deck
Check_If_Higher -> Check if B has a higher value than A

These cards can be used for whatever, just do from src.utils.Cards import Cards
"""


class Cards:
    def __init__(self):
        self.cards = {
            "Clubs": [
                "Ace",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
            ],
            "Spades": [
                "Ace",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
            ],
            "Diamonds": [
                "Ace",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
            ],
            "Hearts": [
                "Ace",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
            ],
        }
        self.suits = ["Clubs", "Spades", "Diamonds", "Hearts"]
        self.cardInfo = [
            "Ace",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
        ]

        self.deck = []

    def shuffle_cards(self, *, nUnique: bool = False, sUnique: bool = False):
        """Shuffle a deck of cards

        Args:
            nUnique (bool): Determins if no two numbers can be next to each other
            sUnique (bool): Determins if no two suits can be next to each other
        """
        cardInfo = self.cards.copy()
        lastCard = None

        for i in range(52):
            completed = False
            while not completed:
                card = self.Draw_Card()
                if card not in self.deck:
                    if lastCard is not None:
                        # Check for unique number
                        if nUnique:
                            if lastCard[1] == card[1]:
                                completed = False
                                continue

                        # Check for unique suit
                        if sUnique:
                            if lastCard[0] == card[0]:
                                completed = False
                                continue

                    # Continue
                    self.deck.append(card)

                    # remove from list to make it quicker to shuffle
                    rmCardIndex = self.cards[card[0]].index(card[1])
                    del self.cards[card[0]][rmCardIndex]

                    if len(self.cards[card[0]]) == 0:
                        rmIndex = self.suits.index(card[0])
                        del self.suits[rmIndex]

                    completed = True
                    lastCard = None

        self.cards = cardInfo.copy()

    def Draw_Card(self):
        """Draws a random card from the list of 52 cards

        Returns:
            _type_: _description_
        """

        suitInd = random.randrange(len(self.suits))
        suit = self.suits[suitInd]
        number = random.choices(self.cards[suit])[0]
        return (suit, number)

    def Get_Deck_Card(self, index: int):
        if len(self.deck) > 0:
            return self.deck[index]
        else:
            logger.warn("Deck has been requested for card before being shuffled")

    def Check_If_Higher(self, card, newCard):
        newValue = newCard[1]
        value = card[1]

        return self.cardInfo.index(newValue) >= self.cardInfo.index(value)
