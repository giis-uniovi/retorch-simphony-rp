# -*- coding: utf-8 -*-
import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
from scipy.spatial.distance import pdist, squareform

from simphonyrp.helpers.helpers import create_heatmap


def calculate_similarity():
    logging.debug("[1] Importing file")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")

    coverage_matrix_path = os.path.join(input_dir, "coverage_matrix.csv")

    df = pd.read_csv(coverage_matrix_path, sep=";", encoding="utf-8", engine="python")

    label_header = "Test Case/HU"
    logging.debug("[2] Cleaning columns")
    df.columns = df.columns.str.strip()
    logging.debug("[3] Extracting the number of test case for ordering")

    df['TestNum'] = df[label_header].str.extract(r'TC(\d+)', expand=False).astype(int)

    logging.debug("[4] Ordering by test number")

    df = df.sort_values('TestNum').reset_index(drop=True)

    logging.debug("[5] Converting 'X' into 1 and placing 0 into the empty cells")
    coverage_cols = df.columns[1:-1]
    binary_df = df[coverage_cols].fillna('').map(lambda x: 1 if x.strip().upper() == 'X' else 0)

    logging.debug("[6] Calculate hamming distance between rows(test-cases)")
    dist_matrix = pdist(binary_df.values, metric='hamming')

    logging.debug("[7] Converting into a square matrix and converting to a dataframe")

    sim_df = pd.DataFrame(1 - squareform(dist_matrix), index=df[label_header], columns=df[label_header])

    logging.debug("[8] Saving as xlxs and csv files")
    with pd.ExcelWriter("output/hamming_similarity.xlsx") as writer:
        sim_df.to_excel(writer, sheet_name="Hamming_Similarity")

    logging.info(".xlxs file with the similarity info generated into: output/hamming_similarity.xlsx")
    sim_df.to_csv("output/hamming_similarity.csv", sep=";", encoding="utf-8")
    logging.info(" .xlxs and .csv files generated sucessfully in: output/hamming_similarity.csv")

    create_heatmap(sim_df)


def calculate_prioritization():
    logging.debug("[1] Loading similarity matrix and initial prioritized list with the tests ")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")

    hamming_sim_data = os.path.join(input_dir, "hamming_similarity.csv")
    sim_df = pd.read_csv(hamming_sim_data, sep=";", index_col=0)

    tests = list(sim_df.index)
    prioritized = []

    logging.debug("[2] Calculating the average similarity of each test")
    avg_sim = sim_df.mean(axis=1)
    logging.debug("[3]  Selecting the less similar test case")
    first_test = avg_sim.idxmin()

    prioritized.append(first_test)
    tests.remove(first_test)
    logging.debug("[4]  Prioritization algorithm, starting to add the most different test case")

    while tests:
        max_dist = -1
        next_test = None
        for t in tests:
            # Calculamos "diferencia promedio" respecto a los ya seleccionados
            diff = 1 - sim_df.loc[t, prioritized]
            avg_diff = diff.mean()
            if avg_diff > max_dist:
                max_dist = avg_diff
                next_test = t
        prioritized.append(next_test)
        tests.remove(next_test)

    logging.debug("[5] Showing the priority")
    logging.info("The prioritized test suite is:")
    for i, t in enumerate(prioritized, 1):
        logging.info(f"{i:02d}. {t}")

    logging.debug("[6] Saving as csv file")
    pd.DataFrame({"Priority": range(1, len(prioritized) + 1), "Test": prioritized}).to_csv(
        "output/prioritization.csv", index=False
    )
    logging.info("[7] .csv file with the prioritized test suite saved")


def plot_coverage_evolution():
    approach_name = "SIMPHONY"
    end_times = {
        "Baseline/Priorit.": 1432,
        "RETORCH": 515,
        "Reduction": 331,
        approach_name + "-Prior.": 576,
        approach_name + "-Reduc.": 193
    }

    logging.debug("[1] Loading the .csv file with the coverage evolution")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")
    coverage_evol_path = os.path.join(input_dir, "coverage_evolution.csv")

    df = pd.read_csv(coverage_evol_path, sep=";", decimal=",")

    logging.debug("[2] Estructuring the dataframe")
    df["Approach"] = df["Approach"].replace(r"\$APPROACH", approach_name, regex=True)

    df_melt = df.melt(id_vars=["Approach", "Coverage"], var_name="Tiempo", value_name="Valor")
    df_melt["Tiempo"] = pd.to_numeric(df_melt["Tiempo"], errors="coerce")
    df_melt["Valor"] = pd.to_numeric(df_melt["Valor"], errors="coerce")

    logging.debug("[3] Splitting by the type of coverage")
    df_branches = df_melt[df_melt["Coverage"].str.lower() == "branches"]
    df_instructions = df_melt[df_melt["Coverage"].str.lower() == "instructions"]

    logging.debug("[4] Creating the plots")
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Font sizes
    title_size = 20
    label_size = 18
    tick_size = 12
    legend_size = 17

    logging.debug("[5] Tuning instruction coverage graph")
    for name, group in df_instructions.groupby("Approach"):
        axes[0].plot(group["Tiempo"], group["Valor"], label=name)
    axes[0].set_title("Evolution of Instruction Coverage", fontsize=title_size, fontweight="bold")
    axes[0].set_ylabel("Coverage (%)", fontsize=label_size)
    axes[0].tick_params(axis="both", labelsize=tick_size)
    axes[0].grid(True)
    axes[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  # 👈 Formato con dos decimales
    logging.debug("[6] Adding end times with a vertical dotted line")
    for name, t in end_times.items():
        axes[0].axvline(x=t, color="gray", linestyle="--", linewidth=1)
        axes[0].text(t, 0.24, name, rotation=90,
                     verticalalignment="top", horizontalalignment="left", fontsize=10, color="gray")

    logging.debug("[7] Tuning branch coverage graph")
    for name, group in df_branches.groupby("Approach"):
        axes[1].plot(group["Tiempo"], group["Valor"], label=name)
    axes[1].set_title("Evolution of Branch Coverage", fontsize=title_size, fontweight="bold")
    axes[1].set_xlabel("Time (s)", fontsize=label_size)
    axes[1].set_ylabel("Coverage (%)", fontsize=label_size)
    axes[1].tick_params(axis="both", labelsize=tick_size)
    axes[1].grid(True)
    axes[1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  # 👈 Formato con dos decimales

    logging.debug("[8] Adding end times with a vertical dotted line")
    for name, t in end_times.items():
        axes[1].axvline(x=t, color="gray", linestyle="--", linewidth=1)
        axes[1].text(t, 0.13, name, rotation=90,
                     verticalalignment="top", horizontalalignment="right", fontsize=10, color="gray")

    logging.debug("[9] Tuning the legend")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=legend_size, frameon=False, borderpad=-0.4)

    logging.debug("[10] Adjusting the layout")
    plt.tight_layout(rect=[0.0, 0.08, 1.0, 1.0])
    plt.savefig("output/figures/Fig_4_1.pdf", format="pdf")
    logging.info("Graph saved into: output/figures/Fig_4_1.pdf")
    plt.show()
