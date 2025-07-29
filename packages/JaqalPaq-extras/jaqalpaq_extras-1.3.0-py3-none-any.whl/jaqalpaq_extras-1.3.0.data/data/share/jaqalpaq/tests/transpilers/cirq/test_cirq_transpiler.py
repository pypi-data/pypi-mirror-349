import unittest
import pytest
import textwrap
from math import pi
import numpy as np

from jaqalpaq.error import JaqalError
from jaqalpaq.generator import generate_jaqal_program
from jaqalpaq.core import CircuitBuilder
from jaqalpaq.run import run_jaqal_string

cirq = pytest.importorskip("cirq")
from jaqalpaq.transpilers.cirq import jaqal_circuit_from_cirq_circuit


cirq_version = [int(part) for part in cirq.__version__.split(".")]
if cirq_version >= [1]:
    from jaqalpaq.transpilers.cirq import QSCOUTTargetGateset


class CirqTranspilerTester(unittest.TestCase):
    def expected_jcirc(self) -> CircuitBuilder:
        jcirc = CircuitBuilder()
        reg = jcirc.register("allqubits", 2)
        jcirc.gate("prepare_all")
        jcirc.gate("R", reg[0], pi, pi)
        jcirc.gate("MS", reg[0], reg[1], 0, pi / 2)
        block = jcirc.block(True)
        block.gate("R", reg[0], -1.5707963267948972, pi / 2)
        # Last few digits are off if we just use -pi/2
        block.gate("R", reg[1], pi, pi / 2)
        jcirc.gate("Rz", reg[0], -pi / 2)
        jcirc.gate("measure_all")
        return jcirc

    def _assert_statevector(self, jp1, jp2) -> None:
        expected_result = run_jaqal_string(
            "from qscout.v1.std usepulses *" + "\n \n" + jp1
        )
        actual_result = run_jaqal_string(
            "from qscout.v1.std usepulses *" + "\n \n" + jp2
        )

        expected_sv = expected_result.by_time[0]._subcircuit._tree.state_vector
        actual_sv = actual_result.by_time[0]._subcircuit._tree.state_vector
        assert np.allclose(actual_sv, actual_sv)

        expected_sv /= expected_sv[0] / np.abs(expected_sv[0])
        actual_sv /= actual_sv[0] / np.abs(actual_sv[0])
        assert np.allclose(actual_sv, actual_sv)

    def test_transpile_line_circuit(self) -> None:
        circuit = cirq.Circuit()
        qubits = cirq.LineQubit.range(2)
        circuit += cirq.H(qubits[0])
        circuit += cirq.CNOT(*qubits)

        if cirq_version >= [1]:
            ic = cirq.optimize_for_target_gateset(
                circuit, gateset=QSCOUTTargetGateset()
            )
        else:
            ic = cirq.ConvertToIonGates().convert_circuit(circuit)

        if cirq_version >= [1, 1]:
            cirq.testing.assert_circuits_have_same_unitary_given_final_permutation(
                circuit, ic, {q: q for q in circuit.all_qubits()}
            )

        ic.append(
            cirq.measure_each(*qubits),
            strategy=cirq.circuits.InsertStrategy.NEW_THEN_INLINE,
        )

        jc = jaqal_circuit_from_cirq_circuit(ic)
        jcirc = self.expected_jcirc()

        if cirq_version >= [1]:
            cirq.testing.assert_has_diagram(
                ic,
                textwrap.dedent(
                    """
                0: ───PhX(1)───MS(0.25π)───PhX(-0.5)^0.5───S^-1───M───
                               │
                1: ────────────MS(0.25π)───PhX(1)^0.5─────────────M───
                """
                ),
            )

        actual_jaqal_program = generate_jaqal_program(jc)
        expected_jaqal_program = generate_jaqal_program(jcirc.build())
        self.assertEqual(actual_jaqal_program.split(), expected_jaqal_program.split())
        self._assert_statevector(actual_jaqal_program, expected_jaqal_program)

    def test_jaqal_circuit_from_cirq_circuit(self) -> None:
        circuit = cirq.Circuit()
        qubits = cirq.GridQubit(0, 0), cirq.GridQubit(0, 1)
        circuit += cirq.H(qubits[0])
        circuit += cirq.CNOT(*qubits)

        class FailingOperation(cirq.Operation):
            """A mock operation that cannot be compiled to."""

            def __init__(self, qubits):
                self._qubits = qubits

            @property
            def qubits(self):
                return self._qubits

            def with_qubits(self, *new_qubits):
                return FailingOperation(new_qubits)

        # Test both `JaqalErrors`
        with pytest.raises(JaqalError, match="to QSCOUT gates before compiling."):
            jaqal_circuit_from_cirq_circuit(circuit)

        with pytest.raises(JaqalError, match="Cannot compile operation"):
            fail_circuit = cirq.Circuit()
            qubit = cirq.LineQubit.range(1)
            fail_circuit.append(FailingOperation(qubit))
            jaqal_circuit_from_cirq_circuit(fail_circuit)

        # Test the `need_prep` flag + empty moment
        expected_jaqal_program = textwrap.dedent(
            """\
            register allqubits[0]
                """
        )
        empty_circ = cirq.Circuit()
        empty_circ += cirq.Moment()
        empty_jaqal_circuit = jaqal_circuit_from_cirq_circuit(empty_circ)
        assert (
            generate_jaqal_program(empty_jaqal_circuit).split()
            == expected_jaqal_program.split()
        )

        circuit = cirq.Circuit()
        qubits = cirq.NamedQubit.range(2, prefix="q_")
        circuit += cirq.H(qubits[0])
        circuit += cirq.CNOT(*qubits)
        if cirq_version >= [1]:
            ccirc = cirq.optimize_for_target_gateset(
                circuit, gateset=QSCOUTTargetGateset()
            )
            jc = jaqal_circuit_from_cirq_circuit(ccirc)
            jcirc = self.expected_jcirc()

        if cirq_version < [1]:
            ic = cirq.ConvertToIonGates().convert_circuit(circuit)
            jc = jaqal_circuit_from_cirq_circuit(ic)
            jcirc = self.expected_jcirc()

        self.assertEqual(
            generate_jaqal_program(jcirc.build()), generate_jaqal_program(jc)
        )

    if cirq_version >= [1]:

        def test_zz_gate_circuit(self) -> None:
            circuit = cirq.Circuit()
            qubits = cirq.LineQubit.range(3)
            circuit += cirq.S(qubits[0])
            circuit += cirq.H(qubits[1])
            circuit += cirq.ZZPowGate(exponent=1 / 2).on(qubits[1], qubits[2])
            circuit += cirq.H(qubits[0])
            compiled_circuit = cirq.optimize_for_target_gateset(
                circuit, gateset=QSCOUTTargetGateset()
            )
            if cirq_version >= [1, 1]:
                cirq.testing.assert_circuits_have_same_unitary_given_final_permutation(
                    circuit, compiled_circuit, {q: q for q in circuit.all_qubits()}
                )
            cirq.testing.assert_has_diagram(
                compiled_circuit,
                textwrap.dedent(
                    """
                0: ───PhX(1)^0.5──────S^-1────────────

                1: ───PhX(-0.5)^0.5───Z──────ZZ───────
                                             │
                2: ──────────────────────────ZZ^0.5───
                """
                ),
            )

    def test_multi_circuit(self):
        # Test GHZ
        q = cirq.LineQubit.range(4)
        circuit_1 = cirq.Circuit(cirq.H(q[0]))
        for i in range(len(q) - 1):
            circuit_1 += cirq.CNOT(q[i], q[i + 1])

        # Test Bell
        q = cirq.LineQubit.range(2)
        circuit_2 = cirq.Circuit()
        circuit_2 += cirq.H(q[0])
        circuit_2 += cirq.CNOT(*q)

        # Test arbitrary circuit
        qubits = cirq.LineQubit.range(3)
        circuit_3 = cirq.Circuit(
            cirq.H(qubits[0]),
            cirq.X(qubits[0]) ** 0.5,
            cirq.CNOT(qubits[1], qubits[0]),
            cirq.S(qubits[0]),
        )

        clist = [circuit_1, circuit_2, circuit_3]
        if cirq_version >= [1]:
            converted_circuits = [
                cirq.optimize_for_target_gateset(c, gateset=QSCOUTTargetGateset())
                for c in clist
            ]
        else:
            converted_circuits = [
                cirq.ConvertToIonGates().convert_circuit(c) for c in clist
            ]

        jaqal_circuit_list = [
            jaqal_circuit_from_cirq_circuit(c) for c in converted_circuits
        ]
        single_jaqal_circuit = jaqal_circuit_from_cirq_circuit(converted_circuits)

        single_jaqal_program = generate_jaqal_program(single_jaqal_circuit)
        jaqal_program_list = [generate_jaqal_program(jc) for jc in jaqal_circuit_list]

        # Remove header info
        modified_single_jaqal_program = "\n".join(single_jaqal_program.split("\n")[2:])
        modified_jaqal_program_list = [
            "\n".join(jp.split("\n")[2:]) for jp in jaqal_program_list
        ]

        self.assertEqual(
            (
                modified_jaqal_program_list[0]
                + modified_jaqal_program_list[1]
                + modified_jaqal_program_list[2]
            ),
            modified_single_jaqal_program,
        )

        expected_jaqal_program = textwrap.dedent(
            """\
            register allqubits[4]

            prepare_all
            R allqubits[0] 3.141592653589793 3.141592653589793
            MS allqubits[0] allqubits[1] 0 1.5707963267948966
            <
                R allqubits[0] -1.5707963267948972 1.5707963267948966
                R allqubits[1] 1.5707963267948966 1.5707963267948966
            >
            <
                Rz allqubits[0] -1.5707963267948966
                Rz allqubits[1] 1.5707963267948966
            >
            MS allqubits[1] allqubits[2] 0 1.5707963267948966
            <
                R allqubits[1] -1.5707963267948972 1.5707963267948966
                R allqubits[2] 1.5707963267948966 1.5707963267948966
            >
            <
                Rz allqubits[1] -1.5707963267948966
                Rz allqubits[2] 1.5707963267948966
            >
            MS allqubits[2] allqubits[3] 0 1.5707963267948966
            <
                R allqubits[2] -1.5707963267948972 1.5707963267948966
                R allqubits[3] 3.141592653589793 1.5707963267948966
            >
            Rz allqubits[2] -1.5707963267948966
            measure_all
            prepare_all
            R allqubits[0] 3.141592653589793 3.141592653589793
            MS allqubits[0] allqubits[1] 0 1.5707963267948966
            <
                R allqubits[0] -1.5707963267948972 1.5707963267948966
                R allqubits[1] 3.141592653589793 1.5707963267948966
            >
            Rz allqubits[0] -1.5707963267948966
            measure_all
            prepare_all
            <
                R allqubits[0] 3.141592653589793 1.5707963267948966
                R allqubits[1] 1.5707963267948966 1.5707963267948966
            >
            Rz allqubits[0] -1.5707963267948966
            MS allqubits[1] allqubits[0] 0 1.5707963267948966
            <
                R allqubits[0] 3.141592653589793 1.5707963267948966
                R allqubits[1] -1.5707963267948972 1.5707963267948966
            >
            <
                Rz allqubits[0] 1.5707963267948966
                Rz allqubits[1] -1.5707963267948966
            >
            measure_all
            """
        )
        assert single_jaqal_program.split() == expected_jaqal_program.split()

    def test_multi_circuit_error(self):
        invalid_ccirc = [cirq.Circuit(), [cirq.Circuit(), cirq.Circuit()]]
        with pytest.raises(ValueError, match="Input circuits must be"):
            jaqal_circuit_from_cirq_circuit(invalid_ccirc)
