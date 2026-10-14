#!/usr/bin/env python3
"""SessionStart hook: tell Claude which Myelinate reviews are due.

Reads ~/.myelinate/learner.json (or $MYELINATE_HOME/learner.json), which exists
only if the learner asked Myelinate to keep a record. Prints nothing when there
is no record or nothing is due, so sessions that aren't about learning see no
change. Never fails the session: any error prints nothing.
"""
import datetime
import json
import os
import sys
from pathlib import Path

MAX_LISTED = 5
FORMAT = Path(__file__).resolve().parents[1] / 'skills' / 'tutor' / 'references' / 'learner-record.md'


def due_topics(record, today):
    due = []
    for entry in record.get('topics', []):
        try:
            when = datetime.date.fromisoformat(str(entry.get('next_review', '')))
        except ValueError:
            continue
        if when <= today:
            due.append((when, entry))
    due.sort(key=lambda item: item[0])
    return [entry for _, entry in due]


def message(record, today, path):
    due = due_topics(record, today)
    if not due:
        return ''
    names = []
    for entry in due[:MAX_LISTED]:
        name = str(entry.get('topic', 'untitled'))
        if entry.get('course'):
            name += f" ({entry['course']})"
        names.append(name)
    more = f' and {len(due) - MAX_LISTED} more' if len(due) > MAX_LISTED else ''
    return (f"Myelinate: {len(due)} review(s) due for this learner: {'; '.join(names)}{more}. "
            f"If this session turns to learning, fold 2-3 retrieval items on these in after the learner's own "
            f"question, and update their entries at the close (record: {path}; format: {FORMAT}). "
            f"Don't mention the record if the session is about something else.")


def main():
    home = Path(os.environ.get('MYELINATE_HOME') or Path.home() / '.myelinate')
    path = home / 'learner.json'
    today = datetime.date.fromisoformat(os.environ['MYELINATE_TODAY']) if os.environ.get('MYELINATE_TODAY') else datetime.date.today()
    try:
        record = json.loads(path.read_text())
    except (OSError, ValueError):
        return 0
    text = message(record, today, path)
    if text:
        print(text)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:  # a broken record must never block a session
        sys.exit(0)
