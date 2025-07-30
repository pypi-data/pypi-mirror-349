# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Functions to process and deploy DataPipeline item."""

import json
import logging
import re
from collections import defaultdict, deque
from pathlib import Path

import dpath

import fabric_cicd.constants as constants
from fabric_cicd import FabricWorkspace
from fabric_cicd._common._exceptions import ParsingError
from fabric_cicd._common._file import File
from fabric_cicd._common._item import Item

logger = logging.getLogger(__name__)


def publish_datapipelines(fabric_workspace_obj: FabricWorkspace) -> None:
    """
    Publishes all data pipeline items from the repository in the correct order based on their dependencies.

    Args:
        fabric_workspace_obj: The FabricWorkspace object containing the items to be published.
    """
    item_type = "DataPipeline"

    # Get all data pipelines from the repository
    pipelines = fabric_workspace_obj.repository_items.get(item_type, {})

    unsorted_pipeline_dict = {}

    # Construct unsorted_pipeline_dict with dict of pipeline
    unsorted_pipeline_dict = {}
    for item_name, item_details in pipelines.items():
        with Path(item_details.path, "pipeline-content.json").open(
            encoding="utf-8",
        ) as f:
            raw_file = f.read()
        item_content_dict = json.loads(raw_file)

        unsorted_pipeline_dict[item_name] = item_content_dict

    publish_order = sort_datapipelines(fabric_workspace_obj, unsorted_pipeline_dict, "Repository")

    # Publish
    for item_name in publish_order:
        fabric_workspace_obj._publish_item(
            item_name=item_name, item_type=item_type, func_process_file=func_process_file
        )


def func_process_file(workspace_obj: FabricWorkspace, item_obj: Item, file_obj: File) -> str:  # noqa: ARG001
    """
    Custom file processing for datapipeline items.

    Args:
        workspace_obj: The FabricWorkspace object.
        item_obj: The item object.
        file_obj: The file object.
    """
    return replace_activity_workspace_ids(workspace_obj, file_obj)


def sort_datapipelines(fabric_workspace_obj: FabricWorkspace, unsorted_pipeline_dict: dict, lookup_type: str) -> list:
    """
    Output a sorted list that datapipelines should be published or unpublished with based on item dependencies.

    Args:
        fabric_workspace_obj: The FabricWorkspace object.
        unsorted_pipeline_dict: Dict representation of the pipeline-content file.
        lookup_type: Finding references in deployed file or repo file (Deployed or Repository).
    """
    # Step 1: Create a graph to manage dependencies
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    unpublish_items = []

    # Step 2: Build the graph and count the in-degrees
    for item_name, item_content_dict in unsorted_pipeline_dict.items():
        # In an unpublish case, keep track of items to get unpublished
        if lookup_type == "Deployed":
            unpublish_items.append(item_name)

        referenced_pipelines = _find_referenced_datapipelines(
            fabric_workspace_obj, item_content_dict=item_content_dict, lookup_type=lookup_type
        )

        for referenced_name in referenced_pipelines:
            graph[referenced_name].append(item_name)
            in_degree[item_name] += 1
        # Ensure every item has an entry in the in-degree map
        if item_name not in in_degree:
            in_degree[item_name] = 0

    # In an unpublish case, adjust in_degree to include entire dependency chain for each pipeline
    if lookup_type == "Deployed":
        for item_name in graph:
            if item_name not in in_degree:
                in_degree[item_name] = 0
            for neighbor in graph[item_name]:
                if neighbor not in in_degree:
                    in_degree[neighbor] += 1

    # Step 3: Perform a topological sort to determine the correct publish order
    zero_in_degree_queue = deque([item_name for item_name in in_degree if in_degree[item_name] == 0])
    sorted_items = []

    while zero_in_degree_queue:
        item_name = zero_in_degree_queue.popleft()
        sorted_items.append(item_name)

        for neighbor in graph[item_name]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    if len(sorted_items) != len(in_degree):
        msg = "There is a cycle in the graph. Cannot determine a valid publish order."
        raise ParsingError(msg, logger)

    # Remove items not present in unpublish list and invert order for deployed sort
    if lookup_type == "Deployed":
        sorted_items = [item_name for item_name in sorted_items if item_name in unpublish_items]
        sorted_items = sorted_items[::-1]

    return sorted_items


def _find_referenced_datapipelines(
    fabric_workspace_obj: FabricWorkspace, item_content_dict: dict, lookup_type: str
) -> list:
    """
    Scan through item dictionary and find pipeline references (including nested pipelines).

    Args:
        fabric_workspace_obj: The FabricWorkspace object.
        item_content_dict: Dict representation of the pipeline-content file.
        lookup_type: Finding references in deployed file or repo file (Deployed or Repository).
    """
    item_type = "DataPipeline"
    reference_list = []
    guid_pattern = re.compile(constants.VALID_GUID_REGEX)

    # Use the dpath library to search through the dictionary for all values that match the GUID pattern
    for _, value in dpath.search(item_content_dict, "**", yielded=True):
        if isinstance(value, str):
            match = guid_pattern.search(value)
            if match:
                # If a valid GUID is found, convert it to name. If name is not None, it's a pipeline and will be added to the reference list
                referenced_id = match.group(0)
                referenced_name = fabric_workspace_obj._convert_id_to_name(
                    item_type=item_type, generic_id=referenced_id, lookup_type=lookup_type
                )
                # Add pipeline to the reference list if it's not already present
                if referenced_name and referenced_name not in reference_list:
                    reference_list.append(referenced_name)

    return reference_list


def replace_activity_workspace_ids(fabric_workspace_obj: FabricWorkspace, file_obj: File) -> str:
    """
    Replaces all instances of non-default feature branch workspace IDs (actual guid of feature branch workspace)
    with target workspace ID found in DataPipeline activities.

    Args:
        fabric_workspace_obj: The FabricWorkspace object.
        file_obj: The file object.
    """
    # Create a dictionary from the raw file
    item_content_dict = json.loads(file_obj.contents)
    guid_pattern = re.compile(constants.VALID_GUID_REGEX)

    # Activities mapping dictionary: {Key: activity_name, Value: [item_type, item_id_name]}
    activities_mapping = {"RefreshDataflow": ["Dataflow", "dataflowId"]}

    # dpath library finds and replaces feature branch workspace IDs found in all levels of activities in the dictionary
    for path, activity_value in dpath.search(item_content_dict, "**/type", yielded=True):
        # Ensure the type value is a string and check if it is found in the activities mapping
        if type(activity_value) == str and activity_value in activities_mapping:
            # Split the path into components, create a path to 'workspaceId' and get the workspace ID value
            path = path.split("/")
            workspace_id_path = (*path[:-1], "typeProperties", "workspaceId")
            workspace_id = dpath.get(item_content_dict, workspace_id_path)

            # Check if the workspace ID is a valid GUID and is not the target workspace ID
            if guid_pattern.match(workspace_id) and workspace_id != fabric_workspace_obj.workspace_id:
                item_type, item_id_name = activities_mapping[activity_value]
                # Create a path to the item's ID and get the item ID value
                item_id_path = (*path[:-1], "typeProperties", item_id_name)
                item_id = dpath.get(item_content_dict, item_id_path)
                # Convert the item ID to a name to check if it exists in the repository
                item_name = fabric_workspace_obj._convert_id_to_name(
                    item_type=item_type, generic_id=item_id, lookup_type="Repository"
                )
                # If the item exists, the associated workspace ID is a feature branch workspace ID and will get replaced
                if item_name:
                    dpath.set(item_content_dict, workspace_id_path, fabric_workspace_obj.workspace_id)

    # Convert the updated dict back to a JSON string
    return json.dumps(item_content_dict, indent=2)
