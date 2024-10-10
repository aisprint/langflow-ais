from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

import astra_assistants.tools as astra_assistants_tools
from loguru import logger

import langflow.components.astra_assistants.tools as langflow_assistant_tools
from langflow.custom.utils import abuild_custom_components, build_custom_components

if TYPE_CHECKING:
    from langflow.services.cache.base import CacheService
    from langflow.services.settings.service import SettingsService


async def aget_all_types_dict(components_paths, tool_packages=None):
    """Get all types dictionary combining native and custom components."""
    return await abuild_custom_components(components_paths=components_paths, tool_packages=tool_packages)


def get_all_types_dict(components_paths):
    """Get all types dictionary combining native and custom components."""
    return build_custom_components(components_paths=components_paths)


# TypeError: unhashable type: 'list'
def key_func(*args, **kwargs):
    # components_paths is a list of paths
    return json.dumps(args) + json.dumps(kwargs)


# is this still used? seems like get_and_cache_all_types_dict is used instead
async def aget_all_components(components_paths, as_dict=False):
    """Get all components names combining native and custom components."""
    all_types_dict = await aget_all_types_dict(components_paths)
    components = {} if as_dict else []
    for category in all_types_dict.values():
        for component in category.values():
            component["name"] = component["display_name"]
            if as_dict:
                components[component["name"]] = component
            else:
                components.append(component)
    return components


# is this still used? seems like get_and_cache_all_types_dict is used instead
def get_all_components(components_paths, as_dict=False):
    """Get all components names combining native and custom components."""
    all_types_dict = get_all_types_dict(components_paths)
    components = [] if not as_dict else {}
    for category in all_types_dict.values():
        for component in category.values():
            component["name"] = component["display_name"]
            if as_dict:
                components[component["name"]] = component
            else:
                components.append(component)
    return components


all_types_dict_cache = None


async def get_and_cache_all_types_dict(
    settings_service: SettingsService,
    cache_service: CacheService,  # not used?
    force_refresh: bool = False,  # not used?
    lock: asyncio.Lock | None = None,  # not used?
):
    tool_packages = [astra_assistants_tools, langflow_assistant_tools]
    global all_types_dict_cache
    if all_types_dict_cache is None:
        logger.debug("Building langchain types dict")
        all_types_dict_cache = await aget_all_types_dict(
            settings_service.settings.components_path, tool_packages=tool_packages
        )

    return all_types_dict_cache
