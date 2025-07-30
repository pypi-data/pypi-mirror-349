# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Module for publishing and unpublishing Fabric workspace items."""

import base64
import json
import logging
from typing import Optional

import fabric_cicd._items as items
from fabric_cicd import constants
from fabric_cicd._common._check_utils import check_regex
from fabric_cicd._common._logging import print_header
from fabric_cicd._common._validate_input import (
    validate_fabric_workspace_obj,
)
from fabric_cicd.fabric_workspace import FabricWorkspace

logger = logging.getLogger(__name__)


def publish_all_items(fabric_workspace_obj: FabricWorkspace, item_name_exclude_regex: Optional[str] = None) -> None:
    """
    Publishes all items defined in the `item_type_in_scope` list of the given FabricWorkspace object.

    Args:
        fabric_workspace_obj: The FabricWorkspace object containing the items to be published.
        item_name_exclude_regex: Regex pattern to exclude specific items from being published.


    Examples:
        Basic usage
        >>> from fabric_cicd import FabricWorkspace, publish_all_items
        >>> workspace = FabricWorkspace(
        ...     workspace_id="your-workspace-id",
        ...     repository_directory="/path/to/repo",
        ...     item_type_in_scope=["Environment", "Notebook", "DataPipeline"]
        ... )
        >>> publish_all_items(workspace)

        With regex name exclusion
        >>> from fabric_cicd import FabricWorkspace, publish_all_items
        >>> workspace = FabricWorkspace(
        ...     workspace_id="your-workspace-id",
        ...     repository_directory="/path/to/repo",
        ...     item_type_in_scope=["Environment", "Notebook", "DataPipeline"]
        ... )
        >>> exclude_regex = ".*_do_not_publish"
        >>> publish_all_items(workspace, exclude_regex)
    """
    fabric_workspace_obj = validate_fabric_workspace_obj(fabric_workspace_obj)

    if "disable_workspace_folder_publish" not in constants.FEATURE_FLAG:
        fabric_workspace_obj._refresh_deployed_folders()
        fabric_workspace_obj._refresh_repository_folders()
        fabric_workspace_obj._publish_folders()

    fabric_workspace_obj._refresh_deployed_items()
    fabric_workspace_obj._refresh_repository_items()

    if item_name_exclude_regex:
        logger.warning(
            "Using item_name_exclude_regex is risky as it can prevent needed dependencies from being deployed.  Use at your own risk."
        )
        fabric_workspace_obj.publish_item_name_exclude_regex = item_name_exclude_regex

    if "VariableLibrary" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Variable Libraries")
        items.publish_variablelibraries(fabric_workspace_obj)
    if "Warehouse" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Warehouses")
        items.publish_warehouses(fabric_workspace_obj)
    if "Lakehouse" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Lakehouses")
        items.publish_lakehouses(fabric_workspace_obj)
    if "SQLDatabase" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing SQL Databases")
        items.publish_sqldatabases(fabric_workspace_obj)
    if "MirroredDatabase" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing MirroredDatabase")
        items.publish_mirroreddatabase(fabric_workspace_obj)
    if "Environment" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Environments")
        items.publish_environments(fabric_workspace_obj)
    if "Notebook" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Notebooks")
        items.publish_notebooks(fabric_workspace_obj)
    if "SemanticModel" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing SemanticModels")
        items.publish_semanticmodels(fabric_workspace_obj)
    if "Report" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Reports")
        items.publish_reports(fabric_workspace_obj)
    if "DataPipeline" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing DataPipelines")
        items.publish_datapipelines(fabric_workspace_obj)
    if "CopyJob" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing CopyJobs")
        items.publish_copyjobs(fabric_workspace_obj)
    if "Eventhouse" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Eventhouses")
        items.publish_eventhouses(fabric_workspace_obj)
    if "KQLDatabase" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing KQL Databases")
        items.publish_kqldatabases(fabric_workspace_obj)
    if "KQLQueryset" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing KQL Querysets")
        items.publish_kqlquerysets(fabric_workspace_obj)
    if "Reflex" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Activators")
        items.publish_activators(fabric_workspace_obj)
    if "Eventstream" in fabric_workspace_obj.item_type_in_scope:
        print_header("Publishing Eventstreams")
        items.publish_eventstreams(fabric_workspace_obj)

    # Check Environment Publish
    if "Environment" in fabric_workspace_obj.item_type_in_scope:
        print_header("Checking Environment Publish State")
        items.check_environment_publish_state(fabric_workspace_obj)


def unpublish_all_orphan_items(fabric_workspace_obj: FabricWorkspace, item_name_exclude_regex: str = "^$") -> None:
    """
    Unpublishes all orphaned items not present in the repository except for those matching the exclude regex.

    Args:
        fabric_workspace_obj: The FabricWorkspace object containing the items to be published.
        item_name_exclude_regex: Regex pattern to exclude specific items from being unpublished. Default is '^$' which will exclude nothing.

    Examples:
        Basic usage
        >>> from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items
        >>> workspace = FabricWorkspace(
        ...     workspace_id="your-workspace-id",
        ...     repository_directory="/path/to/repo",
        ...     item_type_in_scope=["Environment", "Notebook", "DataPipeline"]
        ... )
        >>> publish_all_items(workspace)
        >>> unpublish_orphaned_items(workspace)

        With regex name exclusion
        >>> from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items
        >>> workspace = FabricWorkspace(
        ...     workspace_id="your-workspace-id",
        ...     repository_directory="/path/to/repo",
        ...     item_type_in_scope=["Environment", "Notebook", "DataPipeline"]
        ... )
        >>> publish_all_items(workspace)
        >>> exclude_regex = ".*_do_not_delete"
        >>> unpublish_orphaned_items(workspace, exclude_regex)
    """
    fabric_workspace_obj = validate_fabric_workspace_obj(fabric_workspace_obj)

    regex_pattern = check_regex(item_name_exclude_regex)

    fabric_workspace_obj._refresh_deployed_items()
    fabric_workspace_obj._refresh_repository_items()
    print_header("Unpublishing Orphaned Items")

    # Lakehouses, SQL Databases, and Warehouses can only be unpublished if their feature flags are set
    unpublish_flag_mapping = {
        "Lakehouse": "enable_lakehouse_unpublish",
        "SQLDatabase": "enable_sqldatabase_unpublish",
        "Warehouse": "enable_warehouse_unpublish",
    }

    # Define order to unpublish items
    unpublish_order = []
    for item_type in [
        "Eventstream",
        "Reflex",
        "KQLQueryset",
        "KQLDatabase",
        "Eventhouse",
        "DataPipeline",
        "Report",
        "SemanticModel",
        "Notebook",
        "Environment",
        "MirroredDatabase",
        "SQLDatabase",
        "Lakehouse",
        "Warehouse",
        "VariableLibrary",
    ]:
        if item_type in fabric_workspace_obj.item_type_in_scope:
            unpublish_flag = unpublish_flag_mapping.get(item_type)
            # Append item_type if no feature flag is required or the corresponding flag is enabled
            if not unpublish_flag or unpublish_flag in constants.FEATURE_FLAG:
                unpublish_order.append(item_type)

    for item_type in unpublish_order:
        deployed_names = set(fabric_workspace_obj.deployed_items.get(item_type, {}).keys())
        repository_names = set(fabric_workspace_obj.repository_items.get(item_type, {}).keys())

        to_delete_set = deployed_names - repository_names
        to_delete_list = [name for name in to_delete_set if not regex_pattern.match(name)]

        if item_type == "DataPipeline":
            # need to first define order of delete
            unsorted_pipeline_dict = {}

            for item_name in to_delete_list:
                # Get deployed item definition
                # https://learn.microsoft.com/en-us/rest/api/fabric/core/items/get-item-definition
                item_guid = fabric_workspace_obj.deployed_items[item_type][item_name].guid
                response = fabric_workspace_obj.endpoint.invoke(
                    method="POST", url=f"{fabric_workspace_obj.base_api_url}/items/{item_guid}/getDefinition"
                )

                for part in response["body"]["definition"]["parts"]:
                    if part["path"] == "pipeline-content.json":
                        # Decode Base64 string to dictionary
                        decoded_bytes = base64.b64decode(part["payload"])
                        decoded_string = decoded_bytes.decode("utf-8")
                        unsorted_pipeline_dict[item_name] = json.loads(decoded_string)

            # Determine order to delete w/o dependencies
            to_delete_list = items.sort_datapipelines(fabric_workspace_obj, unsorted_pipeline_dict, "Deployed")

        for item_name in to_delete_list:
            fabric_workspace_obj._unpublish_item(item_name=item_name, item_type=item_type)

    fabric_workspace_obj._refresh_deployed_items()
    fabric_workspace_obj._refresh_deployed_folders()
    if "disable_workspace_folder_publish" not in constants.FEATURE_FLAG:
        fabric_workspace_obj._unpublish_folders()
