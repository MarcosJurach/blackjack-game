import random

suits = ('Hearts','Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_cards = 'The deck has: '
        for card in self.deck:
            deck_cards += '\n' + card.__str__()
        return deck_cards

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card=self.deck.pop()
        return single_card
        
        
class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
 
 
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
        
def take_bet(chips):
    while True:    
        try:
            chips.bet = int(input('How many chips do you wanna bet? '))
        except:
            print('The bet must be an intereger (a number)')
        else:
            if chips.bet > chips.total:
                print("Your bet can't be bigger than your total amount")
            else:
                break
                
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        player_choice = input('Would you like to hit or stand? [H] or [S] ')
        if player_choice.lower() == 'h':
            hit(deck,hand)
            break
        elif player_choice.lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False
            break
        else: 
            print('You must choose between [h]it or [s]tand')


def show_some(player_hand,dealer_hand):
    print("\nDealer's hand:")
    print("<card hidden>")
    print(" ", dealer_hand.cards[1])
    print("\nPlayer's hand:", *player_hand.cards,sep="\n")
    
    
def show_all(player_hand,dealer_hand):
    print("\nDealer's hand:", *dealer_hand.cards,sep="\n")
    print("\nDealer's hand value:",dealer_hand.value)
    print("\nPlayer's hand:", *player_hand.cards,sep="\n")
    print("\nPlayer's hand value:",player_hand.value)
    
    
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")
    
    
while True:
    print("Lets play Blackjack!")

    
    # Create & shuffle the deck, deal two cards to each player
    deck=Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand() 
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())    
        
    # Set up the Player's chips
    player_chips = Chips()
    print("You're starting the game with 100 chips. Use them wisely!")
    
    # Prompt the Player for their bet
    take_bet(player_chips)

    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand) 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
    show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
    if dealer_hand.value > 21:
        dealer_busts(player_hand,dealer_hand,player_chips)

    elif dealer_hand.value > player_hand.value:
        dealer_wins(player_hand,dealer_hand,player_chips)

    elif player_hand.value > dealer_hand.value:
        player_wins(player_hand,dealer_hand,player_chips)
            
    else:
        push(player_hand,dealer_hand)    
    
    
    # Inform Player of their chips total 
    print("Your total of chips is", player_chips.total)
    
    # Ask to play again
    again = input("Would you like to play again? [Y]es or [N]o")
    if again[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break