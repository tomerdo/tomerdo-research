from leduc.agents.leduc_agent import LeducAgent
from leduc.leduc_action import LeducAction
from leduc.leduc_game import LeducGame
import math


def evaluate(game_state):
    return 0.0


class MCTSAgent(LeducAgent):

    def __init__(self):
        super(self)
        self.tree = GameTree(GameState(self))

    def choose_action(self, need_to_call_amount) -> LeducAction:
        self.uct_search(num_of_simulation=1000)

    def uct_search(self, num_of_simulation):
        root = UCTNode(GameState(self))
        for _ in range(num_of_simulation):
            leaf = root.select_leaf()
            child_priors, value_estimate = evaluate(leaf.game_state)
            leaf.expand(child_priors)
            leaf.backup(value_estimate)
        return max(root.children.items(),
                   key=lambda item: item[1].number_visits)


class GameTree:
    def __init__(self, game_state):
        self.root = game_state
        self.children = game_state.possible_children()

    def get_possible_action(self):
        return self.children


class GameState:
    def __init__(self, agent):
        self.private_card = agent.hand
        self.public_card = agent.community_card


class UCTNode:
    def __init__(self, game_state, parent=None, prior=0):
        self.game_state = game_state
        self.is_expanded = False
        self.parent = parent  # Optional[UCTNode]
        self.children = {}  # Dict[move, UCTNode]
        self.prior = prior  # float
        self.total_value = 0  # float
        self.number_visits = 0  # int

    def Q(self) -> float:
        return self.total_value / (1 + self.number_visits)

    def U(self) -> float:
        return (math.sqrt(self.parent.number_visits)
                * self.prior / (1 + self.number_visits))

    def best_child(self):
        return max(self.children.values(),
                   key=lambda node: node.Q() + node.U())

    def select_leaf(self):
        current = self
        while current.is_expanded:
            current = current.best_child()
        return current

    def expand(self, child_priors):
        self.is_expanded = True
        for move, prior in enumerate(child_priors):
            self.add_child(move, prior)

    def add_child(self, move, prior):
        self.children[move] = UCTNode(
            self.game_state.play(move), parent=self, prior=prior)

    def backup(self, value_estimate):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += (value_estimate *
                                    self.game_state.to_play)
            current = current.parent
