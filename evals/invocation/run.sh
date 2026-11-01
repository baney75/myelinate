#!/bin/bash
# Does Claude Code actually call the Skill tool for a Myelinate skill?
# evals/triggers asks a model which skill it would pick from the listing; this runs
# real headless sessions with the plugin loaded and records the Skill calls.
# Usage: evals/invocation/run.sh [plugin-dir] [model] [passes]
# Sessions run inside $MYELINATE_EVAL_CWD when set (use a real code repository, so work
# prompts like "how does this function work" arrive mid-project), else an empty folder.
# Prompts: evals/invocation/prompts.txt, one "id|prompt" per line; ids starting with
# P should load a Myelinate skill, ids starting with N should load none.
# Each session uses your Claude Code sign-in and your user settings, hooks and skills,
# so results reflect your real setup, not an isolated one (isolating would mean copying
# credentials). Installed copies (myelinate@synced, myelinate@baney75) are disabled, and a
# session that still shows another myelinate plugin counts as an error; score.py counts only namespaced myelinate:<name> calls and lists any call to a
# standalone skill named myelinate separately. Sessions can't edit files or run commands
# (--disallowedTools), so a real repository in MYELINATE_EVAL_CWD is left untouched.
here=$(cd "$(dirname "$0")" && pwd)
plugin=$(cd "${1:-$here/../..}" && pwd); model=${2:-sonnet}; passes=${3:-1}
out=$(mktemp -d); scratch=$(mktemp -d); work=${MYELINATE_EVAL_CWD:-$scratch}
for pass in $(seq "$passes"); do
  while IFS='|' read -r id prompt; do
    [ -z "$id" ] && continue
    ( cd "$work" && timeout 300 claude -p --model "$model" --max-turns 3 \
        --output-format stream-json --verbose --plugin-dir "$plugin" \
        --disallowedTools Edit Write NotebookEdit Bash \
        --settings '{"enabledPlugins":{"myelinate@synced":false,"myelinate@baney75":false}}' \
        -- "$prompt" < /dev/null > "$out/$id.$pass.jsonl" 2> "$out/$id.$pass.err" ) &
  done < "$here/prompts.txt"
  wait
done
python3 "$here/score.py" "$out" "$plugin"; status=$?
echo "model=$model passes=$passes plugin=$plugin"
if [ $status -ne 0 ]; then echo "transcripts kept in $out"; rm -rf "$scratch"; exit $status; fi
rm -rf "$out" "$scratch"
