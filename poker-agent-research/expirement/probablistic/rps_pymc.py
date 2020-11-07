import numpy as np
import pymc3 as pm
import arviz as az
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with pm.Model() as model:
        prior = [1, 1, 1]
        observed = [1, 1, 1, 1, 2, 1, 1, 0, 1]
        # observed = None
        dirichlet = pm.Dirichlet('dirichlet', a=prior)
        phi = pm.Categorical('phi', p=dirichlet, observed=observed)
        trace = pm.sample(draws=10_000, step=pm.Metropolis(), return_inferencedata=True)

    # print(model.basic_RVs)
    # # print(model.logp({"phi": 0}))
    # print(model.logp({"phi": 1}))
    # print(model.logp({"phi": 2}))
    # print(model.logp({"phi": 3}))
    # print(model.logp({"phi": -1}))
    # print(model.logp({"phi": 100}))
    # plt.subplot(axs=az.plot_trace(trace))
    print(az.summary(trace))