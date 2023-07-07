import numpy as np
import lib
import matplotlib.pyplot as plt
from ridge import ks_flat as opaks

def main():
    colors = ["red", "green"]

    def get_datasets():
        root = "./data/prostate_reader/"
        group = "_5class"
        datasets = ["assisted", "unassisted"]
        return np.asarray([np.transpose(lib.data_reader(root + dataset + group + ".npy")) for dataset in datasets])
    datasets = get_datasets()

    ## Setup `choices`
    obs_choice = 6 - 2
    # step = 1
    # num_graphs = 4
    # interest = 43
    # bounds = (interest - step * (num_graphs // 2), interest + step * (num_graphs // 2 + 1))
    # choices = np.arange(bounds[0], bounds[1], step)
    choices = np.arange(28, 33 + 1)
    num_choices = len(choices)

    scale = 2.5
    ratio = 1
    fig, axs = plt.subplots(ncols=num_choices, figsize=(num_choices * scale, ratio*scale))
    max = -1
    full_counts = []

    res = opaks(datasets[0, obs_choice, choices, :],
                datasets[1, obs_choice, choices, :])
    print("All above certainty:", np.all(res == 1))
    print("choices:", choices)
    print("ks:", res)

    for i in range(len(datasets)):
        dataset = datasets[i]
        color = colors[i]
        obs = dataset[obs_choice]
        cases = obs[choices]

        rng = (0, 1)
        def _hist(x):
            global bins
            hist, bins = np.histogram(
                x,
                bins=30,
                range=rng
            )
            return hist
        counts = np.apply_along_axis(_hist, 1, cases)
        full_counts.append(counts)
        
        for j in range(len(choices)):
            ax = axs[j]
            ax.hist(
                bins[:-1],
                bins=bins,
                weights=counts[j],
                range=rng,
                align="left",
                color=color,
                alpha=.5
            )
        test = np.amax(counts)
        max = max if max > test else test

    for i in range(len(axs)):
        ax = axs[i]
        ax.set_ylim(0, max)
        ax.set_title(str(choices[i]) + " Cases")
        ax.spines[["left", "top", "right"]].set_visible(False)
        ax.yaxis.set_tick_params(
            left=False,
            labelleft=False)

    ax = axs[0]
    ax.spines[["left"]].set_visible(True)
    ax.yaxis.set_tick_params(
        left=True,
        labelleft=True)

    plt.tight_layout()
    plt.savefig("./results/case_split.png",
                bbox_inches="tight", transparent=False, dpi=1000)
    # plt.show()