from __future__ import annotations

from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import PluginStartError
from LSP.plugin import ServerResponse
from LSP.plugin import WorkspaceFolder
from lsp_utils import NodeManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing_extensions import override

BIOME_LOCATION = Path('node_modules', '@biomejs', 'biome', 'bin', 'biome')


class LspBiomePlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        server_path: str | None = context.configuration.server_path
        if server_path and server_path != 'auto':
            if (biome_path := cls._get_workspace_relative_path(Path(server_path), context.workspace_folders)):
                context.configuration.server_path = str(biome_path)
            else:
                raise PluginStartError(
                    f'[LSP-biome] Could not resolve biome binary from specified server_path {server_path}.')
        elif (biome_path := cls._get_workspace_dependency(context.workspace_folders)):
            context.configuration.server_path = str(biome_path)
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath('Packages', package_name, 'language-server'),
            BIOME_LOCATION,
            node_version_requirement='>=14.21.3',
        )

    @classmethod
    def _get_workspace_relative_path(cls, lsp_bin: Path, workspace_folders: list[WorkspaceFolder]) -> Path | None:
        if lsp_bin.is_absolute():
            return lsp_bin
        for folder in workspace_folders:
            if (possible_path := Path(folder.path, lsp_bin)).is_file():
                return possible_path
        return None

    @classmethod
    def _get_workspace_dependency(cls, workspace_folders: list[WorkspaceFolder]) -> Path | None:
        for folder in workspace_folders:
            if (binary_path := Path(folder.path, BIOME_LOCATION)).is_file():
                return binary_path
        return None

    @override
    def on_server_response_async(self, response: ServerResponse) -> None:
        if response['method'] == 'initialize':
            if (session := self.weaksession()) and (version := response['result'].get('serverInfo', {}).get('version')):
                session.set_config_status_async(version)


def plugin_loaded() -> None:
    LspBiomePlugin.register()


def plugin_unloaded() -> None:
    LspBiomePlugin.unregister()
