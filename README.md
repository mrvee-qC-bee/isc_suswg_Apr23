# Quantum Chemistry in Solution: Implicit Solvent Calculations with SQD and Qiskit Serverless

A technical walkthrough of running solvated quantum chemistry on IBM Quantum QPUs using a hybrid QPU ↔ HPC workflow.

Tutorial link: [https://quantum.cloud.ibm.com/docs/en/tutorials/implicit-solvent-calculations](https://quantum.cloud.ibm.com/docs/en/tutorials/implicit-solvent-calculations)

## Overview

In about one hour, this tutorial runs the full hybrid pipeline end-to-end:

- **Sample-based Quantum Diagonalization (SQD)** for electronic structure
- **IEF-PCM** implicit solvation
- **Qiskit Serverless** for orchestration
- **Iterative QPU ↔ HPC self-consistent loop**, benchmarked against CASCI

The worked example is **methylamine in water** — small enough to benchmark against exact classical methods, but large enough to exercise every stage of a real workflow. The same pattern potentially points directly at harder, solvent-dominated sustainability problems: electrocatalysis, CO₂ capture, and battery electrolytes.

## Workflow covered

1. PySCF molecule setup
2. Geometry optimization
3. AVAS active-space selection
4. LUCJ ansatz preparation and transpilation
5. QPU sampling via Qiskit Runtime
6. Classical post-processing and configuration recovery
7. Self-consistent loop between QPU sampling and HPC diagonalization
8. CASCI benchmark comparison

## Prerequisites

- Python 3.10+
- An IBM Quantum account with access to a QPU backend (simulator works to follow along)
- Basic familiarity with quantum chemistry (Hartree-Fock, active spaces) and Qiskit

## Setup

Clone the repo:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Create the environment with conda:

```bash
conda env create -f environment.yml
conda activate qchem-sqd-tutorial
```

…or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Save your IBM Quantum credentials once:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN", overwrite=True)
```

## Running the tutorial

### As a notebook

```bash
jupyter notebook notebooks/tutorial.ipynb
```

### As RISE slides

RISE is included in the environment. Open the notebook and press `Alt-R` (or click the bar-chart icon in the toolbar) to enter slideshow mode. Navigate with the arrow keys; code cells remain fully executable inside the slides.

If you need to install RISE manually:

```bash
pip install rise
```

> Note: RISE works with the classic Jupyter Notebook interface. If you're on JupyterLab, either launch the classic UI (`jupyter nbclassic`) or use `jupyterlab-rise`.

## Key dependencies

| Package | Purpose |
|---|---|
| `qiskit`, `qiskit-addon-sqd` | SQD implementation |
| `qiskit-ibm-runtime` | QPU access |
| `qiskit-serverless` | Workflow orchestration |
| `pyscf` | Classical chemistry (HF, CASCI, PCM) |
| `rise` | Notebook slide presentation |

## References

- Sample-based Quantum Diagonalization — Robledo-Moreno *et al.*
- LUCJ ansatz — Motta *et al.*
- IEF-PCM in PySCF — see the `pyscf.solvent` module
- Qiskit Serverless documentation — https://docs.quantum.ibm.com/guides/serverless

## License

[MIT](./LICENSE) — choose and add a `LICENSE` file to match.

## Acknowledgments

Built on the IBM Quantum, Qiskit, and PySCF open-source ecosystems. Prepared as part of a sustainability-focused tutorial on applying near-term quantum computing to solvent chemistry.
