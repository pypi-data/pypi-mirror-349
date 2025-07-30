# plugin.py
import logging
from typing import Annotated, Any

from fastpluggy.core.database import session_scope, create_table_if_not_exist
from fastpluggy.core.menu.schema import MenuItem
from fastpluggy.core.module_base import FastPluggyBaseModule
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.core.tools.install import is_installed

from .config import RedisToolsSettings
from .router import redis_router


class RedisToolsPlugin(FastPluggyBaseModule):
    module_name: str = "redis_tools"
    module_version: str = "0.0.7"

    module_menu_name: str = "Redis Tools"
    module_menu_icon:str = "fa-solid fa-database"
    module_menu_type: str = "main"

    module_settings: Any = RedisToolsSettings
    module_router: Any = redis_router

    depends_on: dict = {}

    optional_dependencies: dict = {
        "tasks_worker": ">=0.1.0",
    }

    def on_load_complete(self, fast_pluggy: Annotated["FastPluggy", InjectDependency]) -> None:
        pass