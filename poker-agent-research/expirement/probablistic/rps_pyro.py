from enum import Enum, IntEnum

import matplotlib.pyplot as plt
import numpy as np
import torch

import pyro
import pyro.infer
import pyro.optim
import pyro.distributions as dist

from probablistic.rps import RPS, get_result


def first_player_model():
    strategy = pyro.sample('strategy', dist.Dirichlet(torch.tensor([0.33, 0.33, 0.34])))
    return pyro.sample("p1", dist.Categorical(strategy.type(torch.DoubleTensor)))


def condition_to_win(second_player_choice):
    first_player_conditioned_choice = wins(second_player_choice)
    return pyro.condition(first_player_model, data={"p1": first_player_conditioned_choice})


def learn_best_strategy(num_of_trails=100):
    importance = pyro.infer.Importance(condition_to_win(RPS(pyro.sample("p2", dist.Categorical(torch.tensor([1.0, 1.0, 100.0]))).item())))
    importance.run()
    # return mcmc.get_samples()['p1'].mean(0)


def play_rps(num_of_trails=100):
    """
    simulate a game between two rps players
    :param num_of_trails:
    :return: the ratio between player one winning and player two winning
    """
    first_player_wins = 0
    second_player_wins = 0
    ties = 0
    for i in range(num_of_trails):
        first_player = RPS(pyro.sample("p1", dist.Categorical(torch.ones(3))).item())
        print('first player chose {}'.format(repr(first_player)))

        second_player = RPS(pyro.sample("p2", dist.Categorical(torch.tensor([1.0, 1.0, 100.0]))).item())
        print('second player chose {}'.format(repr(second_player)))

        result = get_result(first_player, second_player)

        if result > 0:
            first_player_wins += 1
        elif result < 0:
            second_player_wins += 1

        else:
            ties += 1

    return first_player_wins, second_player_wins, ties


def main():
    #first_player_wins, second_player_wins, ties = play_rps()
    #print(f'first_player_wins:{first_player_wins} second_player_wins:{second_player_wins} ties:{ties}')
    learn_best_strategy()


if __name__ == '__main__':
    main()
