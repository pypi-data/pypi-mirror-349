import unittest
import pytest
import textwrap
from jaqalpaq.core import CircuitBuilder
from jaqalpaq.generator import generate_jaqal_program

qiskit = pytest.importorskip("qiskit")
from jaqalpaq.transpilers.qiskit import (
    jaqal_circuit_from_qiskit_circuit,
    jaqal_circuit_from_dag_circuit,
    ion_pass_manager,
)
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.converters.circuit_to_dag import circuit_to_dag


class QiskitTranspilerTester(unittest.TestCase):
    def test_transpile_1q_circuit(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(2)
        circ = QuantumCircuit(qr, cr)
        circ.x(qr[0])
        circ.measure(qr[0], cr[0])
        circ.barrier(qr[0])
        circ.reset(qr[0])
        circ.y(qr[0])
        circ.measure(qr[0], cr[1])
        jcirc = CircuitBuilder()
        reg1 = jcirc.register("baseregister", 1)
        reg2 = jcirc.map(qr.name, reg1, slice(0, 1, 1))
        block = jcirc.block()
        block.gate("prepare_all")
        block.gate("Px", reg2[0])
        block.gate("measure_all")
        block = jcirc.block()
        block.gate("prepare_all")
        block.gate("Py", reg2[0])
        block.gate("measure_all")
        self.assertEqual(
            generate_jaqal_program(jcirc.build()),
            generate_jaqal_program(jaqal_circuit_from_qiskit_circuit(circ)),
        )

    def test_transpile_2q_circuit(self):
        qr = QuantumRegister(2)
        cr = ClassicalRegister(4)
        circ = QuantumCircuit(qr, cr)
        circ.x(qr[0])
        circ.measure(qr[0], cr[0])
        circ.measure(qr[1], cr[1])
        circ.barrier()
        circ.reset(qr[0])
        circ.reset(qr[1])
        circ.barrier()
        circ.y(qr[0])
        dag = circuit_to_dag(circ)
        jcirc = CircuitBuilder()
        reg1 = jcirc.register("baseregister", 2)
        reg2 = jcirc.map(qr.name, reg1, slice(0, 2, 1))
        block = jcirc.block()
        block.gate("prepare_all")
        block.gate("Px", reg2[0])
        block.gate("measure_all")
        block = jcirc.block()
        block.gate("prepare_all")
        block = jcirc.block()
        block.gate("Py", reg2[0])
        block.gate("measure_all")
        self.assertEqual(
            generate_jaqal_program(jcirc.build()),
            generate_jaqal_program(jaqal_circuit_from_dag_circuit(dag)),
        )

    def test_multi_circuit(self):
        # Test GHZ
        qc1 = QuantumCircuit(4)
        qc1.h(0)
        for i in range(3):
            qc1.cx(i, i + 1)

        # Test Bell
        qc2 = QuantumCircuit(2)
        qc2.h(0)
        qc2.cx(0, 1)

        # Test arbitrary circuit
        qr1 = QuantumRegister(1, "reg0")
        qr2 = QuantumRegister(2, "reg1")
        qc3 = QuantumCircuit(qr1, qr2)  # test multiple registers in a circuit
        qc3.h(qr1[0])
        qc3.sx(qr2[0])
        qc3.cx(qr2[0], qr1[0])
        qc3.s(qr1[0])

        qc_list = [qc1, qc2, qc3]
        converted_circuits = [ion_pass_manager().run(qc) for qc in qc_list]
        jaqal_circuits = [
            jaqal_circuit_from_qiskit_circuit(qc) for qc in converted_circuits
        ]
        single_jaqal_circuit = jaqal_circuit_from_qiskit_circuit(converted_circuits)

        jaqal_programs = [generate_jaqal_program(jc) for jc in jaqal_circuits]
        single_jaqal_program = generate_jaqal_program(single_jaqal_circuit)

        modified_single_jaqal_program = "\n".join(single_jaqal_program.split("\n")[7:])
        # replace registers names because they increment when input is a list
        modified_jaqal_program_list = [
            "\n".join(jaqal_programs[0].split("\n")[4:]).replace("q", "q_circ0"),
            "\n".join(jaqal_programs[1].split("\n")[4:]).replace("q", "q_circ1"),
            "\n".join(jaqal_programs[2].split("\n")[5:])
            .replace("reg0", "reg0_circ2")
            .replace("reg1", "reg1_circ2"),
        ]  # extra line for last circuit from using two registers

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
            register baseregister[4]

            map q_circ0 baseregister[0:4:1]
            map q_circ1 baseregister[0:2:1]
            map reg0_circ2 baseregister[0:1:1]
            map reg1_circ2 baseregister[1:3:1]

            {
                prepare_all
                Pz q_circ0[0]
                Sy q_circ0[0]
                Sy q_circ0[0]
                MS q_circ0[0] q_circ0[1] 0.0 1.5707963267948966
                Sxd q_circ0[0]
                Syd q_circ0[0]
                Sxd q_circ0[1]
                Sy q_circ0[1]
                MS q_circ0[1] q_circ0[2] 0.0 1.5707963267948966
                Sxd q_circ0[1]
                Syd q_circ0[1]
                Sxd q_circ0[2]
                Sy q_circ0[2]
                MS q_circ0[2] q_circ0[3] 0.0 1.5707963267948966
                Sxd q_circ0[2]
                Syd q_circ0[2]
                Sxd q_circ0[3]
                measure_all
            }
            {
                prepare_all
                Pz q_circ1[0]
                Sy q_circ1[0]
                Sy q_circ1[0]
                MS q_circ1[0] q_circ1[1] 0.0 1.5707963267948966
                Sxd q_circ1[0]
                Syd q_circ1[0]
                Sxd q_circ1[1]
                measure_all
            }
            {
                prepare_all
                Pz reg0_circ2[0]
                Sy reg0_circ2[0]
                Sx reg1_circ2[0]
                Sy reg1_circ2[0]
                MS reg1_circ2[0] reg0_circ2[0] 0.0 1.5707963267948966
                Sxd reg0_circ2[0]
                Sz reg0_circ2[0]
                Sxd reg1_circ2[0]
                Syd reg1_circ2[0]
                measure_all
            }
            """
        )
        assert single_jaqal_program.split() == expected_jaqal_program.split()

    def test_multi_circuit_error(self):
        invalid_ccirc = [QuantumCircuit(1), [QuantumCircuit(2), QuantumCircuit(3)]]
        with pytest.raises(ValueError, match="Input circuits must be"):
            jaqal_circuit_from_qiskit_circuit(invalid_ccirc)
