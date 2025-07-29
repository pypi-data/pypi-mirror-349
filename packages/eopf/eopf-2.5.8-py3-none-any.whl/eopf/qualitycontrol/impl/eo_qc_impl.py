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
import importlib
from dataclasses import dataclass
from typing import Any

from eopf.common import date_utils
from eopf.common.file_utils import compute_json_size
from eopf.common.functions_utils import resolve_path_in_dict
from eopf.product import EOProduct
from eopf.product.eo_product_validation import is_valid_product
from eopf.qualitycontrol.eo_qc import EOQC, EOQCPartialCheckResult
from eopf.qualitycontrol.eo_qc_factory import EOQCFactory
from eopf.qualitycontrol.eo_qc_utils import EOQCFormulaEvaluator


@dataclass
@EOQCFactory.register_eoqc("formulas")
class EOQCFormula(EOQC):
    """Quality formula check class.

      eval of the formula given, parameters, variables and attributes are available under their alias
      eoproduct is also available as 'eoproduct'.

      .. code-block:: JSON

        {
            "id": "fake_inspection",
            "version": "0.0.1",
            "type": "formulas",
            "thematic": "GENERAL_QUALITY",
            "description": "validate that orbit number is between value",
            "precondition": {},
            "evaluator": {
                "parameters": [
                    {
                        "name": "v_min",
                        "value": 0
                    },
                    {
                        "name": "v_max",
                        "value": 9999999
                    }
                ],
                "variables": [
                    {
                        "name": "oa01",
                        "path": "measurements/radiance/oa01"
                    }
                ],
                "attributes": [
                    {
                        "name": "absolute_orbit",
                        "path": "stac_discovery/properties/sat:absolute_orbit"
                    }
                ],
                "formula": "v_min < absolute_orbit < v_max"
            }
        },

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in format XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator
    evaluator: EOQCFormulaEvaluator
        Expression evaluator
    """

    evaluator: EOQCFormulaEvaluator

    # docstr-coverage: inherited
    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:

        # Applying the formula
        result = bool(self.evaluator.evaluate(eoproduct))
        if result:
            message = f"PASSED: Formula {self.evaluator.formula} evaluate True on the product {eoproduct.name}"
        else:
            message = f"FAILED: Formula {self.evaluator.formula} evaluate False on the product {eoproduct.name}"
        return EOQCPartialCheckResult(status=result, message=message)


@dataclass
@EOQCFactory.register_eoqc("validate")
class EOQCValid(EOQC):
    """
    Validate a product

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in format XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator

    """

    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:
        result_valid, anomalies = is_valid_product(eoproduct, validation_mode="STAC")
        result_sensing_time = True
        message_sensing = "Sensing times are valid"
        start_datetime = "2022-08-31T02:17:58.477712Z"
        end_datetime = "2022-08-31T02:17:58.477712Z"
        try:
            start_datetime = resolve_path_in_dict(eoproduct.attrs, "stac_discovery/properties/start_datetime")
        except KeyError:
            result_sensing_time = False
            message_sensing = "Start_datetime is missing"
        try:
            end_datetime = resolve_path_in_dict(eoproduct.attrs, "stac_discovery/properties/end_datetime")
        except KeyError:
            result_sensing_time = False
            message_sensing = "End_datetime is missing"

        if result_sensing_time:
            result_sensing_time = date_utils.get_datetime_from_utc(start_datetime) < date_utils.get_datetime_from_utc(
                end_datetime,
            )
            if result_sensing_time:
                message_sensing = "STAC datetime are valid"
            else:
                message_sensing = "STAC datetime are not valid"
        if result_valid:
            if result_sensing_time:
                message = f"PASSED: The product {eoproduct.name} has valid structure;{message_sensing}"
            else:
                message = f"FAILED: The product {eoproduct.name} has valid structure;{message_sensing}"
        else:
            message_valid = ""
            for anom in anomalies:
                message_valid += f";category : {anom.category}, descr: {anom.description.splitlines()[0]}"
            message = f"FAILED: The product {eoproduct.name} has invalid structure : {message_valid};{message_sensing}"
        return EOQCPartialCheckResult(status=result_valid and result_sensing_time, message=message)


@dataclass
@EOQCFactory.register_eoqc("eoqc_runner")
class EOQCRunner(EOQC):
    """
    This EOQC allows to dynamically load an  EOQC and run it.

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in format XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator
    module: str
        Name to the module to import.
    eoqc_class: str
        eoqc class to be executed in the module.
    parameters: dict[str, Any]
        Parameters to instance the eoqc_class.


    """

    module: str
    eoqc_class: str
    parameters: dict[str, Any]

    # docstr-coverage: inherited
    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:
        module = importlib.import_module(self.module)
        eoqc_class = getattr(module, self.eoqc_class)

        if not issubclass(eoqc_class, EOQC):
            raise TypeError(f"{self.module}/{self.eoqc_class} is not a valid EOQC")
        params = {
            "id": self.id,
            "version": self.version,
            "thematic": self.thematic,
            "description": self.description,
            "precondition": self.precondition,
        }
        params.update(self.parameters)

        eoqc = eoqc_class(**params)

        return eoqc._check(eoproduct)


@dataclass
@EOQCFactory.register_eoqc("product_data_size")
class EOQCProductDataSize(EOQC):
    """
    This EOQC checks that the product data size is within range.

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in format XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator
    min: int
        Min of the range
    max: int
        Maximum of the range

    """

    min: int
    max: int

    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:
        datasize: int = eoproduct.datasize
        result = self.min < datasize < self.max
        if result:
            message = (
                f"PASSED: The product {eoproduct.name} datasize ({datasize}) "
                f"is within range [{self.min},{self.max}]"
            )
        else:
            message = (
                f"FAILED: The product {eoproduct.name} datasize ({datasize}) "
                f"is not within range [{self.min},{self.max}]"
            )
        return EOQCPartialCheckResult(status=result, message=message)


@dataclass
@EOQCFactory.register_eoqc("product_attr_size")
class EOQCProductAttrSize(EOQC):
    """
    This EOQC checks that the product attr file size in json is within range.

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in format XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator
    min: int
        Min of the range
    max: int
        Maximum of the range

    """

    min: int
    max: int

    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:
        datasize: int = compute_json_size(eoproduct.attrs)
        result = self.min < datasize < self.max
        if result:
            message = (
                f"PASSED: The product {eoproduct.name} attr size ({datasize}) "
                f"is within range [{self.min},{self.max}]"
            )
        else:
            message = (
                f"FAILED: The product {eoproduct.name} attr size ({datasize}) "
                f"is not within range [{self.min},{self.max}]"
            )
        return EOQCPartialCheckResult(status=result, message=message)
