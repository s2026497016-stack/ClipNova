"""Safely apply ClipNova game-title recognition to an existing checkout."""
from __future__ import annotations
import argparse
import datetime as dt
import shutil
from pathlib import Path

HELPER = r'''
# Game names are detected from the source title only. This is context, never proof
# that a particular event happened on screen.
_GAME_CATALOG = (
    ("Grand Theft Auto VI", ("gta vi", "gta 6"), "GTAVI"),
    ("Grand Theft Auto V", ("gta v", "gta 5"), "GTAV"),
    ("Fortnite", ("fortnite",), "Fortnite"),
    ("Minecraft", ("minecraft",), "Minecraft"),
    ("Valorant", ("valorant",), "Valorant"),
    ("Elden Ring", ("elden ring",), "EldenRing"),
    ("Call of Duty: Warzone", ("call of duty warzone", "cod warzone", "warzone"), "CODWarzone"),
    ("Apex Legends", ("apex legends",), "ApexLegends"),
    ("Counter-Strike 2", ("counter-strike 2", "counter strike 2", "cs2"), "CounterStrike2"),
    ("PUBG: Battlegrounds", ("pubg battlegrounds", "pubg"), "PUBG"),
    ("League of Legends", ("league of legends",), "LeagueOfLegends"),
    ("Dota 2", ("dota 2",), "Dota2"),
    ("Overwatch 2", ("overwatch 2",), "Overwatch2"),
    ("Rocket League", ("rocket league",), "RocketLeague"),
    ("Rainbow Six Siege", ("rainbow six siege", "r6 siege"), "RainbowSixSiege"),
    ("Red Dead Redemption 2", ("red dead redemption 2", "rdr2"), "RDR2"),
    ("Cyberpunk 2077", ("cyberpunk 2077",), "Cyberpunk2077"),
    ("The Last of Us", ("the last of us",), "TheLastOfUs"),
    ("God of War", ("god of war",), "GodOfWar"),
    ("Resident Evil 4", ("resident evil 4", "re4"), "ResidentEvil4"),
    ("Roblox", ("roblox",), "Roblox"),
    ("Among Us", ("among us",), "AmongUs"),
    ("Call of Duty", ("call of duty", "cod"), "CallOfDuty"),
)


def _game_context(title):
    """Return a cautious game hint when the source title clearly names a known game."""
    source = _safe(title, 240).lower()
    for game, aliases, hashtag in _GAME_CATALOG:
        for alias in aliases:
            pattern = r"(?<![a-z0-9])" + re.escape(alias).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
            if re.search(pattern, source, re.IGNORECASE):
                return (
                    f"\nLikely game context from the video title: {game}. "
                    f"Suggested game hashtag: {hashtag}. "
                    "This is title metadata only, not proof of an event. Use it as a hint, "
                    "not a filter; only describe gameplay events supported by the transcript "
                    "or supplied reaction signals. Never invent visual details.\n"
                )
    return ""
'''

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Safety stop: expected one {label} anchor, found {count}. No files were changed.")
    return text.replace(old, new, 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Path to the existing ClipNova checkout")
    root = Path(parser.parse_args().root).expanduser().resolve()
    brain_path = root / "studio" / "brain.py"
    test_path = root / "tests" / "test_ai.py"
    if not brain_path.is_file() or not test_path.is_file():
        raise SystemExit(f"Safety stop: expected ClipNova files were not found under {root}")

    brain = brain_path.read_text(encoding="utf-8-sig")
    tests = test_path.read_text(encoding="utf-8-sig")
    if "_game_context(title)" in brain and 'check("game title detects GTA VI"' in tests:
        print("Game-title recognition is already installed. No files changed.")
        return 0

    safe_anchor = '''def _safe(v, limit=200):
    """Text from the video (title, channel, speech) on its way into a prompt: one line, and unable to close our tags."""
    return _CTRL.sub(" ", str(v or "")).replace("<", "‹").strip()[:limit]
'''
    has_helper = "def _game_context(title):" in brain
    replacements = [
        ('''prompt = (HEAD.format(title=_safe(title) or "unknown", uploader=_safe(uploader) or "unknown", n=per_window)
                  + title_context''',
         '''prompt = (HEAD.format(title=_safe(title) or "unknown", uploader=_safe(uploader) or "unknown", n=per_window)
                  + _game_context(title)
                  + title_context''', "normal prompt"),
        ('''prompt = (HEAD.format(title=_safe(title) or "unknown", uploader=_safe(uploader) or "unknown", n=2)
              + LIVE_NOTE.format(now=now) + title_context''',
         '''prompt = (HEAD.format(title=_safe(title) or "unknown", uploader=_safe(uploader) or "unknown", n=2)
              + _game_context(title)
              + LIVE_NOTE.format(now=now) + title_context''', "live prompt"),
        (r'''              f"Channel: {uploader or 'unknown'}\n\nReturn exactly one item describing it. Set start and end to 0."''',
         r'''              + _game_context(title)
              + f"Channel: {uploader or 'unknown'}\n\nReturn exactly one item describing it. Set start and end to 0."''', "manual prompt"),
    ]
    if not has_helper:
        brain = replace_once(brain, safe_anchor, safe_anchor + HELPER, "safe helper")
        for old, new, label in replacements:
            brain = replace_once(brain, old, new, label)
    elif brain.count("_game_context(title)") != 4:
        raise SystemExit("Safety stop: partial game-context integration detected. No files changed.")

    test_anchor = '''          and "never infer a specific on-screen event" in brain.TRANSCRIPT_JUDGE.lower())'''
    test_add = '''
    check("game title detects GTA VI", "Grand Theft Auto VI" in brain._game_context("GTA 6 live stream")
          and "GTAVI" in brain._game_context("GTA 6 live stream"))
    check("game title detects a known title with word boundaries", "Fortnite" in brain._game_context("Fortnite ranked gameplay"))
    check("game detection does not match inside unrelated words", brain._game_context("A great total live stream") == "")
    check("unknown video titles keep general-video behavior", brain._game_context("Just chatting with viewers") == "")
    check("game context explicitly remains a hint, not proof",
          "not proof" in brain._game_context("Minecraft survival stream").lower())
'''
    if 'check("game title detects GTA VI"' not in tests:
        tests = replace_once(tests, test_anchor, test_anchor + test_add, "AI test insertion")

    compile(brain, str(brain_path), "exec")
    compile(tests, str(test_path), "exec")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = root.parent / "ClipNova-Safety-Backups" / f"ClipNova-Game-Recognition-{stamp}"
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(brain_path, backup / "brain.py")
    shutil.copy2(test_path, backup / "test_ai.py")
    brain_path.write_text(brain, encoding="utf-8")
    test_path.write_text(tests, encoding="utf-8")
    print("Installed game-title recognition into studio/brain.py and tests/test_ai.py")
    print(f"Backups saved to: {backup}")
    print("Run your existing AI test command before starting ClipNova.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
