from LSP.plugin import ClientConfig, Response, WorkspaceFolder
from LSP.plugin.core.protocol import InitializeResult
from LSP.plugin.core.typing import cast, List, Optional
from lsp_utils import NpmClientHandler
import os
import sublime

BIOME_LOCATION = os.path.join('@biomejs', 'biome', 'bin', 'biome')


class LspBiomePlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'node_modules', BIOME_LOCATION)

    @classmethod
    def required_node_version(cls) -> str:
        return '>=14'

    @classmethod
    def get_binary_arguments(cls) -> List[str]:
        return ['lsp-proxy']

    @classmethod
    def is_allowed_to_start(
        cls,
        window: sublime.Window,
        initiating_view: sublime.View,
        workspace_folders: List[WorkspaceFolder],
        configuration: ClientConfig
    ) -> Optional[str]:
        biome_path = cls._resolve_biome_path(workspace_folders, configuration)
        if not biome_path:
            return 'LSP-biome could not resolve specified biome binary.'
        server = cls.get_server()
        if server:
            configuration.command = [server.node_bin, biome_path] + cls.get_binary_arguments()
        return None

    @classmethod
    def _resolve_biome_path(
        cls, workspace_folders: List[WorkspaceFolder], configuration: ClientConfig
    ) -> Optional[str]:
        rome_lsp_bin = configuration.settings.get('biome.lspBin')
        if isinstance(rome_lsp_bin, str) and rome_lsp_bin:
            return cls._get_workspace_relative_path(rome_lsp_bin, workspace_folders)
        return cls._get_workspace_dependency(workspace_folders) or '${server_path}'

    @classmethod
    def _get_workspace_relative_path(cls, rome_lsp_bin: str, workspace_folders: List[WorkspaceFolder]) -> Optional[str]:
        if os.path.isabs(rome_lsp_bin):
            return rome_lsp_bin
        for folder in workspace_folders:
            possible_path = os.path.join(folder.path, rome_lsp_bin)
            if os.path.isfile(possible_path):
                return possible_path
        return None

    @classmethod
    def _get_workspace_dependency(cls, workspace_folders: List[WorkspaceFolder]) -> Optional[str]:
        for folder in workspace_folders:
            binary_path = os.path.join(folder.path, 'node_modules', BIOME_LOCATION)
            if os.path.isfile(binary_path):
                return binary_path
        return None

    def on_server_response_async(self, method: str, response: Response) -> None:
        if method == 'initialize':
            initializeResponse = cast(Response[InitializeResult], response)
            version = initializeResponse.result.get('serverInfo', {}).get('version')
            if version:
                session = self.weaksession()
                if session:
                    session.set_config_status_async(version)


def plugin_loaded() -> None:
    LspBiomePlugin.setup()


def plugin_unloaded() -> None:
    LspBiomePlugin.cleanup()
