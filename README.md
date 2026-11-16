# serein-cli

The command line tool for the [Serein shell](https://github.com/esrahmn/serein-shell): wallpapers, colour
schemes, screenshots, screen recording, clipboard and emoji pickers, and a handle on the running shell.

It is a fork of [caelestia-cli](https://github.com/caelestia-dots/cli) (GPL-3.0-only) and is **not affiliated
with** the Caelestia project. All credit for the original tool goes to its authors; see
[Credits and license](#credits-and-license).

## What is different from caelestia-cli

- The command is `serein` (module `serein`, package `serein-cli`), so it installs next to `caelestia-cli`
  without clashing.
- `serein shell ...` and `serein screenshot` talk to the Serein shell (`qs -c serein`) instead of
  `qs -c caelestia`.
- A `serein` colour scheme (`serein scheme set -n serein`: night blue slate surfaces, aqua-blue primary, periwinkle
  tertiary; dark and light) and it is the default when no scheme has been set yet (upstream defaults to catppuccin).
- The `caelestia` colour scheme is removed (`serein` replaces it). Generated Qt, Warp and Discord themes are named
  *Serein*; Zed, Pandora and Spicetify themes keep the `caelestia` name because applications select them by name.
- Notifications are sent as `serein-cli`, and `serein --version` lists the CLI's own version first, and the plugin helper is looked up in `/usr/lib/serein`.
- **Data paths follow Serein**: `~/.config/serein` (including `cli.json` and `templates/`), `~/.local/state/serein`,
  `~/.local/share/serein` and `~/.cache/serein`, the same folders [serein-plugin](https://github.com/esrahmn/serein-plugin)
  reads. To bring existing Caelestia data over, run the shell's `scripts/migrate-from-caelestia.sh` once. Generated
  theme files (`caelestia.theme.css`, ...) keep their names, so existing application configs keep working.
- `serein install` and `serein update` still deploy the *upstream* Caelestia dotfiles (they are inherited
  as-is); Serein does not need them.

## Dependencies

Same as caelestia-cli: `python`, `python-pillow`, `python-materialyoucolor`, `libnotify`, `swappy`, `grim`,
`dart-sass`, `wl-clipboard`, `slurp`, `gpu-screen-recorder`, `dconf`, `cliphist`, `fuzzel`, `git`
(and `ffmpeg` for video wallpapers). See [upstream's list](https://github.com/caelestia-dots/cli#dependencies)
for what each one is used for.

## Install

Run it straight from a checkout:

```sh
git clone https://github.com/esrahmn/serein-cli ~/src/serein-cli
ln -s ~/src/serein-cli/bin/serein ~/.local/bin/serein   # needs ~/.local/bin in PATH
serein --version
```

`bin/serein` follows the symlink and runs `python -m serein` from the checkout, so `git pull` is all it takes to
update. Python 3.13 or newer is required.

Optional fish completions: copy or link `completions/serein.fish` into `~/.config/fish/completions/`.

## Usage

```sh
serein shell -s                     # list the shell's IPC commands
serein shell drawers toggle launcher
serein scheme list
serein wallpaper -f ~/Pictures/wall.png
serein screenshot
serein record
serein clipboard
serein emoji -p
```

Run `serein <command> --help` for the options of each command.

## Keeping up with upstream

```sh
git remote add upstream https://github.com/caelestia-dots/cli   # once
git fetch upstream
git merge upstream/main
```

Most conflicts will be in the files that were renamed (`src/caelestia` became `src/serein`), so merge carefully
and re-apply the `qs -c serein` and branding changes if upstream touches those lines.

## Credits and license

serein-cli is a modified version of **caelestia-cli** (<https://github.com/caelestia-dots/cli>), copyright its
authors, and it keeps its license.

It is free software, released under the **GNU General Public License v3.0 only**; see [LICENSE](LICENSE). In line
with the GPL, the changes made on top of caelestia-cli are summarised above and in the git history.
