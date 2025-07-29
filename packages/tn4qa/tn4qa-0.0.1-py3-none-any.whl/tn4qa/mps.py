import copy
from typing import List, TypeAlias, Union

# Underlying tensor objects can either be NumPy arrays or Sparse arrays
import numpy as np
import sparse
from numpy import ndarray

# Qiskit quantum circuit integration
from qiskit import QuantumCircuit
from sparse import SparseArray

from .mpo import MatrixProductOperator
from .tensor import Tensor
from .tn import TensorNetwork

# Visualisation
from .visualisation import draw_mps

DataOptions: TypeAlias = Union[ndarray, SparseArray]


class MatrixProductState(TensorNetwork):
    def __init__(self, tensors: List[Tensor], shape: str = "udp") -> None:
        """
        Constructor for MatrixProductState class.

        Args:
            tensors: List of tensors to form the MPS.
            shape (optional): The order of the indices for the tensors. Default is 'udp' (up, down, physical)

        Returns
            An MPS.
        """
        super().__init__(tensors, "MPS")
        self.num_sites = len(tensors)
        self.shape = shape

        internal_inds = self.get_internal_indices()
        external_inds = self.get_external_indices()
        bond_dims = []
        physical_dims = []
        for idx in internal_inds:
            bond_dims.append(self.get_dimension_of_index(idx))
        for idx in external_inds:
            physical_dims.append(self.get_dimension_of_index(idx))
        self.bond_dimension = max(bond_dims)
        self.physical_dimension = max(physical_dims)

    @classmethod
    def from_arrays(
        cls, arrays: List[DataOptions], shape: str = "udp"
    ) -> "MatrixProductState":
        """
        Create an MPS from a list of arrays.

        Args:
            arrays: The list of arrays.
            shape (optional): The order of the indices for the tensors. Default is 'udp' (up, down, physical)

        Returns:
            An MPS.
        """
        tensors = []

        first_shape = shape.replace("u", "")
        physical_idx_pos = first_shape.index("p")
        virtual_input_idx_pos = first_shape.index("d")
        first_indices = ["", ""]
        first_indices[physical_idx_pos] = "P1"
        first_indices[virtual_input_idx_pos] = "B1"
        first_tensor = Tensor(arrays[0], first_indices, ["MPS_T1"])
        tensors.append(first_tensor)

        physical_idx_pos = shape.index("p")
        virtual_output_idx_pos = shape.index("u")
        virtual_input_idx_pos = shape.index("d")
        for a_idx in range(1, len(arrays) - 1):
            a = arrays[a_idx]
            indices_k = ["", "", ""]
            indices_k[physical_idx_pos] = f"P{a_idx+1}"
            indices_k[virtual_output_idx_pos] = f"B{a_idx}"
            indices_k[virtual_input_idx_pos] = f"B{a_idx+1}"
            tensor_k = Tensor(a, indices_k, [f"MPS_T{a_idx+1}"])
            tensors.append(tensor_k)

        last_shape = shape.replace("d", "")
        physical_idx_pos = last_shape.index("p")
        virtual_output_idx_pos = last_shape.index("u")
        last_indices = ["", ""]
        last_indices[physical_idx_pos] = f"P{len(arrays)}"
        last_indices[virtual_output_idx_pos] = f"B{len(arrays)-1}"
        last_tensor = Tensor(arrays[-1], last_indices, [f"MPS_T{len(arrays)}"])
        tensors.append(last_tensor)

        mps = cls(tensors, shape)
        mps.reshape()
        return mps

    @classmethod
    def from_bitstring(cls, bitstring: str) -> "MatrixProductState":
        """
        Create an MPS for the given bitstring |b>

        Args:
            bitstring: The computational basis state to be prepared.

        Returns:
            An MPS.
        """
        zero = np.array([1, 0], dtype=complex)
        one = np.array([0, 1], dtype=complex)
        arrays = []
        if bitstring[0] == "0":
            arrays.append(zero.reshape((1, 2)))
        else:
            arrays.append(one.reshape((1, 2)))
        for bit in bitstring[1:-1]:
            if bit == "0":
                arrays.append(zero.reshape((1, 1, 2)))
            else:
                arrays.append(one.reshape((1, 1, 2)))
        if bitstring[-1] == "0":
            arrays.append(zero.reshape((1, 2)))
        else:
            arrays.append(one.reshape((1, 2)))

        return cls.from_arrays(arrays)

    @classmethod
    def all_zero_mps(cls, num_sites: int) -> "MatrixProductState":
        """
        Create an MPS for the all zero state |000...0>

        Args:
            num_sites: The number of sites for the MPS

        Returns:
            An MPS.
        """

        return cls.from_bitstring("0" * num_sites)

    @classmethod
    def from_hf_state(cls, num_spin_orbs: int, num_electrons: int):
        """
        Create an MPS for the HF state. Currently only valid for fermionic systems and JW encoded qubit systems.
        This is because the HF state is assumed to be |111000...0>.

        Args:
            num_spin_orbs: The number of spin orbitals in the system.
            num_electrons: The number of electrons in the system.

        Returns:
            A MPS.
        """
        bitstring = "1" * num_electrons + "0" * (num_spin_orbs - num_electrons)

        return cls.from_bitstring(bitstring)

    @classmethod
    def from_symmer_quantumstate(cls, quantum_state: "QuantumState"):  # type: ignore # noqa: F821
        """
        Create an MPS from a Symmer QuantumState object.

        Args:
            quantum_state: The quantum state.

        Returns:
            An MPS.
        """
        state_dict = quantum_state.to_dictionary
        bitstrings = list(state_dict.keys())
        weights = list(state_dict.values())
        mps = MatrixProductState.from_bitstring(bitstrings[0])
        mps.multiply_by_constant(weights[0])
        for idx in range(1, len(bitstrings)):
            temp_mps = MatrixProductState.from_bitstring(bitstrings[idx])
            temp_mps.multiply_by_constant(weights[idx])
            mps = mps + temp_mps

        return mps

    @classmethod
    def random_mps(
        cls, num_sites: int, bond_dim: int, physical_dim: int
    ) -> "MatrixProductState":
        """
        Create a random MPS.

        Args:
            num_sites: The number of sites for the MPS.
            bond_dim: The internal bond dimension to use.
            physical_dim: The physical dimension to use.

        Returns:
            An MPS.
        """
        arrays = []
        first_array = np.random.rand(bond_dim, physical_dim)
        arrays.append(first_array)

        for _ in range(1, num_sites - 1):
            array = np.random.rand(bond_dim, bond_dim, physical_dim)
            arrays.append(array)

        last_array = np.random.rand(bond_dim, physical_dim)
        arrays.append(last_array)

        return cls.from_arrays(arrays, shape="udp")

    @classmethod
    def random_quantum_state_mps(
        cls, num_sites: int, bond_dim: int, physical_dim: int = 2
    ) -> "MatrixProductState":
        """
        Create a random MPS corresponding to a valid quantum state.

        Args:
            num_sites: The number of sites for the MPS.
            bond_dim: The internal bond dimension to use.
            physical_dim (optional): The physical dimension to use. Default is 2 (for qubits).

        Returns:
            An MPS.
        """
        mps = cls.random_mps(num_sites, bond_dim, physical_dim)
        mps.normalise()
        return mps

    @classmethod
    def equal_superposition_mps(cls, num_sites: int) -> "MatrixProductState":
        """
        Create an MPS for the equal superposition state |+++...+>

        Args:
            num_sites: The number of sites for the MPS.

        Returns:
            An MPS.
        """
        h_end = np.array([np.sqrt(1 / 2), np.sqrt(1 / 2)], dtype=complex).reshape(1, 2)
        h_middle = np.array([np.sqrt(1 / 2), np.sqrt(1 / 2)], dtype=complex).reshape(
            1, 1, 2
        )
        arrays = [h_end] + [h_middle] * (num_sites - 2) + [h_end]
        return cls.from_arrays(arrays, shape="udp")

    @classmethod
    def from_qiskit_circuit(
        cls, qc: QuantumCircuit, max_bond: int, input_mps: "MatrixProductState" = None
    ) -> "MatrixProductState":
        """
        Create an MPS for the output of a Qiskit QuantumCircuit.

        Args:
            qc: The QuantumCircuit object.
            max_bond: The maximum bond dimension to allow.
            input (optional): The input MPS. Default is the all zero MPS.

        Returns:
            An MPS.
        """
        qc_mpo = MatrixProductOperator.from_qiskit_circuit(qc, max_bond)
        if not input_mps:
            mps = cls.all_zero_mps(qc.num_qubits)
        else:
            mps = input_mps
        mps = mps.apply_mpo(qc_mpo)
        return mps

    def __add__(self, other: "MatrixProductState") -> "MatrixProductState":
        """
        Defines MPS addition.
        """
        self.reshape()
        other.reshape()
        arrays = []

        t1 = self.tensors[0]
        t2 = other.tensors[0]

        t1_data = t1.data
        t2_data = t2.data
        t1_data = sparse.reshape(t1_data, (1, t1.dimensions[0], t1.dimensions[1]))
        t2_data = sparse.reshape(t2_data, (1, t2.dimensions[0], t2.dimensions[1]))
        t1_dimensions = (1, t1.dimensions[0], t1.dimensions[1])
        t2_dimensions = (1, t2.dimensions[0], t2.dimensions[1])

        data1 = sparse.reshape(
            t1_data, (t1_dimensions[0] * t1_dimensions[2], t1_dimensions[1])
        )
        data2 = sparse.reshape(
            t2_data, (t2_dimensions[0] * t2_dimensions[2], t2_dimensions[1])
        )

        new_data = sparse.concatenate([data1, data2], axis=1)
        new_data = sparse.moveaxis(new_data, [0, 1], [1, 0])
        arrays.append(new_data)

        for t_idx in range(1, self.num_sites - 1):
            t1 = self.tensors[t_idx]
            t2 = other.tensors[t_idx]

            t1_data = t1.data
            t2_data = t2.data
            t1_dimensions = t1.dimensions
            t2_dimensions = t2.dimensions

            data1 = sparse.moveaxis(t1_data, [0, 1, 2], [0, 2, 1])
            data2 = sparse.moveaxis(t2_data, [0, 1, 2], [0, 2, 1])

            data1 = sparse.reshape(
                data1, (t1_dimensions[0] * t1_dimensions[2], t1_dimensions[1])
            )
            data2 = sparse.reshape(
                data2, (t2_dimensions[0] * t2_dimensions[2], t2_dimensions[1])
            )

            zeros_top_right = sparse.COO.from_numpy(
                np.zeros((data1.shape[0], data2.shape[1]))
            )
            zeros_bottom_left = sparse.COO.from_numpy(
                np.zeros((data2.shape[0], data1.shape[1]))
            )

            new_data = sparse.concatenate(
                [
                    sparse.concatenate([data1, zeros_top_right], axis=1),
                    sparse.concatenate([zeros_bottom_left, data2], axis=1),
                ]
            )
            new_data = sparse.moveaxis(new_data, [0, 1], [1, 0])
            new_data = sparse.reshape(
                new_data,
                (
                    t1_dimensions[0] + t2_dimensions[0],
                    t1_dimensions[1] + t2_dimensions[1],
                    t1_dimensions[2],
                ),
            )

            arrays.append(new_data)

        t1 = self.tensors[-1]
        t2 = other.tensors[-1]

        t1_data = t1.data
        t2_data = t2.data
        t1_data = sparse.reshape(t1_data, (t1.dimensions[0], 1, t1.dimensions[1]))
        t2_data = sparse.reshape(t2_data, (t2.dimensions[0], 1, t2.dimensions[1]))
        t1_dimensions = (t1.dimensions[0], 1, t1.dimensions[1])
        t2_dimensions = (t2.dimensions[0], 1, t2.dimensions[1])

        data1 = sparse.reshape(
            t1_data, (t1_dimensions[0] * t1_dimensions[2], t1_dimensions[1])
        )
        data2 = sparse.reshape(
            t2_data, (t2_dimensions[0] * t2_dimensions[2], t2_dimensions[1])
        )

        new_data = sparse.concatenate([data1, data2], axis=1)
        new_data = sparse.moveaxis(new_data, [0, 1], [1, 0])
        arrays.append(new_data)

        output = MatrixProductState.from_arrays(arrays)
        return output

    def __sub__(self, other: "MatrixProductState") -> "MatrixProductState":
        """
        Defines MPS subtraction.
        """
        other.multiply_by_constant(-1.0)
        output = self + other
        return output

    def to_sparse_array(self) -> SparseArray:
        """
        Convert the MPS to a sparse array.
        """
        mps = copy.deepcopy(self)
        output = mps.contract_entire_network()
        output.combine_indices(output.indices, output.indices[0])
        return output.data

    def to_dense_array(self) -> ndarray:
        """
        Convert the MPS to a dense array.
        """
        mps = copy.deepcopy(self)
        sparse_array = mps.to_sparse_array()
        dense_array = sparse_array.todense()
        return dense_array

    def reshape(self, shape: str = "udp") -> None:
        """
        Reshape the tensors in the MPS.

        Args:
            shape (optional): Default is 'udp' (up, down, physical) but any order is allowed.
        """
        first_tensor = self.tensors[0]
        first_current_shape = self.shape.replace("u", "")
        first_new_shape = shape.replace("u", "")
        current_indices = first_tensor.indices
        new_indices = [
            current_indices[first_current_shape.index(n)] for n in first_new_shape
        ]
        first_tensor.reorder_indices(new_indices)

        for t_idx in range(1, self.num_sites - 1):
            t = self.tensors[t_idx]
            current_indices = t.indices
            new_indices = [current_indices[self.shape.index(n)] for n in shape]
            t.reorder_indices(new_indices)

        last_tensor = self.tensors[-1]
        last_current_shape = self.shape.replace("d", "")
        last_new_shape = shape.replace("d", "")
        current_indices = last_tensor.indices
        new_indices = [
            current_indices[last_current_shape.index(n)] for n in last_new_shape
        ]
        last_tensor.reorder_indices(new_indices)

        self.shape = shape
        return

    def multiply_by_constant(self, const: complex) -> None:
        """
        Scale the MPS by a constant.

        Args:
            const: The constant to multiply by.
        """
        first_tensor = self.tensors[0]
        first_tensor.multiply_by_constant(const)
        return

    def dagger(self) -> None:
        """
        Take the conjugate transpose of the MPS. Leaves indices unchanged.
        """
        for t in self.tensors:
            t.data = sparse.COO.conj(t.data)
        return

    def move_orthogonality_centre(self, where: int = None, current: int = None) -> None:
        """
        Move the orthogonality centre of the MPS.

        Args:
            where (optional): Defaults to the last tensor.
            current (optional): Where the orthogonality centre is currently (if known)
        """
        if not where:
            where = self.num_sites

        internal_indices = self.get_internal_indices()

        if current == where:
            return

        if not current:
            push_down = list(range(1, where))
            push_up = list(range(where, self.num_sites))[::-1]
        elif current < where:
            push_down = list(range(current, where))
            push_up = []
        else:
            push_down = []
            push_up = list(range(where, current))[::-1]

        max_bond = self.bond_dimension

        for idx in push_down:
            index = internal_indices[idx - 1]
            self.compress_index(index, max_bond)

        for idx in push_up:
            index = internal_indices[idx - 1]
            self.compress_index(index, max_bond, reverse_direction=True)

        return

    def apply_mpo(self, mpo: MatrixProductOperator) -> "MatrixProductState":
        """
        Apply a MPO to the MPS.

        Args:
            mpo: The MPO to apply.

        Returns:
            The new MPS.
        """
        self.reshape()
        mpo.reshape()
        arrays = []

        t1 = self.tensors[0]
        t2 = mpo.tensors[0]

        t1.indices = ["T1_DOWN", "TO_CONTRACT"]
        t2.indices = ["T2_DOWN", "T2_RIGHT", "TO_CONTRACT"]

        tn = TensorNetwork([t1, t2])
        tn.contract_index("TO_CONTRACT")

        tensor = Tensor(tn.tensors[0].data, tn.get_all_indices(), tn.get_all_labels())
        tensor.combine_indices(["T1_DOWN", "T2_DOWN"], new_index_name="DOWN")
        tensor.reorder_indices(["DOWN", "T2_RIGHT"])
        arrays.append(tensor.data)

        for t_idx in range(1, self.num_sites - 1):
            t1 = self.tensors[t_idx]
            t2 = mpo.tensors[t_idx]

            t1.indices = ["T1_UP", "T1_DOWN", "TO_CONTRACT"]
            t2.indices = ["T2_UP", "T2_DOWN", "T2_RIGHT", "TO_CONTRACT"]

            tn = TensorNetwork([t1, t2])
            tn.contract_index("TO_CONTRACT")

            tensor = Tensor(
                tn.tensors[0].data, tn.get_all_indices(), tn.get_all_labels()
            )
            tensor.combine_indices(["T1_UP", "T2_UP"], new_index_name="UP")
            tensor.combine_indices(["T1_DOWN", "T2_DOWN"], new_index_name="DOWN")
            tensor.reorder_indices(["UP", "DOWN", "T2_RIGHT"])
            arrays.append(tensor.data)

        t1 = self.tensors[-1]
        t2 = mpo.tensors[-1]

        t1.indices = ["T1_UP", "TO_CONTRACT"]
        t2.indices = ["T2_UP", "T2_RIGHT", "TO_CONTRACT"]

        tn = TensorNetwork([t1, t2])
        tn.contract_index("TO_CONTRACT")

        tensor = Tensor(tn.tensors[0].data, tn.get_all_indices(), tn.get_all_labels())
        tensor.combine_indices(["T1_UP", "T2_UP"], new_index_name="UP")
        tensor.reorder_indices(["UP", "T2_RIGHT"])
        arrays.append(tensor.data)
        mps = MatrixProductState.from_arrays(arrays)
        return mps

    def set_default_indices(
        self, internal_prefix: str | None = None, external_prefix: str | None = None
    ) -> None:
        """
        Rename all indices to a standard form.

        Args:
            internal_prefix: If provided the internal bonds will have the form internal_prefix + index
            external_prefix: If provided the external bonds will have the form external_prefix + index
        """
        if not internal_prefix:
            internal_prefix = "B"
        if not external_prefix:
            external_prefix = "P"
        self.reshape("udp")
        new_indices_first = [internal_prefix + "1", external_prefix + "1"]
        self.tensors[0].indices = new_indices_first
        for tidx in range(1, self.num_sites - 1):
            t = self.tensors[tidx]
            new_indices_t = [
                internal_prefix + str(tidx),
                internal_prefix + str(tidx + 1),
                external_prefix + str(tidx + 1),
            ]
            t.indices = new_indices_t
        new_indices_last = [
            internal_prefix + str(self.num_sites - 1),
            external_prefix + str(self.num_sites),
        ]
        self.tensors[-1].indices = new_indices_last
        return

    def compute_inner_product(self, other: "MatrixProductState") -> complex:
        """
        Calculate the inner product with another MPS.

        Args:
            other: The other MPS.

        Returns
            The inner product <self | other>.
        """
        mps1 = copy.deepcopy(self)
        mps2 = copy.deepcopy(other)
        mps1.reshape("udp")
        mps2.reshape("udp")
        mps2.dagger()
        for t in mps2.tensors:
            current_indices = t.indices
            new_indices = [x if x[0] == "P" else x + "_" for x in current_indices]
            t.indices = new_indices
        all_tensors = mps1.tensors + mps2.tensors

        tn = TensorNetwork(all_tensors, "TotalTN")
        for n in range(self.num_sites - 1):
            tn.contract_index(f"P{n+1}")
            tn.contract_index(f"B{n+1}")
            tn.combine_indices([f"P{n+2}", f"B{n+1}_"], new_index_name=f"P{n+2}")

        tn.contract_index(f"P{self.num_sites}")
        val = complex(tn.tensors[0].data.flatten()[0])

        return val

    def compute_expectation_value(self, mpo: MatrixProductOperator) -> float:
        """
        Calculate an expectation value of the form <MPS | MPO | MPS>.

        Args:
            mpo: The MPO whose expectation value will be calculated.

        Returns:
            The expectation value.
        """
        mps1 = copy.deepcopy(self)
        mps2 = copy.deepcopy(self)

        mpo.reshape("udrl")
        mps1.reshape("udp")
        mps2.reshape("udp")

        mps1 = mps1.apply_mpo(mpo)

        exp_val = mps1.compute_inner_product(mps2)
        return exp_val

    def partial_trace(self, sites: list[int], matrix: bool = False) -> ndarray | Tensor:
        """
        Compute the partial trace.

        Args:
            sites: The list of sites to trace over.
            matrix: If True returns the reduced density matrix, otherwise returns a smaller MPS.

        Returns:
            The reduced state.
        """
        mps1 = copy.deepcopy(self)
        mps2 = copy.deepcopy(self)

        mps1.set_default_indices()
        mps2.set_default_indices(internal_prefix="C")

        all_inds = list(range(1, self.num_sites + 1))
        for site in sites:
            all_inds.remove(site)

        for site in all_inds:
            current_indices = mps2.tensors[site - 1].indices
            mps2.tensors[site - 1].indices = [
                x if x[0] == "C" else "_" + x for x in current_indices
            ]

        mps2.dagger()

        all_tensors = mps1.tensors + mps2.tensors
        tn = TensorNetwork(all_tensors, "TotalTN")
        result = tn.contract_entire_network()
        if matrix:
            output_inds = [f"P{x}" for x in all_inds]
            input_inds = [f"_P{x}" for x in all_inds]
            result.tensor_to_matrix(input_idxs=input_inds, output_idxs=output_inds)
        return result

    def normalise(self) -> None:
        """
        Normalise the MPS.
        """
        norm = self.compute_inner_product(self).real
        self.multiply_by_constant(np.sqrt(1 / norm))
        return

    def expand_bond_dimension(self, diff: int, bond_idx: int) -> "MatrixProductState":
        """
        Expand the internal bond dimension by padding with 0s.

        Args:
            diff: The amount to pad the bond dimension by
            bond_idx: The bond to expand
        """
        arrays = [t.data for t in self.tensors]
        self.reshape("udp")
        if bond_idx - 1 == 0:
            arrays[bond_idx - 1] = sparse.pad(arrays[bond_idx - 1], ((0, diff), (0, 0)))
        else:
            arrays[bond_idx - 1] = sparse.pad(
                arrays[bond_idx - 1], ((0, 0), (0, diff), (0, 0))
            )
        if bond_idx == self.num_sites - 1:
            arrays[bond_idx] = sparse.pad(arrays[bond_idx], ((0, diff), (0, 0)))
        else:
            arrays[bond_idx] = sparse.pad(arrays[bond_idx], ((0, diff), (0, 0), (0, 0)))
        mps = MatrixProductState.from_arrays(arrays)

        return mps

    def expand_bond_dimension_list(
        self, diff: int, bond_idxs: list[int]
    ) -> "MatrixProductState":
        """
        Expand multiple bonds.

        Args:
            diff: The amount to pad the bond dimension by
            bond_idxs: The bonds to expand
        """
        mps = self
        for idx in bond_idxs:
            mps = mps.expand_bond_dimension(diff, idx)
        return mps

    def draw(
        self,
        node_size: int | None = None,
        x_len: int | None = None,
        y_len: int | None = None,
    ):
        """
        Visualise MPS.

        Args:
            node_size: Size of nodes in figure (optional)
            x_len: Figure width (optional)
            y_len: Figure height (optional)

        Returns:
            Displays plot.
        """
        draw_mps(self.tensors, node_size, x_len, y_len)
