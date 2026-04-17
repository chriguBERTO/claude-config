---
name: export-to-note
description: >
  Opens any markdown content directly in note.directory (a minimal local-first browser editor).
  Use this skill whenever the user types /export-to-note, or says "export to note.directory",
  "send to note", "open in note.directory", "open this plan in note", or "export this to note".
  Also use it proactively when a plan, summary, or long markdown output has just been produced
  and the user says something like "open that" or "send it over".
  Accepts an optional file path argument; without one, auto-detects the most recently modified
  plan file in .claude/plans/.
---

## What this skill does

Compresses a markdown file and opens it directly in [note.directory](https://note.directory) by
encoding the content into the URL hash — no account, no upload, content stays local.

## Step-by-step

### 1. Resolve the content

**If the user provided a file path** (e.g. `/export-to-note path/to/file.md` or `@ref`): read that file.

**If no argument given**: find the most recently modified `.md` file under `.claude/plans/`:
```bash
ls -t .claude/plans/*.md 2>/dev/null | head -1
```
If `.claude/plans/` is empty or doesn't exist, tell the user no plan file was found and ask them
to pass a file path explicitly.

### 2. Determine the note name

Extract the first H1 heading from the content:
```bash
grep -m1 '^# ' <file> | sed 's/^# //'
```
Fall back to the filename without its extension if no H1 is found.

### 3. Compress the content

Use the helper script — it produces output identical to the browser's `CompressionStream("deflate-raw")`:
```bash
python3 /home/user/.claude/skills/export-to-note/scripts/compress.py < <file>
```
Capture the output as `COMPRESSED`.

### 4. Build the URL

```bash
NAME_ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "<note-name>")
TS=$(python3 -c "import time; print(int(time.time()*1000))")
URL="https://note.directory/#note=${COMPRESSED}&name=${NAME_ENCODED}&ts=${TS}"
```

### 5. Check the URL length

note.directory silently drops the note content when the URL exceeds **60,000 characters**.

- **Within limit**: open in browser (see step 6), then report success.
- **Over limit**: show a clear warning, print the URL anyway so the user can decide what to do.

### 6. Open in browser

Detect the platform and open:
```bash
python3 -c "
import platform, subprocess, sys
url = sys.argv[1]
os = platform.system()
if os == 'Darwin':
    subprocess.run(['open', url])
elif os == 'Windows':
    subprocess.run(['start', url], shell=True)
else:
    subprocess.run(['xdg-open', url])
" "$URL"
```

### 7. Report to the user

Confirm what was exported — the source file, the note name, and (if within limit) that the
browser was opened. Keep it brief.

## Edge cases

- **Python not available**: tell the user and suggest installing Python 3.
- **File not found**: clear error with the path you tried.
- **URL over limit**: warn, print the URL, suggest the user download the file and drag it onto
  note.directory (it supports file drop import).