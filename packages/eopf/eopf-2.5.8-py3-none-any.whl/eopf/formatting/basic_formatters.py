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
from ast import literal_eval
from typing import Any, Union

import numpy

from eopf.exceptions import FormattingError

from .abstract import EOAbstractFormatter


class ToStr(EOAbstractFormatter):
    """Formatter for string conversion"""

    # docstr-coverage: inherited
    name = "to_str"

    # docstr-coverage: inherited
    def _format(self, input: Any) -> str:
        """Convert input to string

        Parameters
        ----------
        input: Any

        Returns
        ----------
        str:
            String representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return str(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToLowerStr(EOAbstractFormatter):
    """Formatter for string conversion to lowercase"""

    # docstr-coverage: inherited
    name = "to_str_lower"

    # docstr-coverage: inherited
    def _format(self, input: Any) -> str:
        """Convert input to string

        Parameters
        ----------
        input: Any

        Returns
        ----------
        str:
            String representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            if isinstance(input, list) and len(input) == 1:
                return str(input[0]).lower()
            else:
                return str(input).lower()
        except Exception as e:
            raise FormattingError(f"{e}")


class ToFloat(EOAbstractFormatter):
    """Formatter for float conversion"""

    # docstr-coverage: inherited
    name = "to_float"

    def _format(self, input: Any) -> float:
        """Convert input to float

        Parameters
        ----------
        input: Any

        Returns
        ----------
        float:
            Float representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return float(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToInt(EOAbstractFormatter):
    """Formatter for int conversion"""

    # docstr-coverage: inherited
    name = "to_int"

    def _format(self, input: Any) -> Union[int, float]:
        """Convert input to int

        Parameters
        ----------
        input: Any

        Returns
        ----------
        int:
            Integer representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            if input == "N/A":
                return numpy.nan
            return int(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToBool(EOAbstractFormatter):
    """Formatter for bool conversion"""

    # docstr-coverage: inherited
    name = "to_bool"

    def _format(self, input: Any) -> bool:
        """Convert input to boolean

        Parameters
        ----------
        input: Any

        Returns
        ----------
        bool:
            Boolean representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return bool(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class IsOptional(EOAbstractFormatter):
    name = "is_optional"

    def _format(self, input: Any) -> Any:
        """Silent formatter, used only for parsing the path
        logic is present in stac_mapper method of XMLManifestAccessor

        Parameters
        ----------
        input: Any
            input

        Returns
        ----------
        Any:
            Returns "Not found"
        """
        if input is None:
            return "null"
        else:
            return input


class ToMicromFromNanom(EOAbstractFormatter):
    """Formatter converting nanometers to micrometers"""

    # docstr-coverage: inherited
    name = "to_microm_from_nanom"

    def _format(self, input: Any) -> float:
        """Convert nanometers to micrometers

        Parameters
        ----------
        input: Any

        Returns
        ----------
        float:
            Float representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return float(input) * float(0.001)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToNumber(EOAbstractFormatter):
    """Formatter for number representation"""

    # docstr-coverage: inherited
    name = "to_number"

    def _format(self, input: Any) -> Any:
        """Formatter converting a string which represents a number to a specific data type. eg: '12' int(12)

        Parameters
        ----------
        input: Any

        Returns
        ----------
        Any:
            int, float, numpy, complex .. whatever the number type might be

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            data = None
            num_types = [
                numpy.uint8,
                numpy.uint16,
                numpy.uint32,
                numpy.uint64,
                numpy.int8,
                numpy.int16,
                numpy.int32,
                numpy.int64,
                numpy.float16,
                numpy.float32,
                numpy.float64,
                numpy.longdouble,
                numpy.complex64,
                numpy.complex128,
            ]
            for num_type in num_types:
                try:
                    # check the current dtype that is floating or not
                    if numpy.issubdtype(num_type, numpy.floating):
                        type_info: Any = numpy.finfo(num_type)  # type: ignore
                        # get the maximum possible value of the number
                        potential_number = float(input)
                        # check in case we have overflow
                        if type_info.min <= potential_number <= type_info.max and input == str(num_type(input)):
                            data = num_type(input)
                        else:
                            continue
                    else:
                        type_info = numpy.iinfo(num_type)
                        # get the maximum possible value of the number
                        potential_number = float(input)
                        # check in case we have overflow
                        if type_info.min <= potential_number <= type_info.max and input == str(num_type(input)):
                            data = num_type(input)
                        else:
                            continue
                    data = num_type(input)
                    data + data, data - data, data * data, data**2, data / data  # type: ignore
                    break
                except Exception as _:  # nosec # noqa: F841
                    continue
            if data is None:
                data = literal_eval(input)
                data + data, data - data, data * data, data**2, data / data  # type: ignore
        except ZeroDivisionError:
            return data
        except Exception as e:
            raise FormattingError(f"{e}")
        else:
            return data


class ToAuto(EOAbstractFormatter):
    """Formatter for converting data to what it is supposed to be"""

    # docstr-coverage: inherited
    name = "auto"

    def _format(self, input: str) -> Any:
        """Convert input to whatever it should be

        Parameters
        ----------
        input: Any

        Returns
        ----------
        Any:
            Output with data type as what it supposed to be

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return literal_eval(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToCorrectedDateISO8601(EOAbstractFormatter):
    """Formatter to correct the date given as string"""

    name = "corrected_Date_ISO8601"

    def _format(self, input: str) -> Any:
        """This formatter should be used when the date has to be corrected.
        A real case would be for missing characters such as 'Z' which stands for UTC

        Parameters
        ----------
        input: string

        Returns
        ----------
        string

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            if input and input[-1] != "Z":
                return input + "Z"
            else:
                return input
        except Exception as e:
            raise FormattingError(f"{e}")
