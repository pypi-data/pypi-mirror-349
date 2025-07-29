# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from .frontend import (
    jaqal_circuit_from_dag_circuit,
    jaqal_circuit_from_qiskit_circuit,
    qiskit_circuit_from_jaqal_circuit,
    ion_pass_manager,
)
from .gates import JaqalMSGate, SYGate, SYdgGate, JaqalRGate

__all__ = [
    "jaqal_circuit_from_dag_circuit",
    "jaqal_circuit_from_qiskit_circuit",
    "qiskit_circuit_from_jaqal_circuit",
    "ion_pass_manager",
    "JaqalMSGate",
    "SYGate",
    "SYdgGate",
    "JaqalRGate",
]

try:
    from .sampler import get_ion_sampler

    __all__ += ["get_ion_sampler"]
except Exception as ex:
    from .instance import get_ion_instance

    __all__ += ["get_ion_instance"]
