import numpy as np
import pymc3 as pm
from probablistic.rps import get_result, numerical_wins


def rps_player_model(alpha=[1, 1, 1], observed=None):
    with pm.Model() as model:
        dirichlet = pm.Dirichlet('dirichlet', a=alpha)
        phi = pm.Categorical('phi', p=dirichlet, observed=observed)
        return model


def infer(model):
    with model:
        trace = pm.sample(step=pm.Metropolis(), model=model, return_inferencedata=True, progressbar=False)
        return trace


def sample_from_posterior(model, trace):
    with model:
        posterior_pred = pm.sample_posterior_predictive(trace, progressbar=False)
        median_over_samples = np.median(posterior_pred['phi'], axis=0)
        return median_over_samples


def sample_from_prior(model, num_of_samples):
    with model:
        samples = pm.sample_prior_predictive(num_of_samples)['phi']
        return samples


def simulate_with_latent_alpha(num_of_simulations=10, alpha=[1, 1, 1]):
    total_smart_player_wins = 0
    total_simple_player_wins = 0
    total_ties = 0

    simple_player_observation = []

    for i in range(num_of_simulations):
        # Learning phase
        simple_player = rps_player_model(alpha=alpha)

        if len(simple_player_observation) == 0:
            simple_player_observations = sample_from_prior(simple_player, num_of_samples=10)

        # gets a list of observed values and returns the distribution of probable action
        smart_player = rps_player_model(observed=simple_player_observations)
        trace = infer(smart_player)

        smart_player_next_moves = sample_from_posterior(smart_player, trace)
        smart_player_next_moves = list(map(numerical_wins, smart_player_next_moves))

        # Evaluation phase
        simple_player_next_moves = sample_from_prior(simple_player, num_of_samples=10)

        smart_player_wins = 0
        simple_player_wins = 0
        ties = 0

        for j in range(len(simple_player_next_moves)):
            result = get_result(smart_player_next_moves[j], simple_player_next_moves[j])
            if result > 0:
                smart_player_wins += 1
            elif result < 0:
                simple_player_wins += 1
            else:
                ties += 1
        total_smart_player_wins += smart_player_wins
        total_simple_player_wins += simple_player_wins
        total_ties += ties
        print(f'in simulation {i}: wins: {smart_player_wins}, loses: {simple_player_wins}, ties: {ties}')
    print(
        f'For opponent\'s alpha vector: {alpha} averages in all simulations is wins: {total_smart_player_wins / num_of_simulations} '
        f' loses:{total_simple_player_wins / num_of_simulations} ties:{total_ties / num_of_simulations}')


def main():
    simulate_with_latent_alpha(alpha=[1, 10, 10])
    # simulate_with_latent_alpha(alpha=[1, 3, 5])
    simulate_with_latent_alpha(alpha=[1, 1, 1])
    simulate_with_latent_alpha(alpha=[1, 6, 1])
    simulate_with_latent_alpha(alpha=[10, 6, 1])


if __name__ == '__main__':
    main()
