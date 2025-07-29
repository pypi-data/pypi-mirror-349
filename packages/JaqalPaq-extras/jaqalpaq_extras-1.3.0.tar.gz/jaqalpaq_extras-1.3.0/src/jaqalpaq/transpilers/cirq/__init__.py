# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
import cirq
from .frontend import jaqal_circuit_from_cirq_circuit

cirq_version = [int(part) for part in cirq.__version__.split(".")]

if cirq_version >= [1]:
    from .frontend import QSCOUTTargetGateset

    __all__ = ["jaqal_circuit_from_cirq_circuit", "QSCOUTTargetGateset"]
else:
    __all__ = ["jaqal_circuit_from_cirq_circuit"]
