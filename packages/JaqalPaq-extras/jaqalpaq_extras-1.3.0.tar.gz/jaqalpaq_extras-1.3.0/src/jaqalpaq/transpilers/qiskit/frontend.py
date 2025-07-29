# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from jaqalpaq.core import CircuitBuilder, Macro
from jaqalpaq.core.circuitbuilder import UnscheduledBlockBuilder
from jaqalpaq.core.algorithm import expand_subcircuits, expand_macros
from jaqalpaq.core.algorithm.visitor import Visitor
from jaqalpaq.core.algorithm.fill_in_map import fill_in_map

# from qscoutlib import MSGate, QasmGate, IonUnroller
from qiskit.converters import dag_to_circuit, circuit_to_dag
from jaqalpaq.error import JaqalError

# from sympy.core.evalf import N
from numpy import pi
from qiskit.circuit.library.standard_gates.p import PhaseGate
from qiskit.circuit.library.standard_gates.r import RGate
from qiskit.circuit.library.standard_gates.x import CXGate
from qiskit.circuit.library.standard_gates.u import UGate
from qiskit.circuit.library.standard_gates.h import HGate
from qiskit.circuit.library.standard_gates.rxx import RXXGate
from qiskit.circuit import (
    QuantumRegister,
    QuantumCircuit,
    Parameter,
    EquivalenceLibrary,
)
from qiskit.circuit.library.standard_gates.equivalence_library import (
    StandardEquivalenceLibrary,
)
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.dagcircuit import DAGCircuit
import qiskit
from .gates import JaqalMSGate, SYGate, SYdgGate, JaqalRGate

qiskit_version = [int(part) for part in qiskit.__version__.split(".")]


_QISKIT_NAMES = {
    "jaqalr": "R",
    "sx": "Sx",
    "sxdg": "Sxd",
    "sy": "Sy",
    "sydg": "Syd",
    "s": "Sz",
    "sdg": "Szd",
    "x": "Px",
    "y": "Py",
    "z": "Pz",
    "rz": "Rz",
    "jaqalms": "MS",
    "sxx": "Sxx",
}

_PARAM_MAPS = {
    "*": lambda targets, args: args,
}


def jaqal_circuit_from_dag_circuit(dag):
    """
    Converts a Qiskit directed-acyclic-graph representation of a circuit to a
    :class:`jaqalpaq.core.Circuit`.
    See :func:`jaqal_circuit_from_qiskit_circuit` for details.

    :param qiskit.dagcircuit.DAGCircuit dag: The directed acyclic graph circuit to convert.
    :returns: The same quantum circuit, converted to JaqalPaq.
    :rtype: jaqalpaq.core.Circuit
    """
    return jaqal_circuit_from_qiskit_circuit(dag_to_circuit(dag))


def _get_register_info(circuit, target_qubit):
    """
    Gets information about a given target qubit in a circuit.

    :param qiskit.circuit.QuantumCircuit circuit: The circuit to search in.
    :param qiskit.circuit.quantumregister.Qubit target_qubit: The qubit to find.
    :returns: A tuple with the target name and index in the circuit.
    :rtype: tuple
    """
    if qiskit_version < [0, 45, 0]:
        reg_name = target_qubit.register.name
        qubit_index = target_qubit.index
        return reg_name, qubit_index
    reg = circuit.find_bit(target_qubit).registers[0]
    reg_name = reg[0].name
    qubit_index = reg[1]  # The index of the qubit w.r.t. to the register
    return reg_name, qubit_index


def jaqal_circuit_from_qiskit_circuit(
    circuit, names=None, native_gates=None, param_maps=None
):
    """
    Converts a Qiskit circuit or circuits to a :class:`jaqalpaq.core.Circuit`. The circuit
    will be structured into a sequence of unscheduled blocks. All instructions between one
    barrier statement and the next will be put into an unscheduled block together. If the
    :mod:`qscout.scheduler` is run on the circuit, as many as possible of those gates will
    be parallelized within each block, while maintaining the order of the blocks.
    Otherwise, the circuit will be treated as a fully sequential circuit.

    Measurement and reset commands are supported, but only if applied to every qubit in
    the circuit in immediate succession. If so, they will be mapped to a prepare_all or
    measure_all gate. If the circuit does not end with a measurement, then a measure_all
    gate will be appended to it.

    Circuits containing multiple quantum registers will be converted to circuits with a
    single quantum register, containing all the qubits from each register. The parts of
    that larger register that correspond to each of the original registers will be mapped
    with the appropriate names.

    :param qiskit.circuit.QuantumCircuit circuit: The circuit or list of circuits to convert.
    :param names: A mapping from names of Qiskit gates to the corresponding native Jaqal
        gate names. If omitted, maps jaqalr
        (:class:`jaqalpaq.transpilers.qiskit.JaqalRGate`), sx, sxdg, sy
        (:class:`jaqalpaq.qiskit.SYGate`), sydg (:class:`jaqalpaq.qiskit.SYdgGate`), s,
        sdg, x, y, z, rz, jaqalms (:class:`jaqalpaq.qiskit.JaqalMSGate`), and sxx
        (:class:`jaqalpaq.qiskit.SXXGate`) to their QSCOUT counterparts.
    :type names: dict or None
    :param native_gates: The native gate set to target. If None, target the QSCOUT native
        gates.
    :type native_gates: dict or None
    :returns: The same quantum circuit, converted to JaqalPaq.
    :rtype: jaqalpaq.core.Circuit
    :raises JaqalError: If any instruction acts on a qubit from a register other than the
        circuit's qregs.
    :raises JaqalError: If the circuit includes a snapshot instruction.
    :raises JaqalError: If the user tries to measure or reset only some of the qubits,
        rather than all of them.
    :raises JaqalError: If the circuit includes a gate not included in `names`.
    """
    # Preprocess input
    if isinstance(circuit, QuantumCircuit):
        largest_circuit = circuit
        circuit = [circuit]
    elif isinstance(circuit, list) and all(
        isinstance(c, QuantumCircuit) for c in circuit
    ):
        largest_circuit = max(circuit, key=lambda c: c.num_qubits)
    else:
        raise ValueError(
            "Input circuits must be a qiskit.QuantumCircuit or list of qiskit.QuantumCircuit objects."
        )
    num_circuits = len(circuit)

    if native_gates is None:
        from qscout.v1.std.jaqal_gates import ALL_GATES as native_gates
    n = largest_circuit.num_qubits
    qsc = CircuitBuilder(native_gates=native_gates)
    if names is None:
        names = _QISKIT_NAMES
    if param_maps is None:
        param_maps = _PARAM_MAPS
    baseregister = qsc.register("baseregister", n)
    registers = [{} for _ in range(num_circuits)]
    for circuit_idx in range(num_circuits):
        offset = 0
        for qreg in circuit[circuit_idx].qregs:
            qubit_register_name = (
                f"{qreg.name}_circ{circuit_idx}" if num_circuits > 1 else qreg.name
            )
            registers[circuit_idx][qreg.name] = qsc.map(
                qubit_register_name,
                baseregister,
                slice(offset, offset + qreg.size),
            )
            offset += qreg.size
    # We're going to divide the circuit up into blocks. Each block will contain every gate
    # between one barrier statement and the next. If the circuit is output with no further
    # processing, then the gates in each block will be run in sequence. However, if the
    # circuit is passed to the scheduler, it'll try to parallelize as many of the gates
    # within each block as possible, while keeping the blocks themselves sequential.
    for circuit_idx in range(num_circuits):
        block = UnscheduledBlockBuilder()
        qsc.expression.append(block.expression)
        block.gate("prepare_all")
        measure_accumulator = set()
        reset_accumulator = set()
        in_preamble = True
        for instr in circuit[circuit_idx].data:
            instr_name = (
                instr.operation.name if qiskit_version >= [0, 37, 0] else instr[0].name
            )
            if reset_accumulator:
                if instr_name == "reset":
                    target_qubit = instr[1][0]
                    name, index = _get_register_info(circuit[circuit_idx], target_qubit)
                    if name in registers[circuit_idx]:
                        reset_accumulator.add(
                            registers[circuit_idx][name].resolve_qubit(index)[1]
                        )
                    else:
                        raise JaqalError("Register %s invalid!" % name)
                    if len(reset_accumulator) == n:
                        block.gate("prepare_all")
                        reset_accumulator = {}
                    continue
                else:
                    raise JaqalError(
                        "Cannot reset only qubits %s and not whole register."
                        % reset_accumulator
                    )
                    # reset_accumulator = set()
            if measure_accumulator:
                if instr_name == "measure":
                    target_qubit = instr[1][0]
                    name, index = _get_register_info(circuit[circuit_idx], target_qubit)
                    if name in registers[circuit_idx]:
                        measure_accumulator.add(
                            registers[circuit_idx][name].resolve_qubit(index)[1]
                        )
                    else:
                        raise JaqalError("Register %s invalid!" % name)
                    if len(measure_accumulator) == n:
                        block.gate("measure_all")
                        measure_accumulator = {}
                    continue
                else:
                    raise JaqalError(
                        "Cannot measure only qubits %s and not whole register."
                        % reset_accumulator
                    )
                    # measure_accumulator = set()
            if instr_name == "measure":
                in_preamble = False
                target_qubit = instr[1][0]
                name, index = _get_register_info(circuit[circuit_idx], target_qubit)
                if name in registers[circuit_idx]:
                    measure_accumulator = {
                        registers[circuit_idx][name].resolve_qubit(index)[1]
                    }
                    if len(measure_accumulator) == n:
                        block.gate("measure_all")
                        measure_accumulator = {}
                    continue
                else:
                    raise JaqalError("Register %s invalid!" % name)
            elif instr_name == "reset":
                if not in_preamble:
                    target_qubit = instr[1][0]
                    name, index = _get_register_info(circuit[circuit_idx], target_qubit)
                    if name in registers[circuit_idx]:
                        reset_accumulator = {
                            registers[circuit_idx][name].resolve_qubit(index)[1]
                        }
                        if len(reset_accumulator) == n:
                            block.gate("prepare_all")
                            reset_accumulator = {}
                    else:
                        raise JaqalError("Register %s invalid!" % name)
            elif instr_name == "barrier":
                block = UnscheduledBlockBuilder()
                qsc.expression.append(block.expression)
                # Use barriers to inform the scheduler, as explained above.
            elif instr_name == "snapshot":
                raise JaqalError(
                    "Physical hardware does not support snapshot instructions."
                )
            elif instr_name in names:
                in_preamble = False
                if instr_name in param_maps:
                    param_map = param_maps[instr_name]
                else:
                    param_map = param_maps["*"]
                target_qubits = (
                    instr.qubits if qiskit_version >= [0, 37, 0] else instr[1]
                )
                for target_q in target_qubits:
                    name, _ = _get_register_info(circuit[circuit_idx], target_q)
                    if name not in registers[circuit_idx]:
                        raise JaqalError("Gate register %s invalid!" % name)
                block.gate(
                    names[instr_name],
                    *(
                        registers[circuit_idx][
                            _get_register_info(circuit[circuit_idx], target_q)[0]
                        ][_get_register_info(circuit[circuit_idx], target_q)[1]]
                        for target_q in target_qubits
                    ),
                    *param_map(
                        target_qubits, (float(param) for param in instr[0].params)
                    ),
                )
            else:
                raise JaqalError(
                    "Instruction %s not available on trapped ion hardware; try unrolling first."
                    % instr_name
                )
        block.gate("measure_all", no_duplicate=True)
    return qsc.build()


def qiskit_circuit_from_jaqal_circuit(circuit, names=None):
    """
    Converts a :class:`jaqalpaq.core.Circuit` to a Qiskit circuit. All scheduling
    information in the circuit will be lost in conversion.

    :param jaqalpaq.core.Circuit circuit: The circuit to convert.
    :param names: A mapping from names of native Jaqal gates to the corresponding Qiskit
        gate names. If omitted, maps R (:class:`jaqalpaq.transpilers.qiskit.JaqalRGate`),
        Sx, Sxd, Sy (:class:`jaqalpaq.qiskit.SYGate`), Syd
        (:class:`jaqalpaq.qiskit.SYdgGate`), Sz, Szd, Px, Py, Pz, Rz, MS
        (:class:`jaqalpaq.qiskit.JaqalMSGate`), and Sxx
        (:class:`jaqalpaq.qiskit.SXXGate`) to their Qiskit counterparts.
    :type names: dict or None
    :returns: The same quantum circuit, converted to Qiskit.
    :rtype: qiskit.circuit.QuantumCircuit
    """
    if names is None:
        names = {v: k for k, v in _QISKIT_NAMES.items()}

    qkr = {
        reg.name: QuantumRegister(size=reg.size, name=reg.name)
        for reg in circuit.registers.values()
        if reg.fundamental
    }
    expanded_circuit = fill_in_map(expand_subcircuits(expand_macros(circuit)))
    visitor = QiskitTranspilationVisitor()
    visitor.registers = qkr
    visitor.names = names
    return visitor.visit(expanded_circuit)


class QiskitTranspilationVisitor(Visitor):
    registers = {}
    names = {}

    def visit_default(self, obj, *args, **kwargs):
        return obj

    def visit_LoopStatement(self, obj, circ):
        subcirc = QuantumCircuit(*self.registers.values())
        circ.compose(
            self.visit(obj.statements, subcirc).repeat(obj.iterations), inplace=True
        )
        return circ

    def visit_BlockStatement(self, obj, circ):
        for stmt in obj.statements:
            self.visit(stmt, circ)
        return circ

    def visit_Circuit(self, obj, circ=None):
        circ = QuantumCircuit(*self.registers.values())
        return self.visit(obj.body, circ)

    def visit_GateStatement(self, obj, circ):
        # Note: The code originally checked if a gate was a native gate, macro, or neither,
        # and raised an exception if neither. This assumes everything not a macro is a native gate.
        # Note: This could be more elegant with a is_macro method on gates
        if isinstance(obj.gate_def, Macro):
            raise JaqalError("Expand macros before transpilation.")
        elif obj.name == "prepare_all":
            for reg in self.registers.values():
                circ.reset(reg)
        elif obj.name == "measure_all":
            circ.measure_all()
        else:
            classical_params = []
            quantum_params = []
            for pname, pval in obj.parameters.items():
                if pname in [
                    cparam.name for cparam in obj.gate_def.classical_parameters
                ]:
                    classical_params.append(self.visit(pval))
                else:
                    quantum_params.append(self.visit(pval))
            getattr(circ, self.names[obj.name])(*classical_params, *quantum_params)

    def visit_Parameter(self, obj):
        return self.visit(obj.resolve_value())

    def visit_NamedQubit(self, obj):
        reg, idx = obj.resolve_qubit()
        return self.registers[reg.name][idx]


def ion_equivalence_library():
    """
    Constructs a `qiskit.circuit.EquivalenceLibrary` containing a few standard identities
    for converting superconducting gates to equivalent sequences of trapped-ion gates.
    In particular, we use an implementation of the CNOT gate taken from Maslov (2017).
    This function is intended for internal use, but may be of utility to users designing
    their own transpilation protocols.

    :returns: The equivalence library.
    :rtype: qiskit.circuit.EquivalenceLibrary
    """
    el = EquivalenceLibrary(base=StandardEquivalenceLibrary)
    q1 = QuantumRegister(1, "q")
    q2 = QuantumRegister(2, "q")
    theta = Parameter("theta")
    phi = Parameter("phi")
    lam = Parameter("lam")

    circuit = QuantumCircuit(q1, global_phase=theta / 2)
    circuit.rz(theta, 0)
    el.set_entry(PhaseGate(theta), [circuit])

    circuit = QuantumCircuit(q1)
    circuit.jaqalr(phi, theta, 0)
    el.set_entry(RGate(theta, phi), [circuit])

    circuit = QuantumCircuit(q1)
    circuit.rz(lam, 0)
    circuit.jaqalr(pi / 2, theta, 0)
    circuit.rz(phi, 0)
    el.set_entry(UGate(theta, phi, lam), [circuit])

    circuit = QuantumCircuit(q1)
    circuit.z(0)
    circuit.sy(0)
    el.set_entry(HGate(), [circuit])

    circuit = QuantumCircuit(q2)
    circuit.jaqalms(0, theta, 0, 1)
    el.set_entry(RXXGate(theta), [circuit])

    # // controlled-NOT as per Maslov (2017); this implementation takes s = v = +1
    # gate cx a,b
    # {
    # ry(pi/2) a;
    # ms(pi/2, 0) a,b;
    # rx(-pi/2) a;
    # rx(-pi/2) b;
    # ry(-pi/2) a;
    # }
    circuit = QuantumCircuit(q2)
    circuit.sy(0)
    circuit.jaqalms(0, pi / 2, 0, 1)
    circuit.sxdg(0)
    circuit.sxdg(1)
    circuit.sydg(0)
    el.set_entry(CXGate(), [circuit])

    return el


class JaqalGateTranslator(TransformationPass):
    def __init__(
        self, el=ion_equivalence_library(), native_gates=list(_QISKIT_NAMES.keys())
    ):
        """
        Transformation pass that will translate a `qiskit.dagcircuit.DAGCircuit` into Jaqal's gateset.
        """
        super().__init__()
        self._equivalence_library = el
        self._native_gates = native_gates

    def run(self, dag, output_name=None, recursion=False):
        """
        Translate a `qiskit.dagcircuit.DAGCircuit` into an equivalent circuit using Jaqal's gateset.

        :returns: The translated quantum circuit.
        :rtype: qiskit.dagcircuit.DAGCircuit
        """
        equivalence_library = self._equivalence_library
        native_gates = self._native_gates + ["measure", "barrier"]

        new_dag = DAGCircuit()
        for qreg in dag.qregs.values():
            new_dag.add_qreg(qreg)
        for creg in dag.cregs.values():
            new_dag.add_creg(creg)

        for layer in dag.serial_layers():
            subdag = layer["graph"]

            for gate in subdag.op_nodes(include_directives=True):
                if gate.op.name in native_gates:
                    new_dag.apply_operation_back(
                        gate.op, qargs=gate.qargs, cargs=gate.cargs
                    )
                    continue

                equivalence = equivalence_library.get_entry(gate.op)
                if len(equivalence) == 0:
                    raise Exception(f"No Jaqal equivalence found for {gate.op}")
                new_dag.compose(
                    circuit_to_dag(equivalence[0]), qubits=gate.qargs, clbits=gate.cargs
                )

        out_basis = set(new_dag.count_ops().keys())
        # if recursion didn't produce new changes, return
        if recursion and new_dag == dag:
            return new_dag
        # if basis is not native basis, run pass again
        elif not out_basis.issubset(native_gates):
            new_dag = self.run(new_dag, recursion=True)

        if output_name:
            new_dag.name = output_name
        return new_dag


def ion_pass_manager():
    """
    Constructs a `qiskit.transpiler.PassManager` that will unroll a circuit into the
    QSCOUT standard gate set. Pass a `qiskit.circuit.Circuit` object into its `run` method
    to perform the unrolling.

    :returns: The pass manager.
    :rtype: qiskit.transpiler.PassManager
    """
    pm = PassManager()
    pm.append(JaqalGateTranslator())
    return pm
