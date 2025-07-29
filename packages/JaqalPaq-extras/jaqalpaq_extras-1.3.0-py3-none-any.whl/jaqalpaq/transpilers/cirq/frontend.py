# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from jaqalpaq.core import CircuitBuilder
from jaqalpaq.error import JaqalError

import numpy as np
import cirq


def _CIRQ_NAMES():
    """(cached) Mapping of Cirq gates to Jaqal-compatible functions."""
    global _CIRQ_NAMES_cache
    try:
        return _CIRQ_NAMES_cache
    except NameError:
        pass

    from cirq import (
        XXPowGate,
        XPowGate,
        YPowGate,
        ZPowGate,
        ZZPowGate,
        PhasedXPowGate,
    )

    _CIRQ_NAMES_cache = {
        XXPowGate: (lambda g, q1, q2: ("MS", q1, q2, 0, g.exponent * np.pi)),
        XPowGate: (lambda g, q: ("R", q, 0, g.exponent * np.pi)),
        YPowGate: (lambda g, q: ("R", q, np.pi / 2, g.exponent * np.pi)),
        ZPowGate: (lambda g, q: ("Rz", q, g.exponent * np.pi)),
        PhasedXPowGate: (
            lambda g, q: ("R", q, g.phase_exponent * np.pi, g.exponent * np.pi)
        ),
        ZZPowGate: (lambda g, q1, q2: ("ZZ", q1, q2, g.exponent * np.pi)),
    }
    return _CIRQ_NAMES_cache


def jaqal_circuit_from_cirq_circuit(ccirc, names=None, native_gates=None):
    """Converts ``cirq.Circuit`` object(s) to a :class:`jaqalpaq.core.Circuit`.

    The circuit(s) will be structured as a sequence of parallel blocks, one for each Cirq
    Moment in the input.

    Measurements are supported, but only if applied to every qubit in the circuit in the
    same moment. If so, they will be mapped to a measure_all gate. If the measure_all gate
    is not the last gate in the circuit, a prepare_all gate will be inserted after it.
    Additionally, a prepare_all gate will be inserted before the first moment. If the
    circuit does not end with a measurement, then a measure_all gate will be appended.

    All active qubits in the circuit will be mapped onto hardware in the sorted order given by
    `ccirc.all_qubits()`.

    :param cirq.Circuit ccirc: The Circuit or list of circuits to convert.
    :param names: A mapping from Cirq gate classes to the corresponding native Jaqal gate
        names. If omitted, maps ``cirq.XXPowGate``, ``cirq.XPowGate``, ``cirq.YPowGate``,
        ``cirq.ZPowGate``, and ``cirq.PhasedXPowGate`` to their QSCOUT counterparts. The
        ``cirq.ConvertToIonGates`` or ``cirq.optimize_for_target_gateset`` function
        will transpile a circuit into this basis.
    :type names: dict or None
    :param native_gates: The native gate set to target. If None, target the QSCOUT native gates.
    :type native_gates: dict or None
    :returns: The same quantum circuit(s), converted to JaqalPaq.
    :rtype: Circuit
    :raises JaqalError: If the circuit(s) includes a gate not included in `names`.
    """
    from cirq import MeasurementGate

    if isinstance(ccirc, cirq.Circuit):
        largest_circuit = ccirc
        ccirc = [ccirc]
    elif isinstance(ccirc, list) and all(
        isinstance(circ, cirq.Circuit) for circ in ccirc
    ):
        largest_circuit = max(
            ccirc, key=lambda x: len(x.all_qubits())
        )  # `allqubits` will be determined by the max of all of the subcircuit's required registers
    else:
        raise ValueError(
            "Input circuits must be a cirq.Circuit or list of cirq.Circuit objects."
        )

    if native_gates is None:
        from qscout.v1.std.jaqal_gates import ALL_GATES as native_gates
    builder = CircuitBuilder(native_gates=native_gates)
    if names is None:
        names = _CIRQ_NAMES()

    allqubits = builder.register("allqubits", len(largest_circuit.all_qubits()))
    for compiled_circuit in ccirc:
        sorted_ccirc_qubits = sorted(compiled_circuit.all_qubits())
        qubitmap = {sorted_ccirc_qubits[i]: i for i in range(len(sorted_ccirc_qubits))}
        need_prep = True

        for moment in compiled_circuit:
            if len(moment) == 0:
                continue
            if need_prep:
                builder.gate("prepare_all")
                need_prep = False

            meas_condition = all([op.gate for op in moment]) and all(
                [isinstance(op.gate, MeasurementGate) for op in moment]
            )
            if meas_condition:
                builder.gate("measure_all")
                need_prep = True
                continue
            else:
                need_prep = False
            if len(moment) > 1:
                block = builder.block(parallel=True)
                # Note: If you tell Cirq you want MS gates in parallel, we'll generate a Jaqal
                # file with exactly that, never mind that QSCOUT can't execute it.
            else:
                block = builder
            sorted_moment = sorted(moment, key=lambda m: m.qubits)
            # `sorted()` used here for compatibility with older transpilation w.r.t. to qubit order in a given moment
            for op in sorted_moment:
                if op.gate:
                    gate_type = None
                    for name in names:
                        if isinstance(op.gate, name):
                            gate_type = name
                            break
                    if gate_type:
                        targets = [allqubits[qubitmap[qb]] for qb in op.qubits]
                        block.gate(*names[gate_type](op.gate, *targets))
                    else:
                        raise JaqalError(
                            "Convert %s to QSCOUT gates before compiling."
                            % str(type(op.gate))
                        )
                else:
                    raise JaqalError("Cannot compile operation %s." % op)
        if not need_prep:
            # If we just measured, or the circuit is empty, don't add a final measurement.
            builder.gate("measure_all")
    return builder.build()


cirq_version = [int(part) for part in cirq.__version__.split(".")]
if cirq_version >= [1]:

    class QSCOUTTargetGateset(cirq.TwoQubitCompilationTargetGateset):
        """Defines the QSCOUT gateset for Cirq."""

        def __init__(self):
            """Constructor for `QSCOUTTargetGateset` specifying the basis gateset."""
            super().__init__(
                cirq.XXPowGate,
                cirq.MeasurementGate,
                cirq.XPowGate,
                cirq.YPowGate,
                cirq.ZPowGate,
                cirq.PhasedXPowGate,
                cirq.ZZPowGate,
                unroll_circuit_op=False,
            )

        def decompose_to_target_gateset(self, op, moment_idx):
            """Protocols to follow to perform decompositions to the gateset.

            :param op: The gate operation to be decomposed.
            :type op: cirq.Operation.
            :param moment_idx: The index of `op` in the circuit.
            :type moment_idx: int
            :returns: A ``cirq.OP_TREE`` with `op` decomposed to the gateset.
            :rtype: cirq.protocols.decompose_protocol.DecomposeResult.
            """
            if not 1 <= cirq.protocols.num_qubits(op) <= 2:
                return self._decompose_multi_qubit_operation(op, moment_idx)
            if cirq.protocols.num_qubits(op) == 1:
                return self._decompose_single_qubit_operation(op, moment_idx)
            else:
                return self._decompose_two_qubit_operation(op, moment_idx)

        def _decompose_single_qubit_operation(self, op, moment_idx):
            """Specifies how to decompose a single-qubit gates to the gateset.

            :param op: The gate operation to be decomposed.
            :type op: cirq.Operation.
            :param moment_idx: The index of `op` in the circuit.
            :type moment_idx: int
            :returns: A ``cirq.OP_TREE`` with `op` decomposed to the gateset.
            :rtype: cirq.protocols.decompose_protocol.DecomposeResult.
            """
            if isinstance(op.gate, cirq.HPowGate) and op.gate.exponent == 1:
                return [
                    cirq.rx(np.pi).on(op.qubits[0]),
                    cirq.ry(-1 * np.pi / 2).on(op.qubits[0]),
                ]
            if cirq.has_unitary(op):
                gates = cirq.single_qubit_matrix_to_phased_x_z(cirq.unitary(op))
                return [g.on(op.qubits[0]) for g in gates]
            return NotImplemented

        def _decompose_two_qubit_operation(self, op, moment_idx):
            """Specifies how to decompose a two-qubit gates to the gateset.

            :param op: The gate operation to be decomposed.
            :type op: cirq.Operation.
            :param moment_idx: The index of `op` in the circuit.
            :type moment_idx: int
            :returns: A ``cirq.OP_TREE`` with `op` decomposed to the gateset.
            :rtype: cirq.protocols.decompose_protocol.DecomposeResult.
            """
            if isinstance(op.gate, cirq.CNotPowGate) and op.gate.exponent == 1:
                return [
                    cirq.ry(np.pi / 2).on(op.qubits[0]),
                    cirq.ms(np.pi / 4).on(op.qubits[0], op.qubits[1]),
                    cirq.rx(-1 * np.pi / 2).on(op.qubits[0]),
                    cirq.rx(-1 * np.pi / 2).on(op.qubits[1]),
                    cirq.ry(-1 * np.pi / 2).on(op.qubits[0]),
                ]
            if cirq.has_unitary(op):
                return cirq.two_qubit_matrix_to_ion_operations(
                    op.qubits[0], op.qubits[1], cirq.unitary(op)
                )
            return NotImplemented

        @property
        def preprocess_transformers(self):
            return []

        @property
        def postprocess_transformers(self):
            return [
                cirq.align_left,
                cirq.synchronize_terminal_measurements,
                cirq.merge_single_qubit_gates_to_phased_x_and_z,
                cirq.drop_negligible_operations,
                cirq.drop_empty_moments,
            ]
