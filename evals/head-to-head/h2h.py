"""Blind head-to-head: learn skill vs myelinate on tutoring scenarios.

usage: python3 evals/head-to-head/h2h.py OUTDIR MYELINATE_ROOT LEARN_SKILL_MD [--repeats N] [--only id,id]
LEARN_SKILL_MD is a local copy of the comparison skill (not vendored here).
Responder: Sonnet via claude -p (no tools). Judge: Opus, blind, randomized order.
"""
import json, random, subprocess, sys, concurrent.futures as cf
from pathlib import Path

HERE = Path(__file__).parent
LEARN = Path(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else None
BASE = ["claude", "-p", "--tools", "", "--setting-sources", "", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', "--no-session-persistence"]
ENV_DEFAULT = "No tools are available this turn. If a visual would help, draw it with markdown, ASCII or a code block."


def skill_text(arm, scen, root):
    if arm == "learn":
        return LEARN.read_text()
    parts = [(root / "myelinate.md").read_text()]
    for s in ([] if arm == "router" else scen.get("subs", [])):
        parts.append(f"\n\n# Loaded sub-skill file skills/{s}/SKILL.md\n\n" + (root / f"skills/{s}/SKILL.md").read_text())
    return "".join(parts)


def call(model, system, prompt):
    r = subprocess.run(BASE + ["--model", model, "--system-prompt", system, prompt],
                       capture_output=True, text=True, timeout=600, cwd=HERE)
    return r.stdout.strip()


def respond(arm, scen, root):
    system = ("You are Claude, chatting with a person on claude.ai. This skill is loaded and you follow it:\n\n<skill>\n"
              + skill_text(arm, scen, root) + "\n</skill>\n\n" + scen.get("env", ENV_DEFAULT))
    ctx = ""
    if scen.get("memory"):
        ctx += f"[Memory about this person: {scen['memory']}]\n\n"
    if scen.get("transcript"):
        ctx += "Conversation so far:\n" + scen["transcript"] + "\n\nThe person's new message:\n"
    prompt = ctx + scen["message"] + ("\n\n(Write only your next reply to the person.)" if scen.get("transcript") else "")
    return call("sonnet", system, prompt)


JUDGE = """You are an expert tutor-trainer grading two AI tutor replies blind. Grade only the reply text.
Scenario context:
{ctx}
Person's message: {msg}

Rubric for this scenario: {rubric}

General standard: the person should leave more able to do it themselves; diagnose before teaching when the need is unclear;
one focused question plus a scaffold per turn in tutoring; short turns; no answer leaks in hints; no false or hollow praise;
honest verdicts; direct help for real deadlines and for topical "just lay it out" requests; resource requests just get made;
accuracy matters; warm, direct, adult tone, no emoji.

Reply A:
<<<
{a}
>>>

Reply B:
<<<
{b}
>>>

Return only JSON: {{"score_A": 1-10, "score_B": 1-10, "winner": "A"|"B"|"tie", "reason": "<=40 words"}}"""


def judge(scen, a, b):
    ctx = (scen.get("memory", "") + "\n" + scen.get("transcript", "")).strip() or "(none)"
    out = call("opus", "You grade tutoring replies. Output JSON only.",
               JUDGE.format(ctx=ctx, msg=scen["message"], rubric=scen["rubric"], a=a, b=b))
    s = out[out.find("{"): out.rfind("}") + 1]
    return json.loads(s)


def run_one(scen, rep, root, outdir):
    r = {arm: respond(arm, scen, root) for arm in ("learn", "myelinate", "router")}
    res = {"id": scen["id"], "rep": rep, "replies": r}
    for other in ("myelinate", "router"):
        a, b = (other, "learn") if random.random() < 0.5 else ("learn", other)
        try:
            v = judge(scen, r[a], r[b])
        except Exception as e:  # judge output unparsable
            v = {"score_A": 0, "score_B": 0, "winner": "error", "reason": str(e)}
        res[other] = {"score": {a: v["score_A"], b: v["score_B"]},
                      "winner": {"A": a, "B": b}.get(v["winner"], v["winner"]), "reason": v["reason"]}
    (outdir / f"{scen['id']}-{rep}.json").write_text(json.dumps(res, indent=1))
    return res


def main():
    outdir, root = Path(sys.argv[1]), Path(sys.argv[2])
    repeats = int(sys.argv[sys.argv.index("--repeats") + 1]) if "--repeats" in sys.argv else 1
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    outdir.mkdir(parents=True, exist_ok=True)
    scens = [s for s in json.loads((HERE / "scenarios.json").read_text()) if not only or s["id"] in only]
    jobs = [(s, k) for s in scens for k in range(repeats)]
    with cf.ThreadPoolExecutor(6) as ex:
        results = list(ex.map(lambda j: run_one(j[0], j[1], root, outdir), jobs))
    n = len(results)
    for other in ("myelinate", "router"):
        tl = to = 0
        wins = {}
        print(f"\n== learn vs {other}")
        for r in sorted(results, key=lambda r: r["id"]):
            m = r[other]
            tl += m["score"].get("learn", 0); to += m["score"].get(other, 0)
            wins[m["winner"]] = wins.get(m["winner"], 0) + 1
            print(f"{r['id']:<22} L={m['score'].get('learn')} {other[0].upper()}={m['score'].get(other)} win={m['winner']:<9} {m['reason']}")
        print(f"mean learn={tl/n:.2f} {other}={to/n:.2f} wins={wins}")


if __name__ == "__main__":
    main()
