#!/bin/bash
# Does Claude Code actually call the Skill tool for a Myelinate skill?
# evals/triggers asks a model which skill it would pick from the listing; this runs
# real headless sessions with the plugin loaded and records the Skill calls.
# Usage: evals/invocation/run.sh [plugin-dir] [model] [passes]
# Prompts: evals/invocation/prompts.txt, one "id|prompt" per line; ids starting with
# P should load a Myelinate skill, ids starting with N should load none.
# Each session uses your Claude Code sign-in and your user settings, hooks and skills,
# so results reflect your real setup, not an isolated one (isolating would mean copying
# credentials). A synced copy named myelinate@synced is disabled so only the plugin under
# test loads; score.py counts only namespaced myelinate:<name> calls and lists any call to a
# standalone skill named myelinate separately.
here=$(cd "$(dirname "$0")" && pwd)
plugin=$(cd "${1:-$here/../..}" && pwd); model=${2:-sonnet}; passes=${3:-1}
out=$(mktemp -d); work=$(mktemp -d)
for pass in $(seq "$passes"); do
  while IFS='|' read -r id prompt; do
    [ -z "$id" ] && continue
    ( cd "$work" && timeout 300 claude -p "$prompt" --model "$model" --max-turns 3 \
        --output-format stream-json --verbose --plugin-dir "$plugin" \
        --settings '{"enabledPlugins":{"myelinate@synced":false}}' \
        < /dev/null > "$out/$id.$pass.jsonl" 2> "$out/$id.$pass.err" ) &
  done < "$here/prompts.txt"
  wait
done
python3 "$here/score.py" "$out"; status=$?
echo "model=$model passes=$passes plugin=$plugin"
if [ $status -ne 0 ]; then echo "transcripts kept in $out"; rm -rf "$work"; exit $status; fi
rm -rf "$out" "$work"
