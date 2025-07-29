from qiskit.primitives.sampler import Sampler
from qiskit.primitives.utils import init_circuit, final_measurement_mapping
from qiskit.exceptions import QiskitError
from .frontend import ion_pass_manager


class IonSampler(Sampler):
    """Qiskit primitive sampler for circuits compiled to ion gates."""

    def __init__(self, *, options=None):
        """
        Initializes a new IonSampler.

        :param dict options: Options to pass to parent Sampler class.
        """
        super().__init__(options=options)

    @staticmethod
    def _preprocess_circuit(circuit):
        """
        Processes input circuits before simulating them. Uses the ion pass manager to transpile
        the circuit to an ion gate set.

        :param qiskit.circuit.QuantumCircuit circuit: The circuit to process.
        :returns: The quantum circuit transpiled to ion gates.
        :rtype: qiskit.circuit.QuantumCircuit
        """
        circuit = init_circuit(circuit)

        # transpile to ion gates
        pm = ion_pass_manager()
        circuit = pm.run(circuits=circuit)

        q_c_mapping = final_measurement_mapping(circuit)
        if set(range(circuit.num_clbits)) != set(q_c_mapping.values()):
            raise QiskitError(
                "Some classical bits are not used for measurements."
                f" the number of classical bits ({circuit.num_clbits}),"
                f" the used classical bits ({set(q_c_mapping.values())})."
            )
        c_q_mapping = sorted((c, q) for q, c in q_c_mapping.items())
        qargs = [q for _, q in c_q_mapping]
        circuit = circuit.remove_final_measurements(inplace=False)
        return circuit, qargs


ion_sampler = IonSampler()


def get_ion_sampler():
    return ion_sampler
