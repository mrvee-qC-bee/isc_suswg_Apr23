#!/usr/bin/env python3
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder

from qiskit_serverless import get_arguments, save_result

import pyscf
from pyscf import gto, scf
from pyscf.solvent import pcm
from pyscf.mcscf import avas

import psutil

mem_info = (
    psutil.virtual_memory()
)  # Get information about virtual memory (RAM)
total_ram_gb = mem_info.total / (1024**3)  # Convert bytes to GB
print(f">>>>> SERVERLESS TOTAL RAM: {total_ram_gb:.2f} GB")

### Argument retrieval
args = get_arguments()
data = args["data"]  # Chemistry Data

i_data = JSONDecoder().decode(data)
[mol_geo, eps, ao_labels] = i_data

print(">>>>> DEFINING MOLECULE")
mol = gto.M()
mol.atom = mol_geo
mol.basis = "cc-pVDZ"
mol.unit = "Ang"
mol.charge = 0
mol.spin = 0
mol.verbose = 0

print(">>>>> BUILDING MOLECULE")
mol.build()

print(">>>>> DEFINING PCM")
cm = pcm.PCM(mol)
cm.eps = eps  # for water
cm.method = "IEF-PCM"

print(">>>>> BUILDING RESTRICTED HARTREE FOCK")
mf = scf.RHF(mol).PCM(cm)  # This is the Final SCF object
mf.kernel(verbose=0)

print(">>>>> RUNNING AVAS")
avas_ = avas.AVAS(mf, ao_labels, with_iao=True, canonicalize=True, verbose=0)
avas_.kernel()
norb, ne_act, mo_avas = avas_.ncas, avas_.nelecas, avas_.mo_coeff

print(">>>>> STARTING CASCI")
mc_pcm = pyscf.mcscf.CASCI(mf, norb, ne_act).PCM(
    cm
)  # Make sure to decorate the CASCI object with PCM
mc_pcm.mo_coeff = mo_avas
# mc_pcm.max_memory = 140000

(CASCI_E, _, _, _, _) = mc_pcm.kernel(verbose=0)

print(f">>>>> CASCI_E: {CASCI_E}")
o_data = JSONEncoder().encode([float(CASCI_E)])

# JSON-safe package
save_result({"outputs": o_data})  # single JSON blob returned to client