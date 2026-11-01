#!/bin/bash
# Does Claude Code actually call the Skill tool for a Myelinate skill?
# evals/triggers asks a model which skill it would pick from the listing; this runs
# real headless sessions with the plugin loaded and records the Skill calls.
# Usage: evals/invocation/run.sh [plugin-dir] [model] [passes]
# Prompts: evals/invocation/prompts.txt, one "id|prompt" per line; ids starting with
# P should load a Myelinate skill, ids starting with N should load none.
# Each session uses your Claude Code sign-in and your user settings, hooks and skills,
# so results reflect your real setup. A synced copy named myelinate@synced is disabled
# so only the plugin under test loads.
here=$(cd "$(dirname "$0")" && pwd)
plugin=$(cd "${1:-$here/../..}" && pwd); model=${2:-sonnet}; passes=${3:-1}
out=$(mktemp -d); work=$(mktemp -d)
for pass in $(seq "$passes"); do
  while IFS='|' read -r id prompt; do
    [ -z "$id" ] && continue
    ( cd "$work" && timeout 300 claude -p "$prompt" --model "$model" --max-turns 3 \
        --output-format stream-json --verbose --plugin-dir "$plugin" \
        --settings '{"enabledPlugins":{"myelinate@synced":false}}' \
        < /dev/null > "$out/$id.$pass.jsonl" 2>/dev/null ) &
  done < "$here/prompts.txt"
  wait
done
hit=0; pos=0; fire=0; neg=0
for f in "$out"/*.jsonl; do
  name=$(basename "$f" .jsonl)
  skills=$(grep -o '"name":"Skill","input":{"skill":"myelinate[^"]*"' "$f" | sed 's/.*"skill":"//;s/"$//' | sort -u | tr '\n' ' ')
  echo "$name ${skills:-none}"
  case $name in
    P*) pos=$((pos+1)); [ -n "$skills" ] && hit=$((hit+1)) ;;
    N*) neg=$((neg+1)); [ -n "$skills" ] && fire=$((fire+1)) ;;
  esac
done
echo "model=$model loaded on $hit/$pos learning prompts, $fire/$neg work prompts"
rm -rf "$out" "$work"
