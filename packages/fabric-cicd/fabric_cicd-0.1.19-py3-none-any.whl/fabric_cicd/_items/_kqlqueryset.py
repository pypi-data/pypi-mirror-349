# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Functions to process and deploy KQL Queryset item."""

import json
import logging

from fabric_cicd import FabricWorkspace
from fabric_cicd._common._exceptions import ParsingError
from fabric_cicd._common._file import File
from fabric_cicd._common._item import Item

logger = logging.getLogger(__name__)


def publish_kqlquerysets(fabric_workspace_obj: FabricWorkspace) -> None:
    """
    Publishes all KQL Queryset items from the repository.

    Args:
        fabric_workspace_obj: The FabricWorkspace object containing the items to be published.
    """
    item_type = "KQLQueryset"

    for item_name in fabric_workspace_obj.repository_items.get(item_type, {}):
        fabric_workspace_obj._publish_item(
            item_name=item_name, item_type=item_type, func_process_file=func_process_file
        )


def func_process_file(workspace_obj: FabricWorkspace, item_obj: Item, file_obj: File) -> str:
    """
    Custom file processing for kql queryset items.

    Args:
        workspace_obj: The FabricWorkspace object.
        item_obj: The item object.
        file_obj: The file object.
    """
    return replace_cluster_uri(workspace_obj, file_obj) if item_obj.type == "KQLQueryset" else file_obj.contents


def replace_cluster_uri(fabric_workspace_obj: FabricWorkspace, file_obj: File) -> str:
    """
    Replaces an empty cluster URI value in a KQL Queryset item with the cluster URI associated
    with its KQL Database source in the raw file content.

    Args:
        fabric_workspace_obj: The FabricWorkspace object.
        file_obj: The file object.
    """
    # Create a dictionary from the raw file
    json_content_dict = json.loads(file_obj.contents)

    queryset = json_content_dict.get("queryset")
    data_sources = queryset.get("dataSources") if queryset else None
    if not data_sources:
        return file_obj.contents

    # Get the KQL Database items from the deployed items
    fabric_workspace_obj._refresh_deployed_items()
    database_items = fabric_workspace_obj.deployed_items.get("KQLDatabase")

    # If the cluster URI is empty, replace it with the cluster URI of the KQL database
    for data_source in data_sources:
        if data_source.get("clusterUri") == "":
            database_item_name = data_source.get("databaseItemName")
            database_item = database_items.get(database_item_name) if database_items else None

            if not database_item:
                msg = f"Cannot find the KQL Database source with name {database_item_name} as it is not yet deployed."
                raise ParsingError(msg, logger)

            database_item_guid = database_item.guid
            # Get the cluster URI of the KQL database
            kqldatabase_data = fabric_workspace_obj.endpoint.invoke(
                method="GET",
                url=f"{fabric_workspace_obj.base_api_url}/kqlDatabases/{database_item_guid}",
            )
            kqldatabase_cluster_uri = kqldatabase_data["body"]["properties"]["queryServiceUri"]
            # Replace the cluster URI value
            data_source["clusterUri"] = kqldatabase_cluster_uri

    return json.dumps(json_content_dict, indent=2)
