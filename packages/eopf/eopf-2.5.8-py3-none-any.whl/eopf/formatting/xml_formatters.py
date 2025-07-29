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
import datetime
from re import search
from typing import Any, List

import lxml.etree
import numpy

from eopf.exceptions import FormattingError
from eopf.logging import EOLogging

from .abstract import EOAbstractXMLFormatter


class ToDatetimeS02(EOAbstractXMLFormatter):
    """Formatter for the datetime attribute compliant with the stac standard"""

    # docstr-coverage: inherited
    name = "to_datetime_s02"

    def _format(self, input: List[lxml.etree._Element]) -> Any:
        """
        The datetime retrived from the product from XML search, the datetime STAC attribute
        should contain the middle time between the start_datetime and the end_datetime
        """
        tag_start, tag_stop = "PRODUCT_START_TIME", "PRODUCT_STOP_TIME"
        children = {elt.tag: elt.text for elt in input[0].iterchildren([tag_start, tag_stop])}
        # will raise ValueError if str(None), of KeyError if not set
        d1 = datetime.datetime.fromisoformat(str(children[tag_start]))
        d2 = datetime.datetime.fromisoformat(str(children[tag_stop]))
        delta = d2 - d1
        middle = d1 + 0.5 * delta
        return datetime.datetime.isoformat(middle)


class ToBands(EOAbstractXMLFormatter):
    name = "to_bands"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> List[str]:
        bands_set = set()
        for element in xpath_input:
            band_id = str(element.attrib["bandId"])
            if len(band_id) == 1:
                bands_set.add(f"b0{band_id}")
            else:
                bands_set.add(f"b{band_id}")

        return sorted(bands_set)


class ToDetectors(EOAbstractXMLFormatter):
    name = "to_detectors"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> List[str]:
        detectors_set = set()
        for element in xpath_input:
            detector_id = str(element.attrib["detectorId"])
            if len(detector_id) == 1:
                detectors_set.add(f"d0{detector_id}")
            else:
                detectors_set.add(f"d{detector_id}")

        return sorted(detectors_set)


class ToMean(EOAbstractXMLFormatter):
    name = "to_mean"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return numpy.mean([float(str(element.text)) for element in xpath_input])


class ToList(EOAbstractXMLFormatter):
    name = "to_list"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [float(str(element.text)) for element in xpath_input]


class ToListStr(EOAbstractXMLFormatter):
    name = "to_list_str"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [element for element in xpath_input]


class ToListFloat(EOAbstractXMLFormatter):
    name = "to_list_float"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [float(str(element)) for element in xpath_input]


class ToListInt(EOAbstractXMLFormatter):
    name = "to_list_int"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [int(str(element)) for element in xpath_input]


class ToProcessingHistory(EOAbstractXMLFormatter):
    # docstr-coverage: inherited
    name = "to_processing_history"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def get_attr(self, node: Any, path: str) -> Any:
        try:
            childs = node.xpath(path, namespaces=self.namespaces)
        except lxml.etree.XPathEvalError:
            childs = []
            self._logger.warning("The product history is probaly missing namespaces.")
        if len(childs) > 0:
            return str(childs[0])
        else:
            return None

    def transform(self, output: Any, output_role: Any, node: Any, accu: Any) -> str:
        if node is not None:
            processor = self.get_attr(node, f"{self.safe_namespace}:facility/{self.safe_namespace}:software/@name")
            version = self.get_attr(node, f"{self.safe_namespace}:facility/{self.safe_namespace}:software/@version")
            facility_name = self.get_attr(node, f"{self.safe_namespace}:facility/@name")
            facility_organisation = self.get_attr(node, f"{self.safe_namespace}:facility/@organisation")
            processing_time = self.get_attr(node, "@stop")
            inputs: Any = dict()
            try:
                childs = node.xpath(f"{self.safe_namespace}:resource", namespaces=self.namespaces)
            except lxml.etree.XPathEvalError:
                childs = []
                self._logger.warning("The product history is probaly missing namespaces.")
            for child in childs:
                role = self.get_attr(child, "@role")
                input = self.transform(
                    self.get_attr(child, "@name"),
                    self.get_attr(child, "@role"),
                    (
                        child.xpath(f"{self.safe_namespace}:processing", namespaces=self.namespaces)[0]
                        if len(child.xpath(f"{self.safe_namespace}:processing", namespaces=self.namespaces)) > 0
                        else None
                    ),
                    accu,
                )
                if input == "":
                    continue
                if role in inputs:
                    inputs[role + "1"] = inputs.pop(role)
                    inputs[role + "2"] = input
                elif role + "1" in inputs:
                    for i in range(3, 999):
                        if not role + str(i) in inputs:
                            inputs[role + str(i)] = input
                            break
                        if i > 997:
                            raise FormattingError("too many inputs with identical role " + role + " for " + output)
                else:
                    inputs[role] = input
            record = dict()
            record["type"] = output_role
            record["processor"] = processor
            if version:
                record["version"] = version
            if facility_name and facility_organisation:
                record["processingCentre"] = facility_name + ", " + facility_organisation
            if processing_time:
                record["processingTime"] = processing_time
            if len(inputs) > 0:
                record["inputs"] = inputs
            record["output"] = output
            accu.append(record)
        else:
            pass
        return output

    def _format(self, packed_data) -> Any:  # type: ignore
        """

        Parameters
        ----------
        input: Any
            input

        Returns
        ----------
        Any:
            Returns the input
        """
        xml_node, self.namespaces, product_name, url = packed_data

        # S1 namespaces differs from S2 and S4
        s1_rex = r"S1[ABCD]_.{2}_.{4}_(\d).{3}_.*"
        if search(s1_rex, url):
            self.safe_namespace = "safe"
        else:
            self.safe_namespace = "sentinel-safe"

        accu: List[Any] = list()

        # determine the product level based on the url of the product
        level = ""
        if url is not None:
            # Sentinels 1, 2, 3 regexes to retrieve the level
            sentinels_rex = [
                r"S1[ABCD]_.{2}_.{4}_(\d).{3}_.*",
                r"S2[ABCD]_MSI(\w{3})_.*",
                r"S3[ABCD]_\w{2}_(.)_.*",
            ]
            i = 0
            while level == "" and i < len(sentinels_rex):
                match = search(sentinels_rex[i], url)
                if match and match[1]:
                    if match[1][0] != "L":
                        level = "L" + match[1]
                    else:
                        level = match[1]
                else:
                    # in case of no match proceed to the following regex
                    i += 1

        self.transform(
            product_name,
            level,
            xml_node,
            accu,
        )
        return accu


class ToBoolInt(EOAbstractXMLFormatter):
    """Formatter for converting a string to an integer representation of bool"""

    # docstr-coverage: inherited
    name = "to_bool_int"

    def _format(self, xpath_input: Any) -> int:
        low_input = xpath_input[0].lower()
        if low_input in ["true"]:
            return 1
        else:
            return 0


class ToProcessingSoftware(EOAbstractXMLFormatter):
    """Formatter for extracting processing software from xml"""

    # docstr-coverage: inherited
    name = "to_processing_software"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> dict[str, str]:
        # retrieve the name and version of the xml node xpath_input

        try:
            data = xpath_input.attrib
        except Exception as e:
            self._logger.warning(f"Can not retrieve processing:software : {e}")
            data = {"name": "", "version": ""}

        return data


class ToSciDOI(EOAbstractXMLFormatter):
    """Formatter for extracting product doi from xml"""

    # docstr-coverage: inherited
    name = "to_sci_doi"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        # retrieve the right part of the DOI url
        try:
            if xpath_input and len(xpath_input) == 0:
                data = xpath_input.replace("https://doi.org/", "")
            elif xpath_input and len(xpath_input) == 1:
                data = xpath_input[0].replace("https://doi.org/", "")
        except Exception as e:
            self._logger.warning(f"Can not retrieve sci:doi : {e}")
            data = ""
        return data


class ToProductTimeliness(EOAbstractXMLFormatter):
    """Formatter for getting the timeliness for specific timeliness"""

    # docstr-coverage: inherited
    name = "to_product_timeliness"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        timeliness_category = xpath_input
        to_timeliness_map = {
            "NR": "PT3H",
            "NRT": "PT3H",
            "NRT-3h": "PT3H",
            "ST": "PT36H",
            "24H": "PT24H",
            "STC": "PT36H",
            "Fast-24h": "PT24H",
            "AL": "Null",
            "NT": "P1M",
            "NTC": "P1M",
        }
        if timeliness_category in to_timeliness_map:
            return to_timeliness_map[timeliness_category]
        else:
            return "Null"


class ToSatOrbitState(EOAbstractXMLFormatter):
    """Formatter for getting the correct orbit state"""

    # docstr-coverage: inherited
    name = "to_sat_orbit_state"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        """There are cases when that xml data is with uppercase or
        it has several xml data attributes about ascending, descending, etc"""

        data = xpath_input

        # the data might come in uppercase | has usage for S1 products
        if data and len(data) == 1:
            return data[0].lower()
        return "No data about orbit state"


class ToProviders(EOAbstractXMLFormatter):
    """Formatter for respecting providers stac standard"""

    # docstr-coverage: inherited
    name = "to_providers"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        """The name and organization have to be mentioned as attributes even though there is no info"""
        return xpath_input if xpath_input else None


class ToPlatform(EOAbstractXMLFormatter):
    """Formatter for the platform attribute compliant with the stac standard"""

    # docstr-coverage: inherited
    name = "to_platform"

    def _format(self, xpath_input: list[lxml.etree._Element]) -> Any:
        """The platform's name retrived from the resulted list from XML search"""
        if isinstance(xpath_input, list) and xpath_input is not None:
            return str(xpath_input[0]).lower()
        elif isinstance(xpath_input, str) and xpath_input is not None:
            return str(xpath_input).lower()
        else:
            raise FormattingError("No data about stac_discovery/properties/platform")


class ToSarPolarizations(EOAbstractXMLFormatter):
    """Formatter for sar:polarizations attribute"""

    # docstr-coverage: inherited
    name = "to_sar_polarizations"

    def _format(self, xpath_input: list[lxml.etree._Element]) -> Any:
        """The input parameter from this function should be a list with all polarizations"""
        if isinstance(xpath_input, list):
            return xpath_input
        else:
            raise FormattingError("The xml path for sar:polarizations is wrong or it doesn't exist!")
