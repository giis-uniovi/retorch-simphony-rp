# -*- coding: utf-8 -*-
import logging

from simphonyrp.core import plot_coverage_evolution
from simphonyrp.core import calculate_prioritization
from simphonyrp.core import calculate_similarity

import simphonyrp.helpers.helpers as helpers


def main():
    logging.info("Starting experiment")
    helpers.ensure_output_dir()
    helpers.ensure_output_dir("output/figures")

    calculate_similarity()
    calculate_prioritization()
    plot_coverage_evolution()
    logging.info("End experiment")

if __name__ == "__main__":
    main()
