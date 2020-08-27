from leduc.agents.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction


class RuleBasedAgent(LeducAgent):

    def choose_action(self, need_to_call_amount) -> LeducAction:
        card_value = self.hand[0]
        if card_value == 'J':
            return LeducAction.FOLD
        elif card_value == 'Q':
            return LeducAction.CHECK
        else:
            return LeducAction.BET
