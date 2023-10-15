# LSP-biome

[Biome](https://biomejs.dev/) - One toolchain for your web project. Format, lint, and more in a fraction of a second.

- Fast: Built with Rust and an innovative architecture inspired by rust-analyzer.
- Scalable: Designed to handle codebases of any size. Focus on growing product instead of your tools.
- Actionable & Informative: Avoid obscure error messages, when we tell you something is wrong, we tell you exactly where the problem is and how to fix it.
- Simple: Zero configuration needed to get started. Extensive options available for when you need them.
- Optimized: With tight internal integration we are able to reuse previous work and any improvement to one tool improves them all.
- Batteries Included: Out of the box support for all the language features you use today. First class support for TypeScript and JSX.

## Installation

1. Install [LSP](https://packagecontrol.io/packages/LSP) and [LSP-biome](https://packagecontrol.io/packages/LSP-biome) via Package Control.
2. (Optional but recommended) Install [LSP-file-watcher-chokidar](https://github.com/sublimelsp/LSP-file-watcher-chokidar) via Package Control to enable functionality to notify the server about changes to the `biome.json` configuration file.
3. Restart Sublime.

## Configuration

Open the configuration file using the Command Palette `Preferences: LSP-biome Settings` command or from the Sublime menu.

> **Note**
> By default Biome requires a configuration file (`biome.json`) in the root of the project to enable syntax errors, formatting and linting. This can be changed through the `biome.requireConfiguration` option in `Preferences: LSP-biome Settings`.

## Biome Resolution

The package tries to use Biome from your project's local dependencies (`node_modules/.bin/biome`). We recommend adding Biome as a project dependency to ensure that NPM scripts and the extension use the same Biome version.

You can also explicitly specify the `biome` binary the extension should use by configuring the `biome.lspBin` setting in `LSP-biome` Settings.

If the project has no dependency on Biome and no explicit path is configured, the extension uses the Biome version managed by this package.

## Usage

### Format document

To format an entire document, open the _Command Palette_ (<kbd>Ctrl</kbd>/<kbd title="Cmd">⌘</kbd>+<kbd title="Shift">⇧</kbd>+<kbd>P</kbd>) and select `LSP: Format Document`.

To format a text range, select the text you want to format, open the _Command Palette_ (<kbd>Ctrl</kbd>/<kbd title="Cmd">⌘</kbd>+<kbd title="Shift">⇧</kbd>+<kbd>P</kbd>), and select `LSP: Format Selection`.

### Fix on save

To enable fix on save, open `Preferences: LSP Settings` from the _Command Palette_ and set:

```json
{
    "lsp_code_actions_on_save": {
        "quickfix.biome": true
    }
}
```

### Imports Sorting [Experimental]

Biome has experimental support for imports sorting through the "Organize Imports" code action. This action is accessible through the _Command Palette_ (<kbd>Ctrl</kbd>/<kbd title="Cmd">⌘</kbd>+<kbd title="Shift">⇧</kbd>+<kbd>P</kbd>) by selecting `LSP-biome: Organize Imports`.

Currently, this functionality needs to be explicitly enabled in the `biome.json` configuration file:

```json
{
    "organizeImports": {
        "enabled": true
    }
}
```

You can add the following to `Preferences: LSP Settings` if you want the action to run automatically on save instead of calling it manually:

```json
{
    "lsp_code_actions_on_save":{
        "source.organizeImports.biome": true
    }
}
```
