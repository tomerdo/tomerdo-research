from leduc.agents.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction
from leduc.leduc_game import LeducGame


class RuleBasedAgent(LeducAgent):

    def choose_action(self, need_to_call_amount) -> LeducAction:
        card_value = self.hand[0]
        if self.community_card is not None:
            rank = LeducGame.rank([self.hand, self.community_card])
            if rank <= 2:
                return LeducAction.BET
            else:
                return LeducAction.CHECK
        if card_value == 'J':
            return LeducAction.CHECK
        elif card_value == 'Q':
            return LeducAction.CHECK
        else:
            return LeducAction.BET
