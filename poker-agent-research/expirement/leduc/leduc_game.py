from typing import List
import random
from leduc.agents.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction

cards = ['JH', 'QH', 'KH', 'JL', 'QL', 'KL']


class LeducGame:

    def __init__(self, player1: LeducAgent, player2: LeducAgent):
        self.player1 = player1
        self.player2 = player2
        self.money_pot = 0
        self.active_players = []
        self.need_to_call = 0

    def play_round(self, round_num: int):

        self.active_players: List[LeducAgent] = [self.player1, self.player2]

        deck = cards.copy()
        print(f'starting round: #{round_num}')

        # Dealing the private cards
        first_hand, second_hand = self.deal_cards(deck)
        self.player1.receive_hand(first_hand)
        self.player2.receive_hand(second_hand)

        # each player put ante
        self.money_pot += 2

        # first player playing (TODO - late do in rotations , and have a choice to do limited betting)
        player1_action = self.player1.take_action()
        try:
            self.commit_action(self.player1, player1_action)

            # second player playing
            player2_action = self.player2.take_action()
            self.commit_action(self.player2, player2_action)

            # dealing the community card
            community_card = self.reveal_community_card(deck)
            self.player1.receive_community_card(community_card)
            self.player2.receive_community_card(community_card)

            player1_action = self.player1.take_action()
            self.commit_action(self.player1, player1_action)

            player2_action = self.player2.take_action()
            self.commit_action(self.player2, player2_action)
            winner, pot = self.eval_winner_and_update(self.player1, self.player2)

        except LastPlayerException:
            winner, pot = self.active_players.pop(), self.money_pot
            winner.money += self.money_pot
            print(f'the second player folded the winner is {winner.name} and won a {pot}')

        if winner is not None:
            prompt_message = f'{winner.name} just won round {round_num} and earned {pot}$'
        else:  # TIE
            prompt_message = f'the game ended with tie both player got half of the pot. each got {pot}'
        print(prompt_message)

        # deleting all the data
        self.money_pot = 0
        self.need_to_call = 0
        self.active_players = []

    def commit_action(self, player, player_action):
        if player_action == LeducAction.CHECK:
            if self.need_to_call > 0:
                # FOLD
                self.fold(player)
            self.call(player)
        elif player_action == LeducAction.FOLD:
            self.fold(player)
        else:  # BET
            self.bet(player, 1)

    def call(self, player):
        player.money -= self.need_to_call
        self.need_to_call = 0

    def bet(self, player, bet_amount):
        player.money -= bet_amount
        self.money_pot += bet_amount
        self.need_to_call = bet_amount

    def fold(self, player):
        self.active_players.remove(player)
        raise LastPlayerException()

    @staticmethod
    def deal_cards(deck):
        random.shuffle(deck)
        first_card = deck.pop()
        second_card = deck.pop()
        return first_card, second_card

    @staticmethod
    def rank(hand: List[str]) -> int:
        ranks = {
            'KK': 1,
            'QQ': 2,
            'JJ': 3,
            'KQ': 4, 'QK': 4,
            'KJ': 5, 'JK': 5,
            'QJ': 6, 'JQ': 6
        }
        eval_cards = hand[0][0] + hand[1][0]
        return ranks[eval_cards]

    @staticmethod
    def reveal_community_card(deck):
        return deck.pop()

    def eval_winner_and_update(self, player1, player2) -> [LeducAgent, int]:
        player1_rank = LeducGame.rank([player1.hand, player1.community_card])
        player2_rank = LeducGame.rank([player2.hand, player2.community_card])
        print(f'player1 hand rank is {player1_rank} player2 hand rank is {player2_rank}')
        if player1_rank == player2_rank:
            half_the_pot = self.money_pot / 2
            self.player1.money += half_the_pot
            self.player2.money += half_the_pot
            return None, half_the_pot
        elif player1_rank > player2_rank:
            winner = player1
        else:
            winner = player2
        winner.money += self.money_pot
        return winner, self.money_pot


class LastPlayerException(Exception):
    pass
