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
from typing import Any

from .abstract import EOAbstractFormatter


class ToImageSize(EOAbstractFormatter):
    """Silent Formatter used to read metadata files"""

    # docstr-coverage: inherited
    name = "to_imageSize"

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
            Returns the input
        """
        return input


class Text(EOAbstractFormatter):
    """Silent Formatter used to read metadata files"""

    # docstr-coverage: inherited
    name = "Text"

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
            Returns the input
        """
        return input
