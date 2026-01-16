# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


def ensure_output_dir(directory_name="output"):
    directory = Path(directory_name)

    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Was not possible to create the directory: {e}")

    return str(directory.resolve())


def create_heatmap(sim_df):
    logging.info("Creating heatmap")
    logging.debug("Using the matrix to generate heatmap")
    plt.figure(figsize=(12, 10))

    sns.heatmap(sim_df, annot=False, cmap="coolwarm", square=True, cbar_kws={"label": "Hamming distance"})

    plt.xlabel("System Test Cases")
    plt.ylabel("System Test Cases")

    logging.debug("Saving heatmap as pdf")

    plt.tight_layout()
    plt.savefig("output/figures/Fig_3_1.pdf", format="pdf")
    plt.show()

    logging.info("Heatmap saved correctly at  output/figures/Fig_3_1.pdf")
