using Turing
using StatsPlots

@model function alice()
	myLocation ~ Bernoulli(0.55)
end

#  Run sampler, collect results
chn = sample(alice(), IS(), 1000)

# Summarise results
describe(chn)

# Plot and save results
p = plot(chn)
savefig("schelling-plot.png")
