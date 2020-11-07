import numpy as np
import pymc3 as pm
import arviz as az
import matplotlib.pyplot as plt

from probablistic.rps import RPS, get_result, numerical_wins


def first_player_model(observed):
    with pm.Model() as model_1:
        alpha = [1, 1, 1]
        observed = observed
        # observed = None
        dirichlet = pm.Dirichlet('dirichlet', a=alpha)
        phi = pm.Categorical('phi', p=dirichlet, observed=observed)
        posterior = pm.sample(step=pm.Metropolis(), return_inferencedata=True)
        posterior_pred = pm.sample_posterior_predictive(posterior)

        print(az.summary(posterior))
        print(posterior_pred)
        median_over_samples = np.median(posterior_pred['phi'], axis=0)
        print(median_over_samples)
        return median_over_samples


def second_player_model(num_of_samples=200):
    with pm.Model() as model_2:
        alpha = [100, 100, 1]
        dirichlet = pm.Dirichlet('dirichlet', a=alpha)
        phi = pm.Categorical('phi', p=dirichlet)
        return phi.random(size=num_of_samples)


def main():
    # Learning phase
    second_player_history = second_player_model(num_of_samples=200)

    # gets a list of observed values and returns the distribution of probable action
    first_player_next_moves = first_player_model(observed=second_player_history)

    print(first_player_next_moves)

    first_player_next_moves = list(map(numerical_wins, first_player_next_moves))
    print(first_player_next_moves)

    # Evaluation phase
    second_player_next_moves = second_player_model(len(first_player_next_moves))

    first_player_wins = 0
    second_player_wins = 0
    ties = 0

    for i in range(len(second_player_next_moves)):
        result = get_result(first_player_next_moves[i], second_player_next_moves[i])
        if result > 0:
            first_player_wins += 1
        elif result < 0:
            second_player_wins += 1
        else:
            ties += 1

    print(f'wins: {first_player_wins}, loses: {second_player_wins}, ties: { ties}')


if __name__ == '__main__':
    main()