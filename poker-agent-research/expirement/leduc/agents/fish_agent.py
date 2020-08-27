from leduc.agents.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction


class FishAgent(LeducAgent):
    def choose_action(self, need_to_call_amount) -> LeducAction:
        if need_to_call_amount > 0:
            # FOLD
            return LeducAction.FOLD
        return LeducAction.CALL
