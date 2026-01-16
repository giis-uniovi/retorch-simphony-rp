[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17442306.svg)](https://doi.org/10.5281/zenodo.17442306)

# Replication package for *'A Framework for Similarity-based and Resource-aware Orchestration of End-to-End Test Cases'*

This repository contains the replication package of the paper *A Framework for Similarity-based and Resource-aware Orchestration of End-to-End Test Cases*
published at *7th ACM/IEEE International Conference on Automation of Software Test (AST 2026)*

This replication package includes the different python scripts, Jenkinsfiles, docker-compose files, environment files `.env` and coverage data in both `.xml` and `.exec` formats.
The replication package structure is depicted as follows:

```markdown
📁 /
├── 📜 .gitignore
├── 📜 CITATION.cff
├── 🤝 LICENSE
├── 🏗️ pyproject.toml
├── 📖 README.md
│
├── 📦 simphonyrp/
│   ├── 🐍 core.py
│   ├── 🐍 experimentation.py
│   ├── 🐍 __init__.py
│   ├── 📦 helpers/
│   └── 📁 input/
│
└── 📁 data/
    ├── 📁 coverage/
    │   ├── 📁 no-orchestrated/
    │   │   ├── 📁 exec/
    │   │   │   ├── 📈 jacoco-tc01-loginTest.exec
    │   │   │   └── ...
    │   │   └── 📁 xml/
    │   │       ├── 📁 baseline/
    │   │       └── 📁 ...
    │   └── 📁 orchestrated/
    │       ├── 📁 exec/
    │       │   ├── 📁 minimization/
    │       │   └── 📁 ...
    │       │
    │       └── 📁 xml/
    │           ├── 📁 minimization/ 
    │           └── 📁 ...
    │
    └── 📁 scripts/
        ├── 🐳 docker-compose.yml
        ├── 📁 enfiles/
        │   ├── 🗃️ tjobn.env
        │   └── ...
        └── 📁 jenkinsfiles/
            ├── 📁 no-orchestrated/
            │   ├── 🚀 baseline-Jenkinsfile
            │   └── 🚀 ...
            └── 📁 orchestrated/
                ├── 🚀 minimization-Jenkinsfile
                └── 🚀 ...
```

- `📦 simphonyrp/` contains the Python scripts used to compute the similarity matrix, as well as the prioritization and
  minimization procedures described in the article. It includes `🐍 core.py`, which holds the main code; a `📦 helpers/`
  folder with supporting utilities; an `🐍 experimentation.py` script; and an `📁 input/` folder with the required data
  sources. During execution, an `📁 output/` folder is dynamically generated to store the calculation results.

- `📁 data/` contains all execution data and the scripts required to run the different execution plans. It is organized
  into two subfolders:

  - `📁 coverage/` includes the coverage files from the 6 execution alternatives, collected with JaCoCo during test
    execution. Coverage data is provided in two formats (.xml and .exec), and organized into folders according to each
    alternative (e.g. prioritization without orchestration, minimization, baseline).

  - `📁 scripts/` includes the `docker-compose.yml`, the environment `.env` files, and the `Jenkinsfiles` used in CI. The folder
    structure mirrors the different execution alternatives (e.g. prioritization without orchestration, minimization,
    baseline).


The replication package data is also archived on [Zenodo](https://doi.org/10.5281/zenodo.17442306)

## Experimental Subject

The experimental subject is a real-world application
called [Fullteaching](https://github.com/codeurjc-students/2019-FullTeaching/tree/Angular-Refactor), used as a
demonstrator of the [ElasTest EU Project](https://elastest.eu/). FullTeaching provides an education platform composed
of several test resources, such as web servers, databases, and multimedia servers that allows to create online
classrooms, classes or publish and create class resources.

To the best of our knowledge, FullTeaching has two test suites available in different
repositories [[1]](https://github.com/elastest/full-teaching) [[2]](https://github.com/codeurjc-students/2019-FullTeaching/tree/Angular-Refactor).
The test suite used to generate the raw datasets provided in this replication package is a compilation of the available
test, cases in these repositories. The test suite, along with the necessary scripts and JenkinsFile required to run the
Execution Plan is made available as the version 1.1.0 in
the [retorch-st-fullteaching](https://github.com/giis-uniovi/retorch-st-fullteaching)
GitHub repository.

From the FullTeaching test suite we have also employed the user requirements in english language used during its
development . They are available in the replication package of our article
titled [Exploratory study of the usefulness of LLMs in System testing](https://github.com/giis-uniovi/retorch-llm-rp/blob/main/llm-rp-expstudy/src/main/resources/input/inputUserRequirements_en.txt)

## Treatment Replication Procedure

To run the experimentation script provided in `📦 simphonyrp/`, Python version 12.0 or later is required. Follow these steps to execute the script:

1. Navigate to the root of the repository and create a virtual environment:

   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:

   * On Windows: `venv\Scripts\activate`
   * On Linux/macOS: `source venv/bin/activate`

3. Install and configure the project:

   ```bash
   pip install -e .
   ```
4. Run the experimentation script with:

   ```bash
   experiment
   ```

## Contributing

See the general contribution policies and guidelines for *giis-uniovi* at
[CONTRIBUTING.md](https://github.com/giis-uniovi/.github/blob/main/profile/CONTRIBUTING.md).

## Contact

Contact any of the researchers who authored the paper; their affiliation and contact information are provided in the
paper itself.

## Citing this work

- Cristian Augusto, Antonia Bertolino, Guglielmo De Angelis, Claudio de la Riva, Francesca Lonetti and Jesús Morán, *“A Framework for Similarity-based and Resource-aware Orchestration of End-to-End Test Cases”* at *7th ACM/IEEE International Conference on Automation of Software Test (AST 2026)*,   [doi: 10.1145/3793654.3793742](https://doi.org/10.1145/3793654.3793742) - [Full Paper available](https://doi.org/10.1145/3793654.3793742) - [Authors version](TO-DO) -
  [Download citation](TO-DO)

## Acknowledgments

This work was supported in part by the project EQUAVEL (PID2022-137646OB-C32) funded by MCIN/AEI/10.13039/501100011033/FEDER,
UE and in part by the European [HORIZON-KDT-JU research project MATISSE](https://matisse-kdt.eu/): *"Model-based
engineering of Digital Twins for early verification and validation of Industrial Systems"*, HORIZON-KDT-JU-2023-2-
RIA, Proposal number: 101140216-2, KDT232RIA_00017, and also by the (partial) support of the PNRR MUR project [FAIR (PE0000013)](https://www.mur.gov.it/sites/default/files/2023-02/D.D.%20341%20_PE0000013_rev181022NF.pdf).
This paper has been also partially supported by the Italian MUR PRIN 2022 Project: Domain (Grant Agreement #2022TSYYKJ) financed by NextGenEu.
Guglielmo De Angelis is with the Italian Research Group: [INdAM-GNCS](https://www.altamatematica.it/gncs/)
