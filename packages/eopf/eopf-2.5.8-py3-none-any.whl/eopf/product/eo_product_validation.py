import os
from dataclasses import dataclass
from logging import Logger
from typing import Any, Callable, Dict, List, Literal, Tuple
from urllib.parse import urlparse

import jsonschema
from jsonschema.exceptions import ValidationError

from eopf import EOLogging
from eopf.common import file_utils
from eopf.common.constants import EOPF_CPM_PATH
from eopf.common.file_utils import AnyPath
from eopf.product.eo_group import EOGroup
from eopf.product.eo_product import EOProduct
from eopf.product.eo_variable import EOVariable

MANDATORY_TOP_ATTR_CATEGORY = ("stac_discovery", "other_metadata")

# Definition of mandatory and optional elements
MANDATORY_GROUPS = ("measurements",)
OPTIONAL_GROUPS = ("quality", "conditions")

MANDATORY_VARIABLE_ATTRS = {"long_name": None, "short_name": None, "dtype": None}
OPTIONAL_VARIABLE_ATTRS = {
    "units": None,
    "standard_name": None,
    "flag_masks": None,
    "flag_values": None,
    "flag_meanings": None,
    "scale_factor": None,
    "add_offset": None,
    "valid_min": None,
    "valid_max": None,
    "fill_value": None,
    "coordinates": None,
    "dimensions": None,
}

# STAC CONSTANTS
STAC_ITEM_SCHEMA = "stac_item_schema_v1.1.0.json"
MANDATORY_STAC_EXTENSIONS = ["eopf-stac-extension"]
KEYWORD_TO_EXTENSION = {"eopf": "eopf-stac-extension"}


# ------------------------------------ EOPRODUCT validation rules ------------------------------------

# ---------- Summary of the workflow for product validation

#   * Whatever the input product, we apply the following:
#     - A "generic validation" which checks that all mandatory
#       elements are present + some basic rules
#     (e.g. a group cannot be empty,...)
#     - A metadata validation (to validate STAC metadata + other metadata)


# ---------- Validation rules for EOGroup:

#   - An EOGroup cannot be empty (must contain at least one sub group or variable)
#   - An EOGroup cannot contain other elements than EOGroups, EOVariables and attributes
#   (this rule is already verified through the setitem method of the EOProduct)
#   - Mandatory groups: measurements
#   - Possible groups: quality and conditions
#   - It is possible to have two groups
#   - Group attributes can be empty

# ---------- Validation rules for EOVariables:

#   - No scalar variables (= no scalar with empty dimensions + no scalar with dimensions “one”)
#   - Variable attributes cannot be empty (mandatory variables required)
#   - Mandatory variable attributes: long_name, short_name
#   - Possible variable attributes: units, standard_name, flag_masks, flag_values, flag_meanings, scale_factor,
#     add_offset, valid_min,
#     valid_max, fill_value, coordinates, dimensions

# ---------- Validation for top-level attributes in an EOPRoduct

# * STAC metadata:
#   - Generic validation:
# 	    . Mandatory STAC extensions in stac_extensions list: eopf, stac base 1.1.0
#       . Verify list of extensions : if one is missing or not used in the properties
#       . Validate against extensions schemas listed
#   - If the schema is available in the CPM install it will use it else it will download it

# * Other metadata:
# 	- Generic validation: No particular restrictions
#   - Template validation: other metadata should respect the template

ValidationAnomalyCategories = Literal["STRUCTURE", "STAC"]
AllowedValidationMode = Literal["STRUCTURE", "STAC"]


@dataclass
class AnomalyDescriptor:
    category: ValidationAnomalyCategories
    description: str


def is_valid_product(
    product: EOProduct,
    validation_mode: AllowedValidationMode = "STRUCTURE",
) -> tuple[bool, List[AnomalyDescriptor]]:
    """
    Returns a boolean indicating the validity of the product
    And the list of anomalies

    Parameters
    ----------
        product (EOProduct): input EOProduct
        validation_mode (str): selected validation mode: possible values:
            - STRUCTURE : only verify structure
            - STAC : STRUCTURE + STAC attr validation
    Returns
    -------
        Boolean indicating whether a product is valid
        List of anomalies, empty if none found
    """
    logger = EOLogging().get_logger("eopf.product.validation")
    anomalies: List[AnomalyDescriptor] = []
    checks_to_do: dict[AllowedValidationMode, List[Callable[[Any, List[AnomalyDescriptor], Logger], None]]] = {
        "STRUCTURE": [check_eoproduct_validity],
        "STAC": [check_eoproduct_validity, check_stac_validity],
    }

    # try:
    for check in checks_to_do[validation_mode]:
        check(product, anomalies, logger)
    return (len(anomalies) == 0, anomalies)
    # except Exception as e:
    #    return (False, anomalies)


def check_eoproduct_validity(product: EOProduct, out_anomalies: List[AnomalyDescriptor], logger: Logger) -> None:
    """
    Check if the input product has a valid format.
    A generic EOProduct validation is applied for all products.
    What's more, if the product type is defined, a product validation based on the templates data structure
    is also applied.

    Parameters
    ----------
        product (EOProduct): input EOProduct
        validation_mode (str): selected validation mode: possible values
    """
    # ----------------- Generic checks
    logger.debug("Launching generic product validation...")
    # Check the mandatory and possible top-level groups
    if any(key not in product for key in MANDATORY_GROUPS):
        out_anomalies.append(
            AnomalyDescriptor("STRUCTURE", f"Mandatory groups {MANDATORY_GROUPS} not present in the current product"),
        )
        logger.debug(f"Mandatory groups {MANDATORY_GROUPS} not present in the current product")
    if any(key not in OPTIONAL_GROUPS for key in [opt_key for opt_key in product if opt_key not in MANDATORY_GROUPS]):
        out_anomalies.append(AnomalyDescriptor("STRUCTURE", f"Optional groups must be in the list: {OPTIONAL_GROUPS}"))
    # Check mandatory attribute categories exist in the EOProduct
    if any(key not in product.attrs for key in MANDATORY_TOP_ATTR_CATEGORY):
        out_anomalies.append(
            AnomalyDescriptor(
                "STRUCTURE",
                f"Missing top-level attribute category from the mandatory list: {MANDATORY_TOP_ATTR_CATEGORY}",
            ),
        )
        logger.debug(f"Missing top-level attribute category from the mandatory list: {MANDATORY_TOP_ATTR_CATEGORY}")
    # Check that top-level groups are not empty
    for group_name, group in product.groups:
        if len(list(group)) == 0:
            out_anomalies.append(
                AnomalyDescriptor(
                    "STRUCTURE",
                    f"Group {group.path} cannot be empty",
                ),
            )
            logger.debug(f"Group {group.path} cannot be empty")

    # Generic check of the product struture
    for group in [group_data[1] for group_data in list(product.groups)]:
        check_group_validity(group, out_anomalies, logger)


def check_group_validity(group: EOGroup, out_anomalies: List[AnomalyDescriptor], logger: Logger) -> None:
    """
    Check if the input group has a valid format. Only a generic validation is done
    (the structure and the rules are verified).
    Parameters
    ----------
        group (EOGroup): input EOGroup
    """
    eoproduct_elem_list = [group[0] for group in list(group.groups)] + [var[0] for var in list(group.variables)]

    for sub_group in [group_data[1] for group_data in list(group.groups)]:
        # Check that subgroups are not empty
        if len(list(sub_group)) == 0:
            delimiter = "/"
            out_anomalies.append(
                AnomalyDescriptor(
                    "STRUCTURE",
                    f"Group {delimiter.join( list(sub_group.relative_path) + [sub_group.name],)} cannot be empty",
                ),
            )
            logger.debug(f"Group {delimiter.join( list(sub_group.relative_path) + [sub_group.name],)} cannot be empty")
    for elem_name in eoproduct_elem_list:
        # Check variable format validity
        if isinstance(group[elem_name], EOGroup):
            check_group_validity(group[elem_name], out_anomalies, logger)  # type: ignore

        # Check subgroup format validity
        elif isinstance(group[elem_name], EOVariable):
            check_variable_validity(group[elem_name], out_anomalies, logger)  # type: ignore


def check_variable_validity(variable: EOVariable, out_anomalies: List[AnomalyDescriptor], logger: Logger) -> None:
    """
    Check if the input variable has a format matching the template

    Parameters
    ----------
        variable (EOVariable): input EOVariable
    """

    # ---------- Generic checks

    if variable.ndim <= 1:
        out_anomalies.append(
            AnomalyDescriptor(
                "STRUCTURE",
                f"Value of EOVariable {variable.path} cannot be a scalar",
            ),
        )
        logger.debug(f"Value of EOVariable {variable.path} cannot be a scalar")
    # Check variable attributes
    attr_list = list(variable.attrs.keys())

    # Check the mandatory and optional variable attributes
    for mandat_attr in MANDATORY_VARIABLE_ATTRS:
        if mandat_attr not in attr_list:
            out_anomalies.append(
                AnomalyDescriptor(
                    "STRUCTURE",
                    f"Mandatory attribute {mandat_attr} not present in {variable.name} variable attributes",
                ),
            )
            logger.debug(f"Mandatory attribute {mandat_attr} not present in {variable.name} variable attributes")
    # This needs to be simplified
    for attr in [opt_attr for opt_attr in attr_list if opt_attr not in MANDATORY_VARIABLE_ATTRS]:
        if attr not in OPTIONAL_VARIABLE_ATTRS:
            out_anomalies.append(
                AnomalyDescriptor(
                    "STRUCTURE",
                    f"""{variable.path}/{attr} not in optional variable attributes list:"""
                    f"""{list(OPTIONAL_VARIABLE_ATTRS.keys())}""",
                ),
            )
            logger.debug(
                f"""{variable.path}/{attr} not in optional variable attributes list:"""
                f"""{list(OPTIONAL_VARIABLE_ATTRS.keys())}""",
            )


def check_stac_validity(product: EOProduct, out_anomalies: List[AnomalyDescriptor], logger: Logger) -> None:
    """
    Check if the input product has a valid STAC.
    A generic EOProduct validation is applied for all products.
    What's more, if the product type is defined, a product validation based on the templates data structure
    is also applied.

    Parameters
    ----------
        product (EOProduct): input EOProduct
        validation_mode (str): selected validation mode: possible values
    """
    # STAC metadata check
    logger.debug("Validating metadata (stac_discovery + other_metadata) from the EOProduct...")
    stac_utils_folder = os.path.join(EOPF_CPM_PATH.path, "product", "stac_extensions")

    if "stac_discovery" not in product.attrs:
        out_anomalies.append(
            AnomalyDescriptor(
                "STAC",
                "No stac_discovery dict in products attributes, cancelling STAC validation",
            ),
        )
        logger.debug("No stac_discovery dict in products attributes, cancelling STAC validation")
        return

    stac_discovery_data = product.attrs["stac_discovery"]
    if not isinstance(stac_discovery_data, dict):
        out_anomalies.append(
            AnomalyDescriptor(
                "STAC",
                "stac_discovery in products attributes is not a dict, cancelling STAC validation",
            ),
        )
        logger.debug("stac_discovery in products attributes is not a dict, cancelling STAC validation")
        return

    stac_item = AnyPath(stac_utils_folder) / STAC_ITEM_SCHEMA
    validate_against_schema_file(stac_item, stac_discovery_data, out_anomalies, logger)
    extensions = extract_stac_extensions(stac_discovery_data, logger)

    check_stac_extensions_list(stac_discovery_data, extensions, out_anomalies, logger)

    # Validate STAC metadata with the stac item standard schema + possible STAC extensions
    check_stac_schemas_validity(stac_discovery_data, extensions, stac_utils_folder, out_anomalies, logger)


def extract_stac_extensions(product_stac_dict: Dict[str, Any], logger: Logger) -> Dict[str, Tuple[str, str, str]]:
    """
    Check if all mandatory STAC extensions are listed in the stac_extension list


    Check also that all properties keyword are linked to its extension in the list

    Parameters
    ----------
        product_stac_dict (dict): stac_discovery metadata of the product
        path_to_stac_data (str): path to STAC standard schema and extensions
    """
    res: Dict[str, Tuple[str, str, str]] = {}
    if "stac_extensions" in product_stac_dict:
        for url in product_stac_dict["stac_extensions"]:

            parsed = urlparse(url)
            parts = parsed.path.strip("/").split("/")

            name = parts[-3]  # 'eopf-stac-extension'
            version = parts[-2]  # v1.2.0

            res[name] = (name, version, url)
            logger.debug(f"Found extension : {name}, {version}, {url}")

    return res


def check_stac_extensions_list(
    product_stac_dict: dict[str, Any],
    extensions: Dict[str, Tuple[str, str, str]],
    out_anomalies: List[AnomalyDescriptor],
    logger: Logger,
) -> None:
    for ext in MANDATORY_STAC_EXTENSIONS:
        if ext not in extensions:
            out_anomalies.append(AnomalyDescriptor("STAC", f"Mandatory extension {ext} not listed in stac_extensions"))
            logger.debug(f"Mandatory extension {ext} not listed in stac_extensions")
        else:
            logger.debug(f"Extension {ext} found in the list of stac_extensions")
    # For each attribute, check if the latter is linked to a STAC extension, if yes
    # load the associated json schema of the extension and validate the STAC attribute according
    # to this schema
    used_extension_list = []
    for key, val in product_stac_dict.items():
        # STAC extension validation
        if key == "properties":
            for prop_key, prop_val in product_stac_dict[key].items():
                if ":" in prop_key:
                    extension = prop_key.split(":")[0]
                    extension = KEYWORD_TO_EXTENSION.get(extension, extension)
                    used_extension_list.append(extension)

    ext_to_search = list(sorted(set(used_extension_list)))
    for ext in ext_to_search:
        if ext not in extensions:
            out_anomalies.append(
                AnomalyDescriptor(
                    "STAC",
                    f"Extension {ext} used in properties but not listed in stac_extensions",
                ),
            )
            logger.debug(f"Extension {ext} used in properties but not listed in stac_extensions")
        else:
            logger.debug(f"Extension {ext} used is correctly listed in stac_extensions")

    for ext in extensions:
        if ext not in ext_to_search:
            out_anomalies.append(
                AnomalyDescriptor(
                    "STAC",
                    f"Extension {ext} listed in stac_extensions but not used",
                ),
            )
            logger.debug(f"Extension {ext} listed in stac_extensions but not used")
        else:
            logger.debug(f"Extension {ext} listed in stac_extensions is used")

    return


def check_stac_schemas_validity(
    product_stac_dict: dict[str, Any],
    extensions: Dict[str, Tuple[str, str, str]],
    path_to_stac_data: str,
    out_anomalies: List[AnomalyDescriptor],
    logger: Logger,
) -> None:
    """Check that all elements from the STAC data follow the STAC standards (and STAC extensions)
    Check if STAC metadata of the input product have a valid format
    Links to the STAC item specifications:
    https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#item-fields

    Corresponding jsonschema:
    https://github.com/radiantearth/stac-spec/blob/master/item-spec/json-schema/item.json

    Parameters
    ----------
        product_stac_dict (dict): stac_discovery metadata of the product
        path_to_stac_data (str): path to STAC standard schema and extensions
    """
    for name, version, url in extensions.values():
        extension_local = AnyPath(path_to_stac_data) / "extensions" / f"{name}_{version}.json"
        if not extension_local.exists():
            extension_local = AnyPath(url)
        validate_against_schema_file(extension_local, product_stac_dict, out_anomalies, logger)

    logger.debug("STAC Schemas validation finished")


def validate_against_schema_file(
    extension_file_to_validate: AnyPath,
    product_stac_dict: dict[str, Any],
    out_anomalies: list[AnomalyDescriptor],
    logger: Logger,
) -> None:
    # Check if the attribute validates the jsonschema
    try:
        ext = file_utils.load_json_file(extension_file_to_validate)
    except FileNotFoundError:
        out_anomalies.append(
            AnomalyDescriptor(
                "STAC",
                f"Extension {extension_file_to_validate.path} not found !!!",
            ),
        )
        logger.debug(f"Extension {extension_file_to_validate.path} not found !!!")
        return
    try:
        logger.debug(f"Validating STAC data with the {extension_file_to_validate.path} extension schema")
        jsonschema.validate(product_stac_dict, ext)
        logger.debug(f"STAC data is valid with the {extension_file_to_validate.path} extension schema")
    except ValidationError as e:
        out_anomalies.append(
            AnomalyDescriptor(
                "STAC",
                f"Error validating STAC metadata with extension {extension_file_to_validate.path}: {e}",
            ),
        )
        logger.debug(f"Error validating STAC metadata with extension {extension_file_to_validate.path}: {e}")
