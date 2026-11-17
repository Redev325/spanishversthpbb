# Bloodbath Spanish Mix — Psych Engine 0.7.3

This repository targets the official **Friday Night Funkin': Psych Engine 0.7.3** source, pinned as a Git submodule at commit `2dfa27773a3668e0c1b043a3fb4348942c8a6fb3`.

## HTML5 browser build

The original mod ZIP is too large to store as ordinary Git files and includes binary assets. Store it as a GitHub Release asset instead:

1. Open **Releases** in this repository and create a release tagged `source-v1.0.0`.
2. Rename the supplied ZIP to `bloodbath-spanish-mix-source.zip` and attach it to that release.
3. Publish the release.
4. Open **Actions → Build Bloodbath Spanish Mix HTML5 → Run workflow**. Keep the source release tag as `source-v1.0.0`.
5. When the build and deploy jobs succeed, open the GitHub Pages URL shown in the deploy job.

You can upload the archive with GitHub CLI by running:

```bash
bash tools/upload_source_release.sh "/path/to/Bloodbath Spanish Mix PC [RTX].zip"
```

The workflow checks out the pinned engine submodule, installs Haxe and the Psych Engine libraries, converts the mod's OGG audio to browser-compatible MP3 files, embeds the chart and assets into the engine's shared/song asset libraries, and builds the HTML5 target.

## Current HTML5 port scope

The supplied ZIP is a **Psych Engine mod package**, not a Haxe source project. Psych Engine's HTML5 target does not enable its desktop filesystem mod loader or LuaJIT mod scripts. The build therefore embeds the files and includes an initial native Haxe recreation of the `south` stage and selected chart behaviors.

The supplied chart contains 2,294 notes across 1,550 sections and 57 distinct event names. The first native port handles the `kyle` note's no-animation behavior, native `GF Sing`, core stage layers, camera zoom/position events, basic fades, flashes, Bad Apple silhouette transition, and selected sprite animations. Other Lua-driven custom events, shader effects, extra character choreography, and some note-type effects are not yet fully ported. A successful HTML5 compile is not the same as a verified full-song playthrough.

The ZIP contains `Inst.ogg` but no `Voices.ogg`, so the browser build marks the chart as instrumental-only. The supplied `LC.json` is preserved, including its current week/menu metadata.

See [docs/HTML5_PORT.md](docs/HTML5_PORT.md) for implementation scope and known gaps.
