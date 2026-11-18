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


## Browser-specific engine patch

The preparation step changes Psych Engine's unconditional `DISCORD_ALLOWED` define to a desktop-only define and wraps `backend/Discord.hx` with a no-op HTML5 implementation. The upstream file imports C++ pointer APIs and creates a desktop thread, so it cannot be compiled into the JavaScript target. The web workflow therefore does not install `hxdiscord_rpc`.


## Compile dependency versions and HTML5 file access

The initial library pins fixed the missing `FlxSound` and `FlxRuntimeShader` classes, but HaxeFlixel 5.3.0 is still too old for other APIs used by this Psych Engine source revision. The engine uses `FlxCamera.filters`, `FlxAnimationController.timeScale`, and `FlxG.animationTimeScale`; the latter was added in HaxeFlixel 5.5.0. Its animation helpers also pass a floating-point frame rate to `addByPrefix`, which is supported by HaxeFlixel 5.6.1.

The workflow therefore uses Haxe 4.3.2, Lime 8.1.2, OpenFL 9.3.3, HaxeFlixel 5.6.1, and flixel-addons 3.2.2. These versions align with the published Psych Engine dependency guidance. The workflow checks the required Flixel APIs before starting the compile.

The HTML5 preparation script also patches the two desktop `File.getContent` calls in Psych Engine's `Paths.loadAnimateAtlas`, and patches the unguarded JSON/XML file reads in the selected `flxanimate` dependency to use `openfl.Assets.getText` for the JavaScript target. Native builds retain their normal filesystem reads. The WOFF generation notices for the mod fonts are non-fatal warnings; they are not the cause of a failed compile.


## Follow-up HTML5 source compatibility fixes

The current preparation step also guards the character editor's operating-system directory scan from the JavaScript target, qualifies the local `options.Option` class explicitly, updates the Flixel logger call, and uses `FlxObject.setPosition` for the stage camera-follow point. The FlxAnimate filter renderer imports Lime's `ImageCanvasUtil` and is granted access to the Lime `ImageBuffer` canvas context that OpenFL uses internally.
