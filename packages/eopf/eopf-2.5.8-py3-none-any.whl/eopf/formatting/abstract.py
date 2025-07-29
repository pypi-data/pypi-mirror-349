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
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Self

import lxml.etree

from eopf.logging import EOLogging


class EOAbstractFormatter(ABC):
    """Abstract formatter representation"""

    def __init__(self, inner_formatter: Optional[Self] = None) -> None:
        self._inner_formatter = inner_formatter
        self._logger = EOLogging().get_logger("eopf.formatting")

    @property
    @abstractmethod
    def name(self) -> str:
        """Set the name of the formatter, for registering it"""
        raise NotImplementedError()

    def format(self, input: Any) -> Any:
        """Function that returns the formatted input"""
        if self._inner_formatter is not None:
            return self._format(self._inner_formatter.format(input))
        else:
            return self._format(input)

    @abstractmethod
    def _format(self, input: Any) -> Any:
        raise NotImplementedError

    def reverse_format(self, input: Any) -> Any:
        """Function that returns the reverse of the formatted input"""
        return input


class EOSingleValueFormatter(EOAbstractFormatter):
    """Abstract formatter representation for a single value"""

    @abstractmethod
    def _format(self, input: Any) -> Any:
        """Function that returns the formatted input"""
        raise NotImplementedError()

    def reverse_format(self, input: Any) -> Any:
        """Function that returns the reverse of the formatted input"""
        return input


class EOListValuesFormatter(EOAbstractFormatter):
    """Abstract formatter representation for a lists"""

    @abstractmethod
    def _format(self, input: List[Any]) -> Any:
        """Function that returns the formatted input"""
        raise NotImplementedError()

    def reverse_format(self, input: Any) -> Any:
        """Function that returns the reverse of the formatted input"""
        return input


class EOAbstractXMLFormatter(EOListValuesFormatter):
    """ "
    specialization for xml input formatter
    """

    @abstractmethod
    def _format(self, input: List[lxml.etree._Element]) -> Any:
        """Function that returns the formatted input"""
        raise NotImplementedError()
