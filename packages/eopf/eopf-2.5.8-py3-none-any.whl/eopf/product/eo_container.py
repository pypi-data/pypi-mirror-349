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
import copy
import warnings
from pathlib import PurePosixPath
from typing import (
    TYPE_CHECKING,
    Any,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    MutableMapping,
    Optional,
    Self,
    Union,
    ValuesView,
)

import numpy as np
from deepdiff import DeepDiff

from eopf.common import date_utils
from eopf.common.constants import (
    DEEP_DIFF_IGNORE_TYPE_IN_GROUPS,
    EOCONTAINER_CATEGORY,
    EOPF_CATEGORY_ATTR,
    EOPF_CPM_PATH,
)
from eopf.common.file_utils import AnyPath
from eopf.common.functions_utils import is_last
from eopf.exceptions import EOContainerSetitemError, StoreMissingAttr
from eopf.product.conveniences import set_product_type
from eopf.product.eo_group import EOGroup
from eopf.product.eo_object import EOObject
from eopf.product.eo_product import EOProduct
from eopf.product.eo_variable import EOVariable
from eopf.product.rendering import renderer

if TYPE_CHECKING:  # pragma: no cover
    from eopf.product.eo_product_validation import AllowedValidationMode


class EOContainer(EOObject):
    """
    specialized dict to retain products and do additional things such as stac attributes etc

    """

    @staticmethod
    def create_from_products(
        name: str,
        products: Iterable["EOProduct" | Self],
        container_type: Optional[str] = None,
    ) -> "EOContainer":
        """
        Create EOContainer from iterable of EOContainers/EOProducts

        Parameters
        ----------
        name: str
            name of EOContainer
        products: Iterable["EOProduct" | Self]
            iterable of products
        container_type: Optional str
            container type

        Raises
        -------
        EOContainerSetitemError

        Returns
        -------
        EOContainer
        """
        for product in products:
            if len(product.name) == 0:
                raise EOContainerSetitemError("Product names must be defined properly")

        # create container
        container = EOContainer(name, type=container_type)
        container._declare_as_container()

        # iterate over products and add them to the container
        for product in products:
            container[product.name] = product

        return container

    def __init__(
        self,
        name: str,
        attrs: Optional[MutableMapping[str, Any]] = None,
        type: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, **kwargs)
        self._prod_dict: dict[str, EOProduct | EOContainer] = {}
        self._attrs: MutableMapping[str, Any] = dict(attrs) if attrs is not None else {}
        self._mission_specific: Optional[str] = None

        if type is None:
            if attrs is None:
                product_type = None
            else:
                try:
                    product_type = attrs["stac_discovery"]["properties"]["product:type"]
                except KeyError:
                    product_type = None
        else:
            product_type = type

        set_product_type(self, product_type)

        self._declare_as_container()

    @property
    def attrs(self) -> MutableMapping[str, Any]:
        for prod in self.values():
            self._add_product_to_links(prod)
        return self._attrs

    @attrs.setter
    def attrs(self, new_attrs: dict[str, Any]) -> None:
        self._attrs = new_attrs

    @property
    def mission_specific(self) -> Optional[str]:
        return self._mission_specific

    @mission_specific.setter
    def mission_specific(self, amission_specific: str) -> None:
        self._mission_specific = amission_specific

    @property
    def type(self) -> Optional[str]:
        """

        Returns
        -------

        """
        warnings.warn("Use container_type instead", DeprecationWarning)
        return self.container_type

    @property
    def container_type(self) -> Optional[str]:
        """
        Retrieve product_type, None if not set

        Returns
        -------
        from attribute ["stac_discovery"]["properties"]["product:type"]
        """
        try:
            return self.attrs["stac_discovery"]["properties"]["product:type"]
        except KeyError:
            return None

    @container_type.setter
    def container_type(self, intype: str) -> None:
        """
        Set product_type

        Parameters
        ----------
        inversion: str
        """
        self.attrs.setdefault("stac_discovery", {}).setdefault("properties", {})["product:type"] = intype

    @property
    def processing_version(self) -> Optional[str]:
        """
        Retrieve processing_version

        Returns
        -------
        from attribute ["stac_discovery"]["properties"]["processing:version"]
        """
        try:
            return self.attrs["stac_discovery"]["properties"]["processing:version"]
        except KeyError:
            return None

    @processing_version.setter
    def processing_version(self, inversion: str) -> None:
        """
        Set processing_version

        Parameters
        ----------
        inversion: str
        """
        self.attrs.setdefault("stac_discovery", {}).setdefault("properties", {})["processing:version"] = inversion

    def __setitem__(self, key: str, value: Union["EOProduct", "EOContainer", "EOGroup", "EOVariable"]) -> None:
        """
        Add "EOProduct", "EOContainer", "EOGroup", "EOVariable" to an EOContainer

        Parameters
        ----------
        key: str
            path of the value inside the container
        value: Union["EOProduct", "EOContainer", "EOGroup", "EOVariable"]
            object to be added

        Raises
        -------
        EOContainerSetitemError
        """

        if len(key) == 0:
            raise KeyError("Empty key is not accepted in eocontainer")

        if key == "/":
            raise KeyError("Key can not be root")

        if key.startswith("/"):
            key = key[1:]

        eopath = PurePosixPath(key)

        try:
            if eopath.is_absolute():
                # do not consider root "/" as a part
                # as it refers to self/current container
                eopath_parts = eopath.parts[1:]
            else:
                eopath_parts = eopath.parts

            if isinstance(value, (EOContainer, EOProduct)):
                if len(eopath_parts) > 1:
                    # recursively add the EOProduct/EOContainer
                    sub_key = "/".join(eopath_parts[1:])
                    sub_obj = self[eopath_parts[0]]
                    sub_obj[sub_key] = value
                    value.parent = self
                else:
                    # add product/container to current object
                    self._prod_dict[key] = value
                    value.parent = self
                    self._add_product_to_links(value)

            else:
                # isinstance(value, (EOVariable, EOGroup)):
                # EOVariables can not be attached to EOContainers
                # hence, we need to discover a descendant EOProduct and attach the EOV to it
                i = 0
                sub_obj = self
                while not isinstance(sub_obj, EOProduct) and i < len(eopath_parts):
                    # recursively search for an EOProduct
                    sub_obj = sub_obj[eopath_parts[i]]
                    i += 1

                if i == len(eopath_parts):
                    # when there is no EOProduct we can not attach the EOV
                    raise EOContainerSetitemError(
                        "EOVariables and EOGroups can only be added to an EOProduct,"
                        "which does not exist in the given path hierarchy {key}",
                    )

                # attach the EOV to the EOP
                eoproduct_path = "/".join(eopath_parts[i:])
                sub_obj[eoproduct_path] = value

        except Exception as err:
            raise EOContainerSetitemError(f"EOContainer setitem error: {err}")

    def __getitem__(self, item: str) -> Union["EOProduct", "EOContainer"]:
        return self._prod_dict[item]

    def __delitem__(self, key: str) -> None:
        self._remove_product_to_links(self._prod_dict[key])
        del self._prod_dict[key]

    def __iter__(self) -> Iterator["str"]:
        yield from iter(self._prod_dict)

    def __len__(self) -> int:
        return len(self._prod_dict)

    def __eq__(self, other: Any) -> bool:
        # Check if the other object is an instance of EOContainer
        if not isinstance(other, EOContainer):
            return False

        # Check if the two EOContainer have the same structure
        if set([key for key in self.keys()]) != set([key for key in other.keys()]):
            return False

        # Compare the two EOContainer attributes
        if DeepDiff(
            self.attrs,
            other.attrs,
            ignore_order=True,
            ignore_type_in_groups=DEEP_DIFF_IGNORE_TYPE_IN_GROUPS,
        ):  # True when DeepDiff returns not empty dict
            return False

        # Compare each contained EOContainer or EOProduct
        for item_key in self:
            if self[item_key] != other[item_key]:  # compare sub-containers or eoproducts
                return False

        return True

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __deepcopy__(self, memo: dict[int, Any]) -> "EOContainer":
        new_instance: EOContainer = EOContainer(
            self.name,
            copy.deepcopy(self.attrs),
            self.type if self.type is not None else "",
        )
        for k, v in self._prod_dict.items():
            new_instance[k] = copy.deepcopy(v)
        new_instance._mission_specific = copy.deepcopy(self._mission_specific)
        memo[id(self)] = new_instance
        return new_instance

    def _repr_html_(self, prettier: bool = True) -> str:
        """Returns the html representation of the current container displaying the tree.

        Parameters
        ----------
        prettier: str
            Flag for using SVG as label for each Product, Group, Variable, Attribute.
        """

        css_file = EOPF_CPM_PATH / "product/templates/static/css/style.css"

        with css_file.open(mode="r") as css:
            css_content = css.read()

        css_str = f"<style>{css_content}</style>\n"
        rendered_template = renderer("container.html", container=self, prettier=prettier)
        final_str = css_str + rendered_template

        return final_str

    def _print_tree_structure(
        self,
        buffer: List[str],
        obj: Union["EOObject", tuple[str, "EOObject"]],
        continues: tuple[bool, ...],
        level: int,
        detailed: bool,
    ) -> None:
        if isinstance(obj, tuple):
            cont = obj[1]
        else:
            cont = obj
        if not isinstance(cont, EOContainer):
            return

        fill, pre = EOObject._compute_tree_indents(continues)
        buffer.append(f"{pre}Container({cont.name})")
        level += 1
        for var, last in is_last(cont.values()):
            var._print_tree_structure(buffer, var, continues + (not last,), level, detailed)

    def items(self) -> ItemsView[str, "EOProduct" | Self]:
        yield from self._prod_dict.items()

    def keys(self) -> KeysView[str]:
        yield from self._prod_dict.keys()

    def values(self) -> ValuesView["EOProduct" | Self]:
        yield from self._prod_dict.values()

    def validate(self, validation_mode: "AllowedValidationMode" = "STRUCTURE") -> None:
        for pro in self._prod_dict.items():
            pro[1].validate(validation_mode=validation_mode)

    def get_default_file_name_no_extension(self, mission_specific: Optional[str] = None) -> str:
        """
        get the default filename using the convention :
        - Take product:type or internal product_type (8 characters, see #97)
        - Add "_"
        - Take start_datetime as YYYYMMDDTHHMMSS
        - Add "_"
        - Take end_datetime and start_datetime and calculate the difference in seconds (between 0000 to 9999)
        - Add "_"
        - Take the last character of "platform"  (A or B)
        - Take sat:relative_orbit (between 000 and 999)
        - Add "_"
        - Take product:timeliness_category: if it is NRT or 24H or STC, add "T";  if it is NTC, add "S"
        - Generate CRC on 3 characters
        If mission specific provided :
        - Add "_"
        - Add <mission_specific>
        """
        _req_attr_in_properties = [
            "start_datetime",
            "end_datetime",
            "platform",
            "sat:relative_orbit",
            "product:timeliness_category",
            "product:timeliness",
        ]
        filename = ""
        # get the properties attribute dict
        attributes_dict: MutableMapping[str, Any] = self.attrs
        if "stac_discovery" not in attributes_dict:
            raise StoreMissingAttr("Missing [stac_discovery] in attributes")
        if "properties" not in attributes_dict["stac_discovery"]:
            raise StoreMissingAttr("Missing [properties] in attributes[stac_discovery]")
        attributes_dict_properties = attributes_dict["stac_discovery"]["properties"]
        for attrib in _req_attr_in_properties:
            if attrib not in attributes_dict_properties:
                raise StoreMissingAttr(
                    f"Missing one required property in product to generate default filename : {attrib}",
                )
        # get the product type
        type = attributes_dict["stac_discovery"]["properties"]["product:type"]
        if type is None:
            raise StoreMissingAttr("Missing product type and product:type attributes")
        else:
            product_type: str = type
        start_datetime = attributes_dict_properties["start_datetime"]
        start_datetime_str = date_utils.get_date_yyyymmddthhmmss_from_tm(
            date_utils.get_datetime_from_utc(start_datetime),
        )
        end_datetime = attributes_dict_properties["end_datetime"]
        duration_in_second = int(
            (
                date_utils.get_datetime_from_utc(end_datetime) - date_utils.get_datetime_from_utc(start_datetime)
            ).total_seconds(),
        )
        platform_unit = attributes_dict_properties["platform"][-1]
        relative_orbit = attributes_dict_properties["sat:relative_orbit"]
        timeline_tag = "X"
        if attributes_dict_properties["product:timeliness_category"] in ["NR", "NRT", "NRT-3h"]:
            timeline_tag = "T"
        elif attributes_dict_properties["product:timeliness_category"] in ["ST", "24H", "STC", "Fast-24h", "AL"]:
            timeline_tag = "_"
        elif attributes_dict_properties["product:timeliness_category"] in ["NTC", "NT"]:
            timeline_tag = "S"
        else:
            raise StoreMissingAttr("Unrecognized product:timeliness_category attribute, should be NRT/24H/STC/NTC")
        crc = np.random.randint(100, 999, 1)[0]
        if mission_specific is not None:
            mission_specific = f"_{mission_specific}"
        elif self.mission_specific is not None:
            mission_specific = f"_{self.mission_specific}"
        else:
            mission_specific = ""
        filename = (
            f"{product_type}_{start_datetime_str}_{duration_in_second:04d}_{platform_unit}{relative_orbit:03d}_"
            f"{timeline_tag}{crc}{mission_specific}"
        )
        return filename

    def export_dask_graph(self, folder: AnyPath) -> None:
        for v in self:
            self[v].export_dask_graph(folder)

    @property
    def is_root(self) -> "bool":
        """
        Container are considered root
        Returns
        -------

        """
        return self.parent is None

    def _declare_as_container(self) -> None:
        self._attrs.setdefault("stac_discovery", dict()).setdefault("links", [])
        self._attrs.setdefault("other_metadata", dict()).setdefault(EOPF_CATEGORY_ATTR, EOCONTAINER_CATEGORY)

    def _add_product_to_links(self, prod: Union["EOProduct", "EOContainer"]) -> None:
        link_list = self._attrs.setdefault("stac_discovery", dict()).setdefault("links", [])
        if prod.name not in link_list:
            link_list.append(prod.name)

    def _remove_product_to_links(self, prod: Union["EOProduct", "EOContainer"]) -> None:
        self._attrs.setdefault("stac_discovery", dict()).setdefault("links", []).remove(prod.name)

    @staticmethod
    def is_container(objwithattr: Any) -> "bool":
        """
        Test is the object has the elements to be considered a container
        Mostly tests on the STAC attribute links and category in other:metadata

        Parameters
        ----------
        objwithattr: any EO object or other that has attrs access

        Returns
        -------

        """
        if isinstance(objwithattr, EOContainer):
            return True
        try:
            return (
                "links" in objwithattr.attrs["stac_discovery"]
                and isinstance(objwithattr.attrs["stac_discovery"]["links"], list)
                and objwithattr.attrs["other_metadata"][EOPF_CATEGORY_ATTR] == EOCONTAINER_CATEGORY
            )
        except KeyError:
            return False
