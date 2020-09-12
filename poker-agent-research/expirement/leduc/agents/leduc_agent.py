from abc import abstractmethod , ABC

from leduc.leduc_action import LeducAction


class LeducAgent(ABC):
    community_card: str = None
    hand: str = None

    def __init__(self, name: str, initial_money):
        self.name = name
        self.money = initial_money

    @abstractmethod
    def choose_action(self, need_to_call_amount) -> LeducAction:
        pass

    def receive_hand(self, hand: str):
        self.hand = hand
        # putting ante
        self.money -= 1

    def receive_community_card(self, community_card: str):
        self.community_card = community_card
