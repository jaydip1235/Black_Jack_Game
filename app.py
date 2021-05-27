from random import shuffle

suits = ('Hearts', 'Diamond', 'Spades', 'Clubs')
rank = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
        'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')

values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

playing = True


# class definations : card , chips, hands , deck

# all cards will have a suit and rank property
# let say ace of diamonds: here ace is card rank and diamond is suit
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


# deck will contain all cards: we have four suits and 13 cards of each suits
class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            # hearts
            for item in rank:
                # here item will be rank like ace , two...
                self.deck.append(Card(suit, item))

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

    def __str__(self):
        deck = ''
        for item in self.deck:
            deck += '\n' + item.__str__()

        return deck


# hands means no of cards  you are holding
class Hand:
    # initially you dont have any cards so your total value is also 0 and no of aces is also 0
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        # let say rank of card is ace
        # values['Ace'] = 11
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_aces(self):
        # let say you have three cards : 10,10 and ace
        # so your value is greater than 21 : 10 + 10 +11 = 31
        # but you can use ace as 1 in this case to get 21
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    # initially we are supposing that we have 100rs or coins
    def __init__(self):
        self.total = 100
        self.bet = 0

    # for example, you have placed 50 for bet and you loose. your initial total no of chips were 100
    # now you have lost 50 so total left will be total - (bet you have placed)
    # so it will be 100 - 50 = 50
    def loose_bet(self):
        self.total -= self.bet

    # for example, you have placed 50 for bet and you won. your initial total no of chips were 100
    # now you have won 50 so total left will be total + (bet you have placed)
    # so it will be 100 + 50 = 150
    def win_bet(self):
        self.total += self.bet


def place_bet(chips):
    while True:
        try:
            # ask user how much bet he/she wants to place? it is a string so we are converting it into a int
            chips.bet = int(input('How many chips you want to bet?'))
        except Exception as e:
            print(e)
        else:
            break


# we are simply using deck and hand functions to add card and adjust aces
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_aces()


# we will use this when we want to show only one card of dealer but two cards of player
def show_some(player, dealer):
    print('\n Dealers Hand')
    print('<Cards Hidden>')
    print(f'one card of dealer: {dealer.cards[1]}')
    print(f'players card are', *player.cards, sep='\n')


# we will use this to show all cards of both player and dealer
def show_all(player, dealer):
    print(f'Dealer hand is:,', *dealer.cards, sep='\n')
    print(f'Dealer Value: {dealer.value}')
    print(f'Player hand is:,', *player.cards, sep='\n')
    print(f'Player Value: {player.value}')


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input('Would you like to pick more cards or stand? Enter h or s \n')
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print('player is standing now and dealer will player')
            playing = False
        else:
            print('Wrong Value.Please try again')
            continue
        break


def player_bursts(chips):
    print('Player Bursts!!')
    chips.loose_bet()


def player_wins(chips):
    print('Player won!! :)')
    chips.win_bet()


def dealer_bursts(chips):
    print('Player Bursts!!')
    chips.win_bet()


def dealer_wins(chips):
    print('Player won!! :)')
    chips.loose_bet()


def tie():
    print('Player and Dealer tie!!')


# start the real game

while True:
    print('Welcome to our Black Jack Game. Get closest to 21 to win \n you can choose ace as 1 or 11 as you wish')
    # initializing deck and then shuffling it
    deck = Deck()
    deck.shuffle()
    # player hand is initialized and then we are giving two cards to the player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    # Dealer hand is initialized and then we are giving two cards to the player

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    # now we are initializing the player chips and then placing a bet
    player_chips = Chips()

    place_bet(player_chips)
    # now we will show cards of both player and dealer. We will show two cards of player but only one card of dealer
    show_some(player_hand, dealer_hand)
    # now player will start taking cards till playing is true. Remember
    # inside hit or stand we are turning this playing value to false that means player does not want to pick more cards
    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        # now after player keep hitting and said stand we will check if some is greater that 21. if yes than player is burst
        if player_hand.value > 21:
            player_bursts(player_chips)
            break
    # now we are out of while loop. PLayer is on stand but have sum less than 21
    if player_hand.value <= 21:
        # we are keeping dealer value less than 17 so that he wont go for >21
        while dealer_hand.value < 17:
            # now dealer will start hitting
            hit(deck, dealer_hand)
        # when dealer ends we will show all cards and the result
        show_all(player_hand, dealer_hand)
        if dealer_hand.value > 21:
            dealer_bursts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            tie()

    print(f'At the end value of player chips is:{player_chips.total}')
    # now game came to an end we will ask to start a new game and again while loop will repeat
    new_game = input('Would you like to play again? Enter y or n')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    if new_game[0].lower() == 'n':
        print('Thanks for playing!!')
        break
