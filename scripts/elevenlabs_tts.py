#!/usr/bin/env python3
"""Turn the ElevenLabs script for an edition into the MP3 bulletin.

  elevenlabs_tts.py briefs/2026-10-29/script.txt --out "briefs/2026-10-29/Inception42 Daily News 29 Oct.mp3"
      [--voice Allistair] [--model eleven_multilingual_v2] [--format mp3_44100_128] [--break 1.0]

Reads ELEVENLABS_API_KEY from the environment. Looks the voice up by name
(case-insensitive) in the account's voice list, inserts <break time="Ns" />
between paragraphs (the API's pause tag, replacing the manual /break step in
Studio), and writes the MP3. Standard library only.

Exit codes: 0 written, 78 not configured (no API key), 1 failure.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.elevenlabs.io/v1"


def req(path, key, data=None, headers=None, raw=False):
    h = {"xi-api-key": key, "Accept": "audio/mpeg" if raw else "application/json"}
    if data is not None:
        h["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    r = urllib.request.Request(API + path, data=data, headers={**h, **(headers or {})})
    with urllib.request.urlopen(r, timeout=180) as resp:
        body = resp.read()
        return body if raw else json.loads(body)


def find_voice(key, name):
    voices = req("/voices", key).get("voices", [])
    for v in voices:
        if v.get("name", "").strip().lower() == name.strip().lower():
            return v["voice_id"], v["name"]
    for v in voices:
        if name.strip().lower() in v.get("name", "").lower():
            return v["voice_id"], v["name"]
    names = ", ".join(v.get("name", "?") for v in voices)
    raise SystemExit(f"voice '{name}' not found in this account; available: {names}")


def prepare_text(script, pause):
    paras = [p.strip() for p in re.split(r"\n\s*\n", script.strip()) if p.strip()]
    if any("—" in p for p in paras):
        print("WARNING: em dash in the script; the house rule bans them", file=sys.stderr)
    brk = f' <break time="{pause:.1f}s" /> '
    return brk.join(paras), len(paras)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--out", required=True)
    ap.add_argument("--voice", default="Allistair")
    ap.add_argument("--model", default="eleven_multilingual_v2")
    ap.add_argument("--format", default="mp3_44100_128")
    ap.add_argument("--break", dest="pause", type=float, default=1.0)
    a = ap.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        print("ELEVENLABS_API_KEY not set; audio step skipped", file=sys.stderr)
        sys.exit(78)
    script = open(a.script, encoding="utf-8").read()
    text, n = prepare_text(script, a.pause)
    words = len(re.findall(r"\w+", script))
    try:
        voice_id, voice_name = find_voice(key, a.voice)
        audio = req(f"/text-to-speech/{voice_id}?output_format={a.format}", key,
                    data={"text": text, "model_id": a.model,
                          "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True}},
                    raw=True)
    except urllib.error.HTTPError as e:
        print(f"ElevenLabs API error {e.code}: {e.read()[:500].decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        print(f"ElevenLabs failure: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "wb").write(audio)
    print(f"wrote {a.out}: {len(audio)} bytes, voice {voice_name}, {n} paragraphs, {words} words")


if __name__ == "__main__":
    main()
