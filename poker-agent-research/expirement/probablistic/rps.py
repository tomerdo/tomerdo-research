from enum import IntEnum

import numpy as np


def wins(other):
    if other is RPS.ROCK:
        return np.long(1)
    elif other is RPS.PAPER:
        return np.long(2)
    else:
        return np.long(0)


def numerical_wins(i):
    return (i + 1) % 3


class RPS(IntEnum):
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2


def get_result(first_player, second_player):
    if first_player == second_player:
        return 0
    elif (first_player == RPS.ROCK and second_player == RPS.SCISSORS) or (
            first_player == RPS.PAPER and second_player == RPS.ROCK) or (
            first_player == RPS.SCISSORS and second_player == RPS.PAPER):
        return 1
    else:
        return -1
