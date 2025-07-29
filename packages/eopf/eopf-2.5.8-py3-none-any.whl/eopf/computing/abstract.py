#
# Copyright (C) 2025 ESA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import inspect
import os.path
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, TypeAlias, Union

from xarray.core.datatree import DataTree

from eopf import EOContainer
from eopf.common import file_utils
from eopf.common.file_utils import AnyPath
from eopf.exceptions.errors import MissingArgumentError
from eopf.product import EOProduct
from eopf.product.eo_product_validation import AllowedValidationMode

DataType: TypeAlias = Union[EOProduct, EOContainer, DataTree]
MappingDataType: TypeAlias = Mapping[str, DataType | Iterable[DataType]]


@dataclass
class AuxiliaryDataFile:
    name: str
    path: AnyPath
    store_params: Optional[dict[str, Any]] = None
    # Data pointer to store opened data or whatever you wants
    data_ptr: Any = None

    def __repr__(self) -> str:
        return f"ADF {self.name} : {self.path} : {self.data_ptr}"


ADF: TypeAlias = AuxiliaryDataFile
MappingAuxiliary: TypeAlias = Mapping[str, AuxiliaryDataFile]


class EOProcessingBase(ABC):
    """
    Define base functionalities for all processing elements such as identifier and representation
    """

    @property
    def identifier(self) -> Any:
        """Identifier of the processing step"""
        return self._identifier

    def __init__(self, identifier: Any = ""):
        self._identifier = identifier or str(id(self))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self.identifier}>"

    def __repr__(self) -> str:
        return f"[{id(self)}]{str(self)}"


class EOProcessingStep(EOProcessingBase):
    """Converts one or several input arrays (of one or several variables)
    into one array (of one intermediate or output variable).

    These algorithms should be usable outside a Dask context to allow re-use in other
    software or integration of existing algorithms.


    Parameters
    ----------
    identifier: str, optional
        a string to identify this processing step (useful for logging)

    See Also
    --------
    dask.array.Array
    """

    def __init__(self, identifier: Any = ""):
        warnings.warn("Deprecated, we no longer enforce the use of ProcessingSteps", DeprecationWarning)
        super().__init__(identifier)

    @abstractmethod
    def apply(self, *inputs: Any, **kwargs: Any) -> Any:  # pragma: no cover
        """Abstract method that is applied for one block of the inputs.

        It creates a new array from arrays, can be any accepted type by map_block function from Dask.

        Parameters
        ----------
        *inputs: any
            input arrays (numpy, xarray) with same number of chunks each compatible with map_block functions
        **kwargs: any
            any needed kwargs

        Returns
        -------
        Any : same kind as the input type ( numpy array or xarray DataArray)
        """


class EOProcessingUnit(EOProcessingBase):
    """Abstract base class of processors i.e. processing units
    that provide valid EOProducts with coordinates etc.

    Parameters
    ----------
    identifier: str, optional
        a string to identify this processing unit (useful for logging and tracing)

    See Also
    --------
    eopf.product.EOProduct
    """

    @staticmethod
    def get_available_modes() -> List[str]:
        """
        Get the list of available mode for the processor

        Returns
        -------
        The list of processor's mode
        """
        return ["default"]

    @staticmethod
    def get_default_mode() -> str:
        """
        Get the default mode of the processor

        Returns
        -------
        The default processor mode
        """
        return "default"

    @classmethod
    def get_tasktable_description(cls, mode: str = "default", **kwargs: Any) -> Mapping[str, Any]:
        """
        Return the tasktable description for the Processing unit
        Parameters
        ----------
        mode : Optional str to specify the processing mode, if not provided default mode given
        kwargs : Any deciding parameter accepted by the processor get_tasktable_description ( see processor's doc)

        Returns
        -------
        Dictionary describing the tasktable
        """
        if mode not in cls.get_available_modes():
            modes_str = ", ".join(cls.get_available_modes())
            raise KeyError(f"Not accepted mode : {mode} , possibles:  {modes_str}")
        tasktable_file_path = AnyPath(os.path.join(Path(inspect.getfile(cls)).parent, "tasktables", mode + ".json"))
        if tasktable_file_path.exists():
            return file_utils.load_json_file(tasktable_file_path)
        else:
            raise KeyError(f"No tasktable file found for {mode} in {tasktable_file_path}")

    def __init__(self, identifier: Any = "") -> None:
        super().__init__(identifier)

    def get_mandatory_input_list(self, **kwargs: Any) -> list[str]:
        """
        Get the list of mandatory inputs names to be provided for the run method.
        In some cases, this list might depend on parameters and ADFs.
        If parameters are not provided, default behaviour is to provide the minimal list.
        Note: This method does not verify the content of the products, it only provides the list.

        Parameters
        ----------
        kwargs : same parameters as for the run method if available

        Returns
        -------
        the list of mandatory products to be provided
        """
        return []

    def get_mandatory_adf_list(self, **kwargs: Any) -> list[str]:
        """
        Get the list of mandatory ADF input names to be provided for the run method.
        In some cases, this list might depend on parameters.
        If parameters are not provided, default behaviour is to provide the minimal list.
        Note: This method does not verify the content of the ADF, it only provides the list.
        So no check on input ADF can be performed here.

        Parameters
        ----------
        kwargs : same parameters as for the run method if available

        Returns
        -------
        the list of mandatory ADFs to be provided
        """
        return []

    @abstractmethod
    def run(
        self,
        inputs: MappingDataType,
        adfs: Optional[MappingAuxiliary] = None,
        **kwargs: Any,
    ) -> MappingDataType:  # pragma: no cover
        """
        Abstract method to provide an interface for algorithm implementation

        Parameters
        ----------
        inputs: Mapping[str,DataType]
            all the products to process in this processing unit
        adfs: Optional[Mapping[str,AuxiliaryDataFile]]
            all the ADFs needed to process

        **kwargs: any
            any needed kwargs (e.g. parameters)

        Returns
        -------
        Mapping[str, DataType ]
        """

    def run_validating(
        self,
        inputs: MappingDataType,
        adfs: Optional[MappingAuxiliary] = None,
        validation_mode: AllowedValidationMode = "STRUCTURE",
        **kwargs: Any,
    ) -> MappingDataType:
        """Transforms input products into a new valid EOProduct/EOContainer/DataTree with new variables.

        Parameters
        ----------
        inputs: dict[str,DataType]
            all the products to process in this processing unit
        adfs: Optional[dict[str,AuxiliaryDataFile]]
            all the ADFs needed to process
        validation_mode: AllowedValidationMode
            Mode to validate see eo_product_validation

        **kwargs: any
            any needed kwargs

        Returns
        -------
        dict[str, DataType]
        """
        # verify that the input list is complete
        if not all(i in inputs.keys() for i in self.get_mandatory_input_list(**kwargs)):
            raise MissingArgumentError(
                f"Missing input, provided {inputs.keys()} while requested {self.get_mandatory_input_list(**kwargs)}",
            )
        # verify that the input list is complete
        if adfs is not None and not all(i in adfs.keys() for i in self.get_mandatory_adf_list(**kwargs)):
            raise MissingArgumentError(
                f"Missing input, provided {inputs.keys()} while requested {self.get_mandatory_input_list(**kwargs)}",
            )
        if adfs is not None:
            result_product = self.run(inputs, adfs, **kwargs)
        else:
            result_product = self.run(inputs, **kwargs)
        self.validate_output_products(result_product, validation_mode)
        return result_product

    def validate_output_products(self, products: MappingDataType, validation_mode: AllowedValidationMode) -> None:
        """Verify that the given product is valid.

        If the product is invalid, raise an exception.

        See Also
        --------
        eopf.product.EOProduct.validate
        """
        for p in products.items():
            # Can't validate a datatree
            if isinstance(p[1], (EOProduct, EOContainer)):
                p[1].validate(validation_mode)
