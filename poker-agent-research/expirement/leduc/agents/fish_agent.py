from leduc.agents.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction


class FishAgent(LeducAgent):
    def take_action(self) -> LeducAction:
        return LeducAction.CHECK
