# South Park Bloodbath — Spanish Version

This repository is configured for **Friday Night Funkin': Psych Engine 0.7.3**.

## Engine version

The `PsychEngine/` directory is a Git submodule pinned to the official Psych Engine **0.7.3** source commit:

- Upstream: https://github.com/ShadowMario/FNF-PsychEngine
- Tag: `0.7.3`
- Commit: `2dfa27773a3668e0c1b043a3fb4348942c8a6fb3`

Clone the project with the engine source included:

```bash
git clone --recurse-submodules https://github.com/Redev325/spanishversthpbb.git
```

## Importing the supplied mod folder

The uploaded `Bloodbath Spanish Mix PC [RTX].zip` contains a **Psych Engine mod folder**, not the Psych Engine source itself. Its directory layout (characters, custom_events, custom_notetypes, data, images, scripts, songs, sounds, stages, and weeks) belongs inside the engine's `mods/` directory.

After extracting the prepared archive, copy:

```
mods/Bloodbath Spanish Mix PC [RTX]/
```

into:

```
PsychEngine/mods/Bloodbath Spanish Mix PC [RTX]/
```

Keep the folder name and internal paths unchanged for the first test. The original archive includes 838 files. The source assets have not been translated or modified during extraction.

## Source archive notes

The archive's metadata is inconsistent: `pack.json` names the pack **Last Chance V7 (Non Pixelated)**, while the week and song folders refer to `LC` and `bloodbath-spanish-mix`. Those values are preserved as supplied; review them before changing week names or identifiers.

## Build

Follow the build instructions in the pinned Psych Engine source. Do not copy this mod folder into the repository root of the engine submodule; it must be placed under `PsychEngine/mods/`.
