#!/usr/bin/env python3
"""Prepare Bloodbath Spanish Mix for an embedded Psych Engine 0.7.3 HTML5 build.

Psych Engine's desktop mod filesystem is not available on HTML5. This script
embeds the mod's data and original audio files in the shared/songs asset
libraries, enables the web OGG asset path, and adds a native Haxe stage
implementation for the chart's south stage.

This is an initial browser port: Lua-only custom events and shader effects that
are not explicitly ported in South.hx will not execute in the HTML5 build.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

SONG = "bloodbath-spanish-mix"
WEEK = "LC"
CHART = f"{SONG}-hard.json"

SOUTH_HX = r'''package states.stages;

import backend.BaseStage;
import objects.BGSprite;
import states.PlayState;
import flixel.FlxSprite;
import flixel.tweens.FlxEase;
import flixel.tweens.FlxTween;
import flixel.util.FlxColor;

/** Native, asset-embedded stage for the Bloodbath Spanish Mix browser build. */
class South extends BaseStage
{
    var sprites:Map<String, BGSprite> = new Map<String, BGSprite>();
    var whiteBg:BGSprite;
    var blackOverlay:BGSprite;
    var blackBar:BGSprite;
    var bg1:BGSprite;
    var bg2:BGSprite;
    var bg3:BGSprite;
    var bg4:BGSprite;
    var anim1:BGSprite;
    var anim2:BGSprite;
    var anim3:BGSprite;
    var anim4:BGSprite;
    var kyleSprite:BGSprite;
    var kyleAltSprite:BGSprite;
    var vignette:BGSprite;
    var funnyEffect:BGSprite;
    var cameraDadX:Float = -500;
    var cameraDadY:Float = 100;
    var cameraBfX:Float = 1200;
    var cameraBfY:Float = 150;
    var cameraZoomTween:FlxTween;

    function register(tag:String, sprite:BGSprite, hud:Bool = false):BGSprite
    {
        sprite.cameras = hud ? [camHUD] : [camGame];
        sprites.set(tag, sprite);
        add(sprite);
        return sprite;
    }

    function addStill(tag:String, image:String, x:Float, y:Float, hud:Bool = false):BGSprite
    {
        return register(tag, new BGSprite(image, x, y), hud);
    }

    function addAnimated(tag:String, image:String, x:Float, y:Float, scaleX:Float, scaleY:Float,
        prefix:String, fps:Int, loop:Bool, hud:Bool = false):BGSprite
    {
        var sprite = new BGSprite(image, x, y, 1, 1, [prefix], loop);
        sprite.scale.set(scaleX, scaleY);
        var anim = sprite.animation.getByName(prefix);
        if (anim != null) anim.frameRate = fps;
        return register(tag, sprite, hud);
    }

    override function create():Void
    {
        // The source stage opens on a white field, then reveals its animated layers.
        whiteBg = addStill("white", "white", -1700, -500);
        whiteBg.scale.set(3, 2.7);
        whiteBg.alpha = 1;

        bg1 = addAnimated("bg", "bg", -1670, -1140, 2.7, 2.7, "bg a", 17, true);
        bg1.alpha = 0;
        bg2 = addAnimated("bg2", "bg2", -1670, -1340, 2.7, 2.7, "bg2 a", 17, true);
        bg2.alpha = 0;
        bg3 = addAnimated("bg3", "bg3", -1270, -540, 2.8, 2.7, "bg3 a", 17, true);
        bg3.alpha = 0;
        bg4 = addAnimated("bg4", "bg4", -1270, -540, 2.8, 2.7, "bg4 a", 17, true);
        bg4.alpha = 0;

        kyleSprite = addAnimated("kyle", "kyle", 626, 189, 0.9, 0.9, "kenny anim", 25, false);
        kyleSprite.alpha = 1;
        kyleAltSprite = addAnimated("kyle s", "kyle s", 626, 190, 0.9, 0.9, "idle", 17, true);
        kyleAltSprite.alpha = 0;
        var kyleAltAnim = kyleAltSprite.animation.getByName("idle");
        if (kyleAltAnim != null) kyleAltAnim.frameRate = 17;
        kyleAltSprite.animation.addByPrefix("anim1", "anim", 24, false);

        anim1 = addAnimated("anim1", "anim1", -30, 230, 1.1, 1.1, "anim", 24, false, true);
        anim1.alpha = 0;
        anim1.animation.addByPrefix("idle anim", "idle anim", 17, true);
        anim2 = addAnimated("anim2", "anim2", 750, 270, 1.3, 1.3, "anim", 24, false, true);
        anim2.alpha = 0;
        anim3 = addAnimated("anim3", "anim3", 0, 0, 1, 1, "anim3", 24, false, true);
        anim3.alpha = 0;
        anim4 = addAnimated("anim4", "anim4", 40, 40, 0.6, 0.6, "anim4 a", 60, false, true);
        anim4.alpha = 0;

        vignette = addStill("Vignette", "Vignette", -20, 0, true);
        vignette.alpha = 0;
        funnyEffect = addStill("thefunnyeffect", "thefunnyeffect", 0, 0, true);
        funnyEffect.alpha = 0;
        blackOverlay = addStill("black", "black", 0, 0, true);
        blackOverlay.alpha = 0;
        blackBar = addStill("blackbar", "blackbar", 0, 0, true);
        blackBar.alpha = 0;
    }

    override function stepHit():Void
    {
        switch (curStep)
        {
            case 2:
                if (boyfriend != null) boyfriend.color = FlxColor.BLACK;
                if (dad != null) dad.color = FlxColor.BLACK;
                if (gf != null) gf.color = FlxColor.BLACK;
            case 5:
                if (gf != null) gf.alpha = 0;
                if (kyleSprite != null) kyleSprite.alpha = 0;
                if (kyleAltSprite != null) kyleAltSprite.alpha = 0;
            case 465:
                if (boyfriend != null) boyfriend.color = FlxColor.WHITE;
            case 472:
                if (kyleSprite != null) kyleSprite.alpha = 1;
            case 1115:
                if (anim1 != null) anim1.y = 190;
            case 1145:
                if (anim1 != null) FlxTween.tween(anim1, {x: -1000}, 1, {ease: FlxEase.expoIn});
            case 1157:
                if (anim2 != null) FlxTween.tween(anim2, {x: 2000}, 1, {ease: FlxEase.expoIn});
            case 2344:
                if (boyfriend != null) FlxTween.tween(boyfriend, {x: 1000}, 1, {ease: FlxEase.cubeOut});
        }
    }

    override function sectionHit():Void
    {
        if (camFollow == null || PlayState.SONG == null || PlayState.SONG.notes == null
            || curSection < 0 || curSection >= PlayState.SONG.notes.length) return;
        if (PlayState.SONG.notes[curSection].mustHitSection)
            camFollow.setPosition(cameraBfX, cameraBfY);
        else
            camFollow.setPosition(cameraDadX, cameraDadY);
    }

    function fadeSprite(tag:String, target:Float, duration:Float):Void
    {
        var sprite = sprites.get(tag);
        if (sprite == null) return;
        FlxTween.cancelTweensOf(sprite);
        if (duration <= 0) sprite.alpha = target;
        else FlxTween.tween(sprite, {alpha: target}, duration, {ease: FlxEase.linear});
    }

    function setSilhouette(enabled:Bool, duration:Float):Void
    {
        var target = enabled ? FlxColor.BLACK : FlxColor.WHITE;
        if (boyfriend != null) tweenCharacterColor(boyfriend, target, duration);
        if (dad != null) tweenCharacterColor(dad, target, duration);
        if (gf != null) tweenCharacterColor(gf, target, duration);
    }

    function tweenCharacterColor(character:FlxSprite, target:FlxColor, duration:Float):Void
    {
        FlxTween.cancelTweensOf(character);
        if (duration <= 0) character.color = target;
        else FlxTween.color(character, duration, character.color, target, {ease: FlxEase.linear});
    }

    override function eventCalled(eventName:String, value1:String, value2:String,
        flValue1:Null<Float>, flValue2:Null<Float>, strumTime:Float):Void
    {
        var n1 = Std.parseFloat(value1);
        var n2 = Std.parseFloat(value2);
        switch (eventName)
        {
            case "afadein":
                fadeSprite(value1, 1, Math.isNaN(n2) ? 0 : n2);
            case "afadeout":
                fadeSprite(value1, 0, Math.isNaN(n2) ? 0 : n2);
            case "badapplelol":
                var duration = Math.isNaN(n2) ? 0 : n2;
                if (value1.toLowerCase() == "a")
                {
                    fadeSprite("white", 1, duration);
                    setSilhouette(true, duration);
                }
                else if (value1.toLowerCase() == "b")
                {
                    fadeSprite("white", 0, duration);
                    setSilhouette(false, duration);
                    fadeSprite("black", 0, 0);
                }
            case "aofisetiBF" | "aofisetiBF-fest":
                if (!Math.isNaN(n1)) cameraBfX = n1;
                if (!Math.isNaN(n2)) cameraBfY = n2;
            case "aofisetiDad" | "aofisetiDad-fest":
                if (!Math.isNaN(n1)) cameraDadX = n1;
                if (!Math.isNaN(n2)) cameraDadY = n2;
            case "aCamaraZoom" | "aCamaraZoom1" | "aCamaraZoom3":
                if (!Math.isNaN(n1) && n1 > 0 && n1 <= 4)
                {
                    if (cameraZoomTween != null) cameraZoomTween.cancel();
                    if (Math.isNaN(n2) || n2 <= 0)
                    {
                        defaultCamZoom = n1;
                    }
                    else
                    {
                        cameraZoomTween = FlxTween.num(defaultCamZoom, n1, n2,
                            {ease: eventName == "aCamaraZoom1" ? FlxEase.expoOut : FlxEase.sineInOut},
                            function(value:Float) defaultCamZoom = value);
                    }
                }
            case "aFlash Camera(red)":
                var duration = Math.isNaN(n1) || n1 <= 0 ? 0.5 : n1;
                camGame.flash(FlxColor.RED, duration);
            case "Flash Camera":
                var duration = Math.isNaN(n1) || n1 <= 0 ? 0.5 : n1;
                camGame.flash(FlxColor.WHITE, duration);
            case "aCameraFlashBlack" | "aCameraFlashBlackIntro" | "FadeScreenOut":
                // Use a short camera flash, never leave a permanent black cover.
                var duration = Math.isNaN(n1) || n1 <= 0 ? 0.35 : n1;
                if (duration > 1.5) duration = 1.5;
                camGame.flash(FlxColor.BLACK, duration);
            case "aObject Play Animation":
                var sprite = sprites.get(value1);
                if (sprite != null && value2.length > 0) sprite.animation.play(value2, true);
            case "aCinematics (Still Strum)":
                fadeSprite("blackbar", value1.toLowerCase() == "off" ? 0 : 1,
                    Math.isNaN(n2) ? 0.2 : n2);
            case "BF Fade":
                if (boyfriend != null) tweenCharacterAlpha(boyfriend, n1, n2);
            case "GF Fade":
                if (gf != null) tweenCharacterAlpha(gf, n1, n2);
            case "Opponent Fade":
                if (dad != null) tweenCharacterAlpha(dad, n1, n2);
            case "aDarkness":
                fadeSprite("black", Math.isNaN(n1) ? 1 : n1, Math.isNaN(n2) ? 0 : n2);
            case "Set Property":
                var parts = value1.split(".");
                if (parts.length == 2 && parts[1] == "alpha")
                    fadeSprite(parts[0], Math.isNaN(n2) ? 0 : n2, 0);
            case "Play Animation":
                if (value1 == "1" && anim1 != null) anim1.animation.play("anim", true);
                if (value1 == "2" && anim2 != null) anim2.animation.play("anim", true);
                if (value1 == "3" && anim3 != null) anim3.animation.play("anim3", true);
                if (value1 == "4" && anim4 != null) anim4.animation.play("anim4 a", true);
        }
    }

    function tweenCharacterAlpha(character:FlxSprite, target:Float, duration:Float):Void
    {
        if (Math.isNaN(target)) target = 1;
        if (target < 0) target = 0;
        if (target > 1) target = 1;
        if (Math.isNaN(duration) || duration <= 0) character.alpha = target;
        else FlxTween.tween(character, {alpha: target}, duration, {ease: FlxEase.linear});
    }
}
'''


def safe_extract(zip_path: Path, destination: Path) -> None:
    """Extract a ZIP while rejecting paths that escape the destination."""
    destination_resolved = destination.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if target != destination_resolved and destination_resolved not in target.parents:
                raise RuntimeError(f"Unsafe path in source archive: {member.filename}")
        archive.extractall(destination)


def find_mod_root(package: Path) -> Path:
    expected_chart = Path("data") / SONG / CHART
    candidates = [package] if package.is_dir() else []
    candidates.extend(p.parent for p in package.rglob("pack.json"))
    for candidate in candidates:
        if (candidate / expected_chart).is_file() and (candidate / "stages" / "south.json").is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not locate the supplied mod folder containing {expected_chart} and stages/south.json"
    )


def copy_tree(source: Path, destination: Path, ignore=None) -> int:
    if not source.is_dir():
        return 0
    shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore)
    return sum(1 for path in destination.rglob("*") if path.is_file())


def ignore_duplicate_nested_images(directory: str, names: list[str]) -> set[str]:
    # The package repeats much of images/ inside images/characters/images/.
    if Path(directory).name == "characters" and "images" in names:
        return {"images"}
    return set()


def copy_audio_folder(source: Path, destination: Path) -> int:
    """Copy original browser-decodable MP3/OGG audio without re-encoding."""
    if not source.is_dir():
        return 0
    destination.mkdir(parents=True, exist_ok=True)
    count = 0
    for audio in sorted(source.iterdir()):
        if not audio.is_file() or audio.suffix.lower() not in {".ogg", ".mp3"}:
            continue
        shutil.copy2(audio, destination / audio.name)
        count += 1
    return count


def patch_html5_platform_features(engine: Path) -> None:
    """Remove desktop-only Discord RPC from the JavaScript target."""
    project_file = engine / "Project.xml"
    project = project_file.read_text(encoding="utf-8")
    old_define = '<define name="DISCORD_ALLOWED" />'
    new_define = '<define name="DISCORD_ALLOWED" if="desktop" />'
    if old_define in project:
        project = project.replace(old_define, new_define, 1)

    # The supplied mod stores its instrumental and sound effects as OGG.
    # Include OGG files only in the shared and songs web libraries. Keep the
    # exclusions for week_assets and optional secrets unchanged.
    audio_asset_rules = (
        (
            '<assets path="assets/shared"        exclude="*.ogg" if="web"/>',
            '<assets path="assets/shared"        if="web"/>',
        ),
        (
            '<assets path="assets/songs"         library="songs"         exclude="*.ogg" if="web"/>',
            '<assets path="assets/songs"         library="songs"         if="web"/>',
        ),
    )
    for original_rule, web_rule in audio_asset_rules:
        if original_rule in project:
            if project.count(original_rule) != 1:
                raise RuntimeError(f"Expected one asset rule: {original_rule}")
            project = project.replace(original_rule, web_rule, 1)
        elif web_rule not in project:
            raise RuntimeError(f"Could not locate an expected shared/songs web asset rule: {original_rule}")

    if project != project_file.read_text(encoding="utf-8"):
        project_file.write_text(project, encoding="utf-8")
    if new_define not in project:
        raise RuntimeError("Could not find the Discord feature define in Project.xml.")

    discord_file = engine / "source" / "backend" / "Discord.hx"
    if not discord_file.is_file():
        raise FileNotFoundError(f"Psych Engine Discord source is missing: {discord_file}")
    original = discord_file.read_text(encoding="utf-8")
    marker = "// HTML5 Discord RPC stub"
    if marker not in original:
        # Discord.hx imports hxdiscord_rpc and cpp pointer/thread APIs at file
        # scope. Merely setting DISCORD_ALLOWED off does not make those imports
        # safe on JS, so provide a no-op implementation for the html5 target.
        stub = """#if html5
package backend;

// HTML5 Discord RPC stub. The original implementation requires C++ and desktop threads.
class DiscordClient
{
    public static var isInitialized:Bool = false;
    public static var clientID:String = "863222024192262205";
    public static function check():Void {}
    public static function prepare():Void {}
    public static function shutdown():Void { isInitialized = false; }
    public static function initialize():Void {}
    public static function changePresence(?details:String = "In the Menus", ?state:Null<String>, ?smallImageKey:String, ?hasStartTimestamp:Bool, ?endTimestamp:Float):Void {}
    public static function updatePresence():Void {}
    public static function resetClientID():Void {}
    public static function loadModRPC():Void {}
    public static function addLuaCallbacks(lua:Dynamic):Void {}
}
#else
"""
        discord_file.write_text(stub + original.rstrip() + chr(10) + "#end" + chr(10), encoding="utf-8")


def patch_html5_ogg_fallback(engine: Path) -> None:
    """Resolve original OGG files when an HTML5 MP3 asset is not present."""
    paths_file = engine / "source" / "backend" / "Paths.hx"
    source = paths_file.read_text(encoding="utf-8")
    fallback_marker = "// HTML5 OGG fallback"
    if fallback_marker in source:
        return

    old = """\t\tvar gottenPath:String = '$key.$SOUND_EXT';
\t\tif(path != null) gottenPath = '$path/$gottenPath';
\t\tgottenPath = getPath(gottenPath, SOUND, library);
\t\tgottenPath = gottenPath.substring(gottenPath.indexOf(':') + 1, gottenPath.length);
\t\t// trace(gottenPath);
\t\tif(!currentTrackedSounds.exists(gottenPath))
\t\t{
\t\t\tvar retKey:String = (path != null) ? '$path/$key' : key;
\t\t\tretKey = ((path == 'songs') ? 'songs:' : '') + getPath('$retKey.$SOUND_EXT', SOUND, library);
\t\t\tif(OpenFlAssets.exists(retKey, SOUND))
\t\t\t{
\t\t\t\tcurrentTrackedSounds.set(gottenPath, OpenFlAssets.getSound(retKey));
\t\t\t\t//trace('precached vanilla sound: $retKey');
\t\t\t}
\t\t}
"""
    new = """\t\tvar assetPath:String = (path != null) ? '$path/$key' : key;
\t\tvar gottenPath:String = getPath('$assetPath.$SOUND_EXT', SOUND, library);
\t\tgottenPath = gottenPath.substring(gottenPath.indexOf(':') + 1, gottenPath.length);
\t\tvar retKey:String = ((path == 'songs') ? 'songs:' : '') + getPath('$assetPath.$SOUND_EXT', SOUND, library);
\t\t#if html5
\t\t// HTML5 OGG fallback: preserve MP3 preference but load original OGG when
\t\t// the mod does not ship a browser-specific MP3.
\t\tif(!OpenFlAssets.exists(retKey, SOUND))
\t\t{
\t\t\tvar oggPath:String = getPath('$assetPath.ogg', SOUND, library);
\t\t\tvar oggKey:String = ((path == 'songs') ? 'songs:' : '') + oggPath;
\t\t\tif(OpenFlAssets.exists(oggKey, SOUND))
\t\t\t{
\t\t\t\tgottenPath = oggPath.substring(oggPath.indexOf(':') + 1, oggPath.length);
\t\t\t\tretKey = oggKey;
\t\t\t}
\t\t}
\t\t#end
\t\tif(!currentTrackedSounds.exists(gottenPath))
\t\t{
\t\t\tif(OpenFlAssets.exists(retKey, SOUND))
\t\t\t{
\t\t\t\tcurrentTrackedSounds.set(gottenPath, OpenFlAssets.getSound(retKey));
\t\t\t\t//trace('precached vanilla sound: $retKey');
\t\t\t}
\t\t}
"""
    if source.count(old) != 1:
        raise RuntimeError("Cannot locate the unique Paths.returnSound audio asset lookup block.")
    source = source.replace(old, new, 1)
    paths_file.write_text(source, encoding="utf-8")


def patch_html5_animate_io(engine: Path) -> None:
    """Use embedded OpenFL text assets instead of desktop filesystem reads on JS."""
    paths_file = engine / "source" / "backend" / "Paths.hx"
    paths_source = paths_file.read_text(encoding="utf-8")
    paths_marker = "OpenFlAssets.getText(Std.string(spriteJson))"
    if paths_marker not in paths_source:
        sprite_old = "spriteJson = File.getContent(spriteJson);"
        animation_old = "animationJson = File.getContent(animationJson);"
        if paths_source.count(sprite_old) != 1 or paths_source.count(animation_old) != 1:
            raise RuntimeError("Cannot locate both FlxAnimate JSON reads in backend/Paths.hx.")
        paths_source = paths_source.replace(
            sprite_old,
            """#if sys
\t\t\tspriteJson = File.getContent(spriteJson);
\t\t#else
\t\t\tspriteJson = OpenFlAssets.getText(Std.string(spriteJson));
\t\t#end""",
            1,
        )
        paths_source = paths_source.replace(
            animation_old,
            """#if sys
\t\t\tanimationJson = File.getContent(animationJson);
\t\t#else
\t\t\tanimationJson = OpenFlAssets.getText(Std.string(animationJson));
\t\t#end""",
            1,
        )
        paths_file.write_text(paths_source, encoding="utf-8")

    # Patch the exact FlxAnimate dependency selected by Haxelib. The dev
    # branch already handles HTML5 for ZIP and atlas-folder reads, but its
    # loadAtlasEx JSON/XML branches still call sys.io.File unconditionally.
    haxelib_path = subprocess.run(
        ["haxelib", "path", "flxanimate"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    library_root = None
    for raw_line in haxelib_path.splitlines():
        candidate_text = raw_line.strip()
        if candidate_text.startswith("-cp "):
            candidate_text = candidate_text[4:].strip()
        if candidate_text and not candidate_text.startswith("-"):
            candidate = Path(candidate_text)
            if candidate.is_dir():
                library_root = candidate
                break
    if library_root is None:
        raise RuntimeError("Could not resolve the installed flxanimate Haxelib source path.")

    animate_file = library_root / "flxanimate" / "FlxAnimate.hx"
    if not animate_file.is_file():
        raise FileNotFoundError(f"FlxAnimate source file is missing: {animate_file}")
    animate_source = animate_file.read_text(encoding="utf-8")
    if "Assets.getText(Std.string(myJson))" not in animate_source:
        old_json = "if(trimmed == '.json') myJson = sys.io.File.getContent(myJson); //is a path"
        new_json = """if(trimmed == '.json') //is a path
\t\t\t{
\t\t\t\t#if sys
\t\t\t\tmyJson = sys.io.File.getContent(myJson);
\t\t\t\t#else
\t\t\t\tmyJson = Assets.getText(Std.string(myJson));
\t\t\t\t#end
\t\t\t}"""
        old_data = "myData = sys.io.File.getContent(pathOrStr);"
        new_data = """#if sys
\t\t\tmyData = sys.io.File.getContent(pathOrStr);
\t\t\t#else
\t\t\tmyData = Assets.getText(pathOrStr);
\t\t\t#end"""
        if animate_source.count(old_json) != 1 or animate_source.count(old_data) != 2:
            raise RuntimeError("Unexpected FlxAnimate loadAtlasEx file-I/O source; refusing an unsafe patch.")
        animate_source = animate_source.replace(old_json, new_json, 1)
        animate_source = animate_source.replace(old_data, new_data)
        animate_file.write_text(animate_source, encoding="utf-8")


    renderer_file = library_root / "flxanimate" / "display" / "FlxAnimateFilterRenderer.hx"
    if not renderer_file.is_file():
        raise FileNotFoundError(f"FlxAnimate filter renderer is missing: {renderer_file}")
    renderer_source = renderer_file.read_text(encoding="utf-8")
    import_marker = "import lime.graphics.cairo.Cairo;"
    import_line = "import lime._internal.graphics.ImageCanvasUtil;"
    if import_line not in renderer_source:
        if renderer_source.count(import_marker) != 1:
            raise RuntimeError("Cannot locate the Lime Cairo import in FlxAnimateFilterRenderer.hx.")
        renderer_source = renderer_source.replace(import_marker, import_line + "\n" + import_marker, 1)
    access_line = "@:access(lime.graphics.ImageBuffer)"
    class_marker = "class FlxAnimateFilterRenderer"
    if access_line not in renderer_source:
        if renderer_source.count(class_marker) != 1:
            raise RuntimeError("Cannot locate FlxAnimateFilterRenderer class declaration.")
        renderer_source = renderer_source.replace(class_marker, access_line + "\n" + class_marker, 1)
    renderer_file.write_text(renderer_source, encoding="utf-8")


def patch_html5_engine_source(engine: Path) -> None:
    """Guard desktop-only source operations and fix APIs used by this build."""
    editor_file = engine / "source" / "states" / "editors" / "CharacterEditorState.hx"
    editor_source = editor_file.read_text(encoding="utf-8")
    scan_line = "\t\tvar foldersToCheck:Array<String> = Mods.directoriesWithFile(Paths.getSharedPath(), 'characters/');"
    guarded_scan_line = "\t\t#if sys\n" + scan_line
    if scan_line in editor_source and guarded_scan_line not in editor_source:
        if editor_source.count(scan_line) != 1:
            raise RuntimeError("Cannot locate a unique CharacterEditorState character-folder scan.")
        editor_source = editor_source.replace(scan_line, guarded_scan_line, 1)
        end = "\t\t\t\t}\n\n\t\tif(characterList.length < 1)"
        if editor_source.count(end) != 1:
            raise RuntimeError("Cannot locate end of CharacterEditorState character-folder scan.")
        editor_source = editor_source.replace(
            end,
            "\t\t\t\t}\n\t\t#end\n\n\t\tif(characterList.length < 1)",
            1,
        )
        editor_file.write_text(editor_source, encoding="utf-8")
    elif guarded_scan_line not in editor_source:
        raise RuntimeError("CharacterEditorState folder scan is missing or was unexpectedly changed.")

    cool_file = engine / "source" / "backend" / "CoolUtil.hx"
    cool_source = cool_file.read_text(encoding="utf-8")
    if "FlxG.error(" in cool_source:
        cool_source = cool_source.replace("FlxG.error(", "FlxG.log.error(")
        cool_file.write_text(cool_source, encoding="utf-8")

    # Make the in-repo Options class explicit. This prevents global imports
    # from resolving Option to an unrelated UI class with a defaultSelected
    # boolean constructor parameter.
    for filename in ("GraphicsSettingsSubState.hx", "VisualsUISubState.hx", "GameplaySettingsSubState.hx"):
        option_file = engine / "source" / "options" / filename
        option_source = option_file.read_text(encoding="utf-8")
        option_source = option_source.replace("var option:Option =", "var option:options.Option =")
        option_source = option_source.replace("new Option(", "new options.Option(")
        option_file.write_text(option_source, encoding="utf-8")


def patch_html5_week_loading(engine: Path) -> None:
    """Register the embedded week and guarantee valid LC metadata on HTML5."""
    week_file = engine / "source" / "backend" / "WeekData.hx"
    source = week_file.read_text(encoding="utf-8")
    original = "\t\tvar sexList:Array<String> = CoolUtil.coolTextFile(Paths.getSharedPath('weeks/weekList.txt'));"
    replacement = """\t\t#if html5
\t\tvar sexList:Array<String> = ["LC"];
\t\t#else
\t\tvar sexList:Array<String> = CoolUtil.coolTextFile(Paths.getSharedPath('weeks/weekList.txt'));
\t\t#end"""
    if 'var sexList:Array<String> = ["LC"];' not in source:
        if source.count(original) != 1:
            raise RuntimeError("Cannot locate the Psych Engine week-list load statement.")
        source = source.replace(original, replacement, 1)

    # Some deployed packages have deserialized the LC week with null optional
    # fields even though the preparation step normalizes the JSON. Keep the
    # browser menu data valid at the engine boundary, and provide the one real
    # chart entry if songs is absent so Freeplay remains playable.
    constructor_marker = "\t\tthis.fileName = fileName;"
    constructor_replacement = """\t\tthis.fileName = fileName;
\t\t#if html5
\t\t// HTML5 Bloodbath LC week defaults: never leave menu arrays null.
\t\tif (fileName == "LC")
\t\t{
\t\t\tif (songs == null || songs.length == 0)
\t\t\t\tsongs = [["Bloodbath Spanish Mix", "bf", [146, 113, 253]]];
\t\t\tif (weekBefore == null) weekBefore = "";
\t\t\tif (weekCharacters == null || weekCharacters.length < 3)
\t\t\t\tweekCharacters = ["dad", "bf", "gf"];
\t\t\tif (weekName == null || weekName.length == 0) weekName = "Bloodbath Spanish Mix";
\t\t\tif (storyName == null || storyName.length == 0) storyName = "Bloodbath Spanish Mix";
\t\t\tif (freeplayColor == null || freeplayColor.length < 3) freeplayColor = [146, 113, 253];
\t\t\tif (weekBackground == null) weekBackground = "LC";
\t\t}
\t\t#end"""
    if "HTML5 Bloodbath LC week defaults" not in source:
        if source.count(constructor_marker) != 1:
            raise RuntimeError("Cannot locate the unique WeekData constructor assignment.")
        source = source.replace(constructor_marker, constructor_replacement, 1)
    week_file.write_text(source, encoding="utf-8")

def patch_html5_menu_guards(engine: Path) -> None:
    """Show actionable diagnostics instead of crashing on an empty HTML5 menu."""
    story_file = engine / "source" / "states" / "StoryMenuState.hx"
    story = story_file.read_text(encoding="utf-8")
    story_marker = "\t\tWeekData.setDirectoryFromWeek(loadedWeeks[0]);"
    story_guard = """\t\tif (loadedWeeks.length < 1)
\t\t{
\t\t\tvar message = new FlxText(0, 0, FlxG.width, "No Story Mode week was loaded. Check the embedded LC week data.", 24);
\t\t\tmessage.setFormat(Paths.font("vcr.ttf"), 24, FlxColor.WHITE, CENTER, FlxTextBorderStyle.OUTLINE, FlxColor.BLACK);
\t\t\tmessage.screenCenter();
\t\t\tadd(message);
\t\t\tsuper.create();
\t\t\treturn;
\t\t}

"""
    if "No Story Mode week was loaded." not in story:
        if story.count(story_marker) != 1:
            raise RuntimeError("Cannot locate the StoryMenuState initial week access.")
        story = story.replace(story_marker, story_guard + story_marker, 1)
        story_file.write_text(story, encoding="utf-8")

    freeplay_file = engine / "source" / "states" / "FreeplayState.hx"
    freeplay = freeplay_file.read_text(encoding="utf-8")
    week_entry = "\t\t\tvar leWeek:WeekData = WeekData.weeksLoaded.get(WeekData.weeksList[i]);"
    safe_week_entry = """\t\t\tvar leWeek:WeekData = WeekData.weeksLoaded.get(WeekData.weeksList[i]);
\t\t\tif (leWeek == null || leWeek.songs == null) continue;"""
    if "if (leWeek == null || leWeek.songs == null) continue;" not in freeplay:
        if freeplay.count(week_entry) != 1:
            raise RuntimeError("Cannot locate FreeplayState's week metadata lookup.")
        freeplay = freeplay.replace(week_entry, safe_week_entry, 1)
    freeplay_marker = "\t\tMods.loadTopMod();"
    freeplay_guard = """\t\tif (songs.length < 1)
\t\t{
\t\t\tvar message = new FlxText(0, 0, FlxG.width, "No Freeplay songs were loaded from the embedded LC week.", 24);
\t\t\tmessage.setFormat(Paths.font("vcr.ttf"), 24, FlxColor.WHITE, CENTER, FlxTextBorderStyle.OUTLINE, FlxColor.BLACK);
\t\t\tmessage.screenCenter();
\t\t\tadd(message);
\t\t\tsuper.create();
\t\t\treturn;
\t\t}

"""
    if "No Freeplay songs were loaded" not in freeplay:
        if freeplay.count(freeplay_marker) != 1:
            raise RuntimeError("Cannot locate the FreeplayState song-list completion point.")
        freeplay = freeplay.replace(freeplay_marker, freeplay_guard + freeplay_marker, 1)
        freeplay_file.write_text(freeplay, encoding="utf-8")


    # The upstream menu implementations assume weekBefore is always a string.
    # Some mod week files deserialize an omitted/null value as null, which makes
    # weekBefore.length throw in HTML5. Treat a null/empty prerequisite as no
    # prerequisite, and skip an unexpectedly missing week instead of crashing.
    lock_patches = (
        (
            "StoryMenuState.hx",
            """\tfunction weekIsLocked(name:String):Bool {
\t\tvar leWeek:WeekData = WeekData.weeksLoaded.get(name);
\t\treturn (!leWeek.startUnlocked && leWeek.weekBefore.length > 0 && (!weekCompleted.exists(leWeek.weekBefore) || !weekCompleted.get(leWeek.weekBefore)));
\t}""",
            """\tfunction weekIsLocked(name:String):Bool {
\t\tvar leWeek:WeekData = WeekData.weeksLoaded.get(name);
\t\tif (leWeek == null) return true;
\t\tvar weekBefore:String = leWeek.weekBefore;
\t\tif (leWeek.startUnlocked || weekBefore == null || weekBefore.length == 0) return false;
\t\treturn (!weekCompleted.exists(weekBefore) || !weekCompleted.get(weekBefore));
\t}""",
        ),
        (
            "FreeplayState.hx",
            """\tfunction weekIsLocked(name:String):Bool {
\t\tvar leWeek:WeekData = WeekData.weeksLoaded.get(name);
\t\treturn (!leWeek.startUnlocked && leWeek.weekBefore.length > 0 && (!StoryMenuState.weekCompleted.exists(leWeek.weekBefore) || !StoryMenuState.weekCompleted.get(leWeek.weekBefore)));
\t}""",
            """\tfunction weekIsLocked(name:String):Bool {
\t\tvar leWeek:WeekData = WeekData.weeksLoaded.get(name);
\t\tif (leWeek == null) return true;
\t\tvar weekBefore:String = leWeek.weekBefore;
\t\tif (leWeek.startUnlocked || weekBefore == null || weekBefore.length == 0) return false;
\t\treturn (!StoryMenuState.weekCompleted.exists(weekBefore) || !StoryMenuState.weekCompleted.get(weekBefore));
\t}""",
        ),
    )
    for filename, original_lock, safe_lock in lock_patches:
        menu_file = engine / "source" / "states" / filename
        menu_source = menu_file.read_text(encoding="utf-8")
        if "weekBefore == null || weekBefore.length == 0" in menu_source:
            continue
        if menu_source.count(original_lock) != 1:
            raise RuntimeError(f"Cannot locate the unique weekIsLocked() implementation in {filename}.")
        menu_source = menu_source.replace(original_lock, safe_lock, 1)
        menu_file.write_text(menu_source, encoding="utf-8")



def patch_html5_menu_artwork(engine: Path) -> None:
    """Use the four custom repository artworks across the browser menus."""
    main_file = engine / "source" / "states" / "MainMenuState.hx"
    main = main_file.read_text(encoding="utf-8")

    replacements = (
        (
            "magenta = new FlxSprite(-80).loadGraphic(Paths.image('menuDesat'));",
            "magenta = new FlxSprite(-80).loadGraphic(Paths.image('menuMagenta'));",
        ),
        ("magenta.color = 0xFFfd719b;", "magenta.color = 0xFFFFFFFF;"),
        (
            "bg.setGraphicSize(Std.int(bg.width * 1.175));",
            "bg.setGraphicSize(Std.int(bg.width * Math.max(FlxG.width / bg.width, FlxG.height / bg.height)));",
        ),
        (
            "magenta.setGraphicSize(Std.int(magenta.width * 1.175));",
            "magenta.setGraphicSize(Std.int(magenta.width * Math.max(FlxG.width / magenta.width, FlxG.height / magenta.height)));",
        ),
    )
    for original, updated in replacements:
        if updated not in main:
            if main.count(original) != 1:
                raise RuntimeError(f"Cannot uniquely locate MainMenuState artwork line: {original}")
            main = main.replace(original, updated, 1)
    main_file.write_text(main, encoding="utf-8")

    freeplay_file = engine / "source" / "states" / "FreeplayState.hx"
    freeplay = freeplay_file.read_text(encoding="utf-8")
    freeplay_old = """\t\tbg = new FlxSprite().loadGraphic(Paths.image('menuDesat'));
\t\tbg.antialiasing = ClientPrefs.data.antialiasing;
\t\tadd(bg);
\t\tbg.screenCenter();"""
    freeplay_new = """\t\tbg = new FlxSprite().loadGraphic(Paths.image('menuDesat'));
\t\tbg.antialiasing = ClientPrefs.data.antialiasing;
\t\tvar bgScale:Float = Math.max(FlxG.width / bg.width, FlxG.height / bg.height);
\t\tbg.setGraphicSize(Std.int(bg.width * bgScale));
\t\tbg.updateHitbox();
\t\tadd(bg);
\t\tbg.screenCenter();"""
    if freeplay_new not in freeplay:
        if freeplay.count(freeplay_old) != 1:
            raise RuntimeError("Cannot locate FreeplayState's custom background setup.")
        freeplay = freeplay.replace(freeplay_old, freeplay_new, 1)
    freeplay_file.write_text(freeplay, encoding="utf-8")

    story_file = engine / "source" / "states" / "StoryMenuState.hx"
    story = story_file.read_text(encoding="utf-8")
    story_old = """\t\t} else {
\t\t\tbgSprite.loadGraphic(Paths.image('menubackgrounds/menu_' + assetName));
\t\t}"""
    story_new = """\t\t} else {
\t\t\tbgSprite.loadGraphic(Paths.image('menubackgrounds/menu_' + assetName));
\t\t\tvar bgScale:Float = Math.max(FlxG.width / bgSprite.width, FlxG.height / bgSprite.height);
\t\t\tbgSprite.setGraphicSize(Std.int(bgSprite.width * bgScale));
\t\t\tbgSprite.updateHitbox();
\t\t\tbgSprite.screenCenter(X);
			bgSprite.y = 56;
\t\t}"""
    if story_new not in story:
        if story.count(story_old) != 1:
            raise RuntimeError("Cannot locate StoryMenuState's week-background setup.")
        story = story.replace(story_old, story_new, 1)
    story_file.write_text(story, encoding="utf-8")


def patch_note_types(engine: Path) -> None:
    note_file = engine / "source" / "objects" / "Note.hx"
    source = note_file.read_text(encoding="utf-8")
    marker = "\t\t\t\tcase 'GF Sing':\n\t\t\t\t\tgfNote = true;"
    addition = (
        "\t\t\t\tcase 'kyle':\n"
        "\t\t\t\t\t// The source mod marks Kyle notes as non-animating notes.\n"
        "\t\t\t\t\tnoAnimation = true;\n"
        + marker
    )
    if "// The source mod marks Kyle notes" not in source:
        if source.count(marker) != 1:
            raise RuntimeError("Cannot locate the Psych Engine 0.7.3 GF Sing note-type switch.")
        source = source.replace(marker, addition, 1)
        note_file.write_text(source, encoding="utf-8")


def patch_stage_registration(engine: Path) -> None:
    play_file = engine / "source" / "states" / "PlayState.hx"
    source = play_file.read_text(encoding="utf-8")
    marker = "\t\t\tcase 'stage': new states.stages.StageWeek1(); //Week 1"
    insertion = "\t\t\tcase 'south': new states.stages.South(); // Bloodbath Spanish Mix HTML5 stage\n" + marker
    if "case 'south': new states.stages.South();" not in source:
        if source.count(marker) != 1:
            raise RuntimeError("Cannot locate the Psych Engine 0.7.3 stage registration switch.")
        source = source.replace(marker, insertion, 1)
        play_file.write_text(source, encoding="utf-8")


def prepare(engine: Path, mod: Path) -> dict[str, object]:
    shared = engine / "assets" / "shared"
    shared.mkdir(parents=True, exist_ok=True)

    # Embed mod resources into asset folders already included by Project.xml.
    copy_tree(mod / "images", shared / "images", ignore_duplicate_nested_images)

    # The custom artwork is committed at the repository root. Copy it after the
    # mod package so these four user-supplied menu images are the active versions.
    custom_art = {
        "menu.png": shared / "images" / "menuBG.png",
        "menublue.png": shared / "images" / "menubackgrounds" / "menu_LC.png",
        "menudesat.png": shared / "images" / "menuDesat.png",
        "menumagenta.png": shared / "images" / "menuMagenta.png",
    }
    for source_name, destination in custom_art.items():
        source_image = engine.parent / source_name
        if not source_image.is_file():
            raise FileNotFoundError(f"Missing custom menu artwork in repository root: {source_image}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, destination)
    copy_tree(mod / "characters", shared / "characters")
    copy_tree(mod / "data" / SONG, shared / "data" / SONG)

    stages_destination = shared / "stages"
    stages_destination.mkdir(parents=True, exist_ok=True)
    for path in (mod / "stages").glob("*.json"):
        shutil.copy2(path, stages_destination / path.name)

    weeks_destination = shared / "weeks"
    weeks_destination.mkdir(parents=True, exist_ok=True)
    week_source = mod / "weeks" / f"{WEEK}.json"
    if not week_source.is_file():
        raise FileNotFoundError(f"Missing week file: {week_source}")

    # This browser build embeds one playable chart, whose only chart file is
    # bloodbath-spanish-mix-hard.json. Make the week visible/unlocked in both
    # menus and make Hard the sole offered difficulty so both menu paths resolve
    # the exact chart that is actually embedded.
    week_data = json.loads(week_source.read_text(encoding="utf-8"))
    if not isinstance(week_data, dict):
        raise RuntimeError("The LC week metadata must be a JSON object.")

    display_song = " ".join(part.capitalize() for part in SONG.split("-"))
    source_songs = week_data.get("songs")
    source_song = source_songs[0] if isinstance(source_songs, list) and source_songs else []
    song_character = source_song[1] if isinstance(source_song, list) and len(source_song) > 1 and isinstance(source_song[1], str) and source_song[1] else "bf"
    song_color = source_song[2] if isinstance(source_song, list) and len(source_song) > 2 else week_data.get("freeplayColor")
    if not isinstance(song_color, list) or len(song_color) < 3 or not all(isinstance(value, int) for value in song_color[:3]):
        song_color = [146, 113, 253]

    week_data["songs"] = [[display_song, song_character, song_color[:3]]]
    characters = week_data.get("weekCharacters")
    if not isinstance(characters, list) or len(characters) != 3 or not all(isinstance(value, str) and value for value in characters):
        week_data["weekCharacters"] = ["dad", "bf", "gf"]
    # StoryMenuState resolves this value as menubackgrounds/menu_<name>.png.
    # The supplied archive contains menu_LC.png (case-sensitive on Pages).
    background_candidates = ("LC", "lc", "")
    background_name = ""
    for candidate in background_candidates:
        if not candidate:
            continue
        if (shared / "images" / "menubackgrounds" / f"menu_{candidate}.png").is_file():
            background_name = candidate
            break
    week_data["weekBackground"] = background_name

    # MenuItem loads storymenu/<week-file-name>.png. There is no LC.png in
    # the supplied package or stock engine assets, so add a real bundled
    # fallback card to prevent the Story Menu from requesting a missing image.
    storymenu_dir = shared / "images" / "storymenu"
    storymenu_dir.mkdir(parents=True, exist_ok=True)
    storymenu_card = storymenu_dir / f"{WEEK}.png"
    if not storymenu_card.is_file():
        fallback_card = storymenu_dir / "week1.png"
        if not fallback_card.is_file():
            fallback_card = storymenu_dir / "tutorial.png"
        if not fallback_card.is_file():
            raise FileNotFoundError("No stock story menu card is available for the LC week.")
        shutil.copy2(fallback_card, storymenu_card)
    week_data["storyName"] = week_data.get("storyName") if isinstance(week_data.get("storyName"), str) and week_data.get("storyName") else display_song
    week_data["weekName"] = week_data.get("weekName") if isinstance(week_data.get("weekName"), str) and week_data.get("weekName") else display_song
    week_data["weekBefore"] = ""
    week_data["startUnlocked"] = True
    week_data["hiddenUntilUnlocked"] = False
    week_data["hideStoryMode"] = False
    week_data["hideFreeplay"] = False
    week_data["difficulties"] = "Hard"
    normalized_week = weeks_destination / week_source.name
    normalized_week.write_text(json.dumps(week_data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (weeks_destination / "weekList.txt").write_text(WEEK + "\n", encoding="utf-8")

    if (mod / "fonts").is_dir():
        copy_tree(mod / "fonts", engine / "assets" / "fonts")

    sound_count = copy_audio_folder(mod / "sounds", shared / "sounds")
    song_destination = engine / "assets" / "songs" / SONG
    song_count = copy_audio_folder(mod / "songs" / SONG, song_destination)
    if not any(p.stem.lower() == "inst" and p.suffix.lower() in {".ogg", ".mp3"}
               for p in song_destination.iterdir()):
        raise FileNotFoundError("The browser song library is missing Inst.ogg/Inst.mp3.")

    chart_file = shared / "data" / SONG / CHART
    if not chart_file.is_file():
        raise FileNotFoundError(f"Chart was not copied: {chart_file}")
    chart_data = json.loads(chart_file.read_text(encoding="utf-8"))
    song_data = chart_data.get("song", chart_data)
    if not isinstance(song_data, dict):
        raise RuntimeError("Unexpected chart JSON format: the song object is missing.")
    # The archive contains Inst.ogg but no Voices.ogg.
    song_data["needsVoices"] = False
    song_data["stage"] = "south"
    chart_file.write_text(json.dumps(chart_data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    patch_html5_platform_features(engine)
    patch_html5_ogg_fallback(engine)
    patch_html5_animate_io(engine)
    patch_html5_engine_source(engine)
    patch_html5_week_loading(engine)
    patch_html5_menu_guards(engine)
    patch_html5_menu_artwork(engine)
    patch_note_types(engine)
    patch_stage_registration(engine)
    stage_file = engine / "source" / "states" / "stages" / "South.hx"
    stage_file.write_text(SOUTH_HX, encoding="utf-8")

    event_counts: Counter[str] = Counter()
    note_counts: Counter[str] = Counter()
    for event_group in song_data.get("events", []):
        if not isinstance(event_group, list) or len(event_group) < 2 or not isinstance(event_group[1], list):
            continue
        for event in event_group[1]:
            if isinstance(event, list) and event:
                event_counts[str(event[0])] += 1
    for section in song_data.get("notes", []):
        if not isinstance(section, dict):
            continue
        for note in section.get("sectionNotes", []):
            if isinstance(note, list) and len(note) > 3 and note[3]:
                note_counts[str(note[3])] += 1

    return {
        "modFolder": mod.name,
        "song": SONG,
        "week": WEEK,
        "chart": CHART,
        "menuModes": {"storyMode": True, "freeplay": True},
        "weekVisible": {"storyMode": not week_data["hideStoryMode"], "freeplay": not week_data["hideFreeplay"]},
        "availableDifficulties": ["Hard"],
        "storyMenuCard": f"images/storymenu/{WEEK}.png",
        "storyMenuBackground": week_data["weekBackground"],
        "customMenuArtwork": ["menu.png", "menublue.png", "menudesat.png", "menumagenta.png"],
        "songSections": len(song_data.get("notes", [])),
        "noteCount": sum(len(section.get("sectionNotes", [])) for section in song_data.get("notes", []) if isinstance(section, dict)),
        "events": dict(event_counts),
        "noteTypes": dict(note_counts),
        "embeddedSongAudioFiles": song_count,
        "embeddedSoundFiles": sound_count,
        "noteTypePort": ["kyle", "GF Sing (native Psych Engine)"],
        "stagePort": "south (initial Haxe recreation; non-core Lua effects remain unported)",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path, help="Original ZIP or extracted mod folder")
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    engine = args.engine.resolve()
    package = args.package.resolve()
    if not (engine / "Project.xml").is_file():
        raise FileNotFoundError(f"Psych Engine source not found: {engine}")
    if not package.exists():
        raise FileNotFoundError(f"Mod package not found: {package}")
    if package.suffix.lower() == ".zip":
        with tempfile.TemporaryDirectory(prefix="bloodbath-spanish-") as temp:
            extraction = Path(temp)
            safe_extract(package, extraction)
            mod = find_mod_root(extraction)
            report = prepare(engine, mod)
    else:
        mod = find_mod_root(package)
        report = prepare(engine, mod)

    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    print("NOTE: This is an initial HTML5 port, not full Lua/event parity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
