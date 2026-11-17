# HTML5 port notes

## Source package findings

The supplied archive contains 838 files (873 ZIP entries including directory entries), with the chart at:

`data/bloodbath-spanish-mix/bloodbath-spanish-mix-hard.json`

The chart has 1,550 sections, 2,294 notes, and 57 distinct event names. The original note types found in the chart are `GF Sing`, `kyle`, `craignote`, `Glitch Note`, `cledyNOTE`, `glitchColor`, and `Trail Note Shake`.

The archive has `songs/bloodbath-spanish-mix/Inst.ogg`, but no `Voices.ogg`. The HTML5 preparation step therefore sets `needsVoices` to `false` and converts OGG files to MP3 because the Psych Engine 0.7.3 web asset manifest excludes OGG files.

## Why the mod is embedded

Psych Engine 0.7.3 enables `MODS_ALLOWED`, `HSCRIPT_ALLOWED`, and `LUA_ALLOWED` only for desktop builds in `Project.xml`. Its normal mod filesystem loader and LuaJIT scripts are not available to the HTML5 target. The preparation script places character definitions, stage definitions, charts, week metadata, images, sounds, and the song instrumental into the shared and songs asset libraries that are compiled into the web build.

## Native behavior currently implemented

- Registers a `south` Haxe stage in `PlayState`.
- Recreates the base `white`, `bg`, `bg2`, `bg3`, `bg4`, `kyle`, `kyle s`, `anim1`–`anim4`, `Vignette`, `thefunnyeffect`, `black`, and `blackbar` layers from the supplied stage assets.
- Ports the `kyle` custom note's `noAnimation` behavior.
- Uses Psych Engine's built-in `GF Sing` behavior.
- Handles selected stage events: `afadein`, `afadeout`, `badapplelol`, `aofisetiBF`, `aofisetiDad`, `aCamaraZoom` variants, camera flashes, selected sprite animation, cinematic bar fade, character alpha fades, darkness fade, and selected stage property changes.

## Known gaps

The original archive includes hundreds of Lua custom-event files and song scripts. The first native pass does not translate all of them. Several chart event families and their shader effects, the full Kyle/Clyde/Craig extra-character choreography, glitch note effects, arrow manipulation, lyrics overlays, and other scripted scene changes remain incomplete. Those behaviors need individual Haxe ports, followed by a full playthrough test in the browser.

The build workflow must not be described as a fully faithful release until the deployed page is loaded and the complete song is tested from beginning to end.
