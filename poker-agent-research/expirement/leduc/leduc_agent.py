from leduc.leduc_action import LeducAction


class LeducAgent:
    community_card: str
    hand: str

    def __init__(self, name: str, initial_money):
        self.name = name
        self.money = initial_money

    def take_action(self) -> LeducAction:
        return LeducAction.CHECK

    def receive_hand(self , hand: str):
        self.hand = hand
        # putting ante
        self.money -= 1

    def receive_community_card(self, community_card: str):
        self.community_card = community_card
