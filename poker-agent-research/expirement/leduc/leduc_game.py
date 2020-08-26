from enum import Enum
from typing import List
import random
from leduc.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction

cards = ['JH', 'QH', 'KH', 'JL', 'QL', 'KL']


class LeducGame:

    def __init__(self, player1: LeducAgent, player2: LeducAgent):
        self.player1 = player1
        self.player2 = player2
        self.money_pot = 0

    def play_round(self, round_num: int):
        deck = cards.copy()
        print(f'starting round: #{round_num}')
        first_hand, second_hand = self.deal_cards(deck)
        self.player1.receive_hand(first_hand)
        self.player2.receive_hand(second_hand)
        self.money_pot += 2

        player1_action = self.player1.take_action()
        self.commit_action(player1_action)
        player2_action = self.player2.take_action()
        self.commit_action(player2_action)
        community_card = self.reveal_community_card(deck)
        self.player1.receive_community_card(community_card)
        self.player2.receive_community_card(community_card)
        player1_action = self.player1.take_action()
        self.commit_action(player1_action)
        player2_action = self.player2.take_action()
        self.commit_action(player2_action)
        winner, pot = self.eval_winner_and_update(self.player1, self.player2)
        print(f'{winner.name} just won round {round_num} and earned {pot}$')
        self.money_pot = 0

    def commit_action(self, player_action):
        if player_action == LeducAction.CHECK:
            pass

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
        if player1_rank >= player2_rank:
            winner = player1

        else:
            winner = player2
        winner.money += self.money_pot
        return winner, self.money_pot
