#!/usr/bin/env python3
"""Prepare Bloodbath Spanish Mix for an embedded Psych Engine 0.7.3 HTML5 build.

Psych Engine's desktop mod filesystem is not available on HTML5. This script
copies the mod's data into the normal shared/songs asset libraries, converts
OGG audio to MP3 for the web asset manifest, and adds a native Haxe stage
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
            camFollow.set(cameraBfX, cameraBfY);
        else
            camFollow.set(cameraDadX, cameraDadY);
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


def convert_audio(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    target = destination.with_suffix(".mp3")
    if source.suffix.lower() == ".mp3":
        shutil.copy2(source, target)
        return
    if source.suffix.lower() != ".ogg":
        raise RuntimeError(f"Unsupported audio format for HTML5: {source}")
    subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(source), "-vn", "-codec:a", "libmp3lame", "-q:a", "2",
         str(target)],
        check=True,
    )


def copy_audio_folder(source: Path, destination: Path) -> int:
    if not source.is_dir():
        return 0
    count = 0
    for audio in sorted(source.iterdir()):
        if not audio.is_file() or audio.suffix.lower() not in {".ogg", ".mp3"}:
            continue
        convert_audio(audio, destination / audio.name)
        count += 1
    return count


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
    shutil.copy2(week_source, weeks_destination / week_source.name)
    (weeks_destination / "weekList.txt").write_text(WEEK + "\n", encoding="utf-8")

    if (mod / "fonts").is_dir():
        copy_tree(mod / "fonts", engine / "assets" / "fonts")

    sound_count = copy_audio_folder(mod / "sounds", shared / "sounds")
    song_destination = engine / "assets" / "songs" / SONG
    song_count = copy_audio_folder(mod / "songs" / SONG, song_destination)
    if not any(p.stem.lower() == "inst" for p in song_destination.glob("*.mp3")):
        raise FileNotFoundError("The browser song library is missing Inst.mp3 after conversion.")

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
        "songSections": len(song_data.get("notes", [])),
        "noteCount": sum(len(section.get("sectionNotes", [])) for section in song_data.get("notes", []) if isinstance(section, dict)),
        "events": dict(event_counts),
        "noteTypes": dict(note_counts),
        "convertedSongAudioFiles": song_count,
        "convertedSoundFiles": sound_count,
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
