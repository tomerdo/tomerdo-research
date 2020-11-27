import numpy as np
import pymc3 as pm
import arviz as az
import matplotlib.pyplot as plt
from time import time
from probablistic.rps import RPS, get_result, numerical_wins


def first_player_model(observed):
    t1 = time()
    with pm.Model() as model_1:
        alpha = [1, 1, 1]
        # observed = None
        dirichlet = pm.Dirichlet('dirichlet', a=alpha)
        phi = pm.Categorical('phi', p=dirichlet, observed=observed)
        posterior = pm.sample(step=pm.Metropolis(), return_inferencedata=True)
        posterior_pred = pm.sample_posterior_predictive(posterior)

        # print(az.summary(posterior))
        # print(posterior_pred)
        median_over_samples = np.median(posterior_pred['phi'], axis=0)
        # print(median_over_samples)
        t2 = time()
        elapsed = t2 - t1
        # print('Elapsed time is %f seconds.' % elapsed)
        return median_over_samples


def second_player_model(num_of_samples=5, alpha=[1, 5, 3]):
    with pm.Model() as model_2:
        dirichlet = pm.Dirichlet('dirichlet', a=alpha)
        phi = pm.Categorical('phi', p=dirichlet)
        return phi.random(size=num_of_samples)


def simulate_with_latent_alpha(num_of_simulations=10, alpha=[1, 1, 1]):
    total_first_player_wins = 0
    total_second_player_wins = 0
    total_ties = 0
    for i in range(num_of_simulations):
        # Learning phase
        second_player_history = second_player_model(num_of_samples=10, alpha=alpha)

        # gets a list of observed values and returns the distribution of probable action
        first_player_next_moves = first_player_model(observed=second_player_history)

        # print(first_player_next_moves)

        first_player_next_moves = list(map(numerical_wins, first_player_next_moves))
        # print(first_player_next_moves)

        # Evaluation phase
        second_player_next_moves = second_player_model(len(first_player_next_moves), alpha=alpha)

        first_player_wins = 0
        second_player_wins = 0
        ties = 0

        for j in range(len(second_player_next_moves)):
            result = get_result(first_player_next_moves[j], second_player_next_moves[j])
            if result > 0:
                first_player_wins += 1
            elif result < 0:
                second_player_wins += 1
            else:
                ties += 1
        total_first_player_wins += first_player_wins
        total_second_player_wins += second_player_wins
        total_ties += ties
        # print(f'in simulation {i}: wins: {first_player_wins}, loses: {second_player_wins}, ties: {ties}')
    print(
        f'For opponent\'s alpha vector: {alpha} averages in all simulations is wins: {total_first_player_wins / num_of_simulations} '
        f' loses:{total_second_player_wins / num_of_simulations} ties:{total_ties / num_of_simulations}')


def main():
    simulate_with_latent_alpha(alpha=[1, 10, 10])
    simulate_with_latent_alpha(alpha=[1, 3, 5])
    simulate_with_latent_alpha(alpha=[1, 1, 1])
    simulate_with_latent_alpha(alpha=[1, 6, 1])
    simulate_with_latent_alpha(alpha=[10, 6, 1])


if __name__ == '__main__':
    main()
