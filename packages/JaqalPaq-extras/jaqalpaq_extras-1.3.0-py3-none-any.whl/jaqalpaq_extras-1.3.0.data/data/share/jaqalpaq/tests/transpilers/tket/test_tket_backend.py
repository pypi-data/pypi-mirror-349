import unittest
import pytest

pytket = pytest.importorskip("pytket")
from jaqalpaq.transpilers.tket import JaqalBackend
from pytket import Circuit


class PytketBackendTester(unittest.TestCase):
    def test_prepare_bell_pairs(self):
        circ = Circuit(2, 2)
        circ.H(1).CX(1, 0).measure_all()
        jb = JaqalBackend("emulator")
        compiled = jb.get_compiled_circuit(circ)
        handle = jb.process_circuit(compiled, n_shots=16)
        for shot in jb.get_result(handle).get_shots():
            self.assertEqual(shot[0], shot[1])
