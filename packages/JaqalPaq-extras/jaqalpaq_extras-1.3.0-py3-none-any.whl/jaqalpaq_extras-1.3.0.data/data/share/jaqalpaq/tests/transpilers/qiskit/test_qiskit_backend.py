import unittest
import pytest
from math import pi

qiskit = pytest.importorskip("qiskit")
try:
    from jaqalpaq.transpilers.qiskit import get_ion_sampler

    use_sampler = True
except ImportError:
    from jaqalpaq.transpilers.qiskit import get_ion_instance

    use_sampler = False

from qiskit.circuit import QuantumCircuit, QuantumRegister


class QiskitBackendTester(unittest.TestCase):
    def test_bell_pair_instance(self):
        qr = QuantumRegister(2)
        circ = QuantumCircuit(qr)
        circ.jaqalms(pi / 4, pi / 2, qr[0], qr[1])
        circ.measure_all()
        if use_sampler:
            sampler = get_ion_sampler()
            job = sampler.run(circ)
            result = job.result()
            dists = result.quasi_dists[0]
            self.assertAlmostEqual(dists[0], 0.5)
            self.assertAlmostEqual(dists[3], 0.5)
        else:
            instance = get_ion_instance()
            instance.set_config(shots=1024)
            result = instance.execute([circ])
            counts = result.get_counts()
            self.assertEqual(len(counts), 2)
            self.assertTrue("00" in counts)
            self.assertTrue("11" in counts)
