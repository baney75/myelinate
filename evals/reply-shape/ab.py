"""Blind A/B of two Myelinate skill texts on reply-shape scenarios (v2.7.0).

usage: python3 evals/reply-shape/ab.py OUT OLD_ROOT NEW_ROOT REPS [id,id]
OLD_ROOT and NEW_ROOT are checkouts (or copies) of this repo. Each reply is written by Sonnet
(claude -p, no tools) with the router plus the scenario's sub-skill as the system prompt and a
host note that show_widget blocks render inline; Opus judges each old/new pair in random order.
Writer and judge are both Claude models. Results: one JSON per pair in OUT, a summary on stdout.
"""
import json, random, re, subprocess, sys, concurrent.futures as cf
from pathlib import Path

OUT, OLD, NEW, REPS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
ONLY = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
OUT.mkdir(parents=True, exist_ok=True)
BASE = ["claude", "-p", "--tools", "", "--setting-sources", "", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', "--no-session-persistence"]
ENV = ("Host: claude.ai. You can render an inline visual: write a fenced block whose info string is show_widget containing "
       "self-contained HTML/SVG/JS; it renders inline in the conversation (dark and light mode). A widget can call "
       "sendPrompt(text) to send a message back to you as the user. Write only your reply.")
PRELAB = """Here's my prelab for Williamson ether synthesis (2-naphthol + butyl p-toluenesulfonate, NaOH, ethanol, reflux -> 2-butoxynaphthalene):
1. Identify the nucleophile and explain why it is a good nucleophile.
2. Identify the electrophile and the electrophilic carbon.
3. Identify the leaving group and explain why it is a good leaving group.
4. Draw the full mechanism, including the transition state.
5. What are the solvent conditions and why were they chosen?
6. What are the preferred conditions for an SN2 reaction? Does this lab meet them?
Week 2 report: determine the limiting reagent and theoretical yield. We use 0.72 g 2-naphthol, 0.32 g NaOH, 1.1 mL butyl tosylate (d = 1.10 g/mL).

Teach me all I need to know so I can be confident that I can solve these"""
SCEN = [
    {"id": "prelab", "subs": ["assignment"], "msg": PRELAB,
     "rubric": "Graded prelab and lab-report math. Best: teaches the few ideas the questions rest on (nucleophile strength and deprotonation, leaving-group ability, SN2 conditions, limiting reagent) using parallel cases, an inline visual the learner operates, and hands question 1 back for the learner to answer. Fails: writes out answers to Q1-6 or computes their theoretical yield; a long cluttered wall of text; many bold headings; more than one question at the end."},
    {"id": "exam", "subs": ["tutor"], "msg": "Exam Friday on acid-base equilibria (buffers, Henderson-Hasselbalch, titration curves). This is the ungraded review sheet. Teach me everything I need to know.",
     "rubric": "Practice, not graded. Best: a map of the few core ideas, teaches the first one well with an inline visual (for example a titration curve they operate), one question; lean and scannable. Fails: an exhaustive scroll covering everything at once; stacked bold headings; recap; no learner action."},
    {"id": "layout", "subs": ["teach"], "msg": "Just lay out how CRISPR-Cas9 gene editing works. I want the whole picture, not a quiz.",
     "rubric": "Legitimate 'just lay it out' request. Best: a substantive but tight structured overview, a visual, accurate, ends with at most one optional offer; no quiz. Fails: quizzing them; a sprawling essay; padding; inaccuracy; so thin it misses the whole picture they asked for."},
    {"id": "practice", "subs": ["tutor"], "msg": """Ungraded practice set from my professor's review sheet, get me ready:
1. Rank by SN2 rate: 1-bromobutane, 2-bromobutane, 2-bromo-2-methylpropane.
2. Which is the better leaving group, Cl- or I-? Why?
3. Predict the product of sodium ethoxide with iodomethane.
4. Why does DMSO speed up SN2 compared with methanol?
5. What happens to the stereocenter in (R)-2-bromobutane with NaCN?""",
     "rubric": "Ungraded practice set. Best: turns the set into practice the learner does, ideally an inline widget with a card or box per question, hints, and a way to check or send answers, plus a short lead-in naming the ideas; lean. Fails: answering all five in prose; a long lecture before any practice; stacked bold headings."},
    {"id": "quick", "subs": ["tutor"], "msg": "Quick class question: why does SN2 need backside attack?",
     "rubric": "Quick class question. Best: a short direct answer (orbital reason: the nucleophile enters the C-LG sigma* lobe opposite the leaving group), maybe a small visual, one check question. Fails: a long lecture; refusing to answer; multiple questions."},
]
JUDGE = """You are an expert tutor-trainer grading two AI tutor replies blind. Fenced show_widget blocks render as inline interactive visuals; judge them as what the learner would see and use.
Person's message: {msg}
Rubric: {rubric}
Also judge clutter: would a student find this easy to scan and act on, or a wall?
Reply A:
<<<
{a}
>>>
Reply B:
<<<
{b}
>>>
Return only JSON: {{"score_A": 1-10, "score_B": 1-10, "winner": "A"|"B"|"tie", "leaks_graded_answers_A": true|false, "leaks_graded_answers_B": true|false, "reason": "<=40 words"}}"""


def skill(root, subs):
    t = (root / "myelinate.md").read_text()
    for s in subs:
        t += f"\n\n# Loaded sub-skill file skills/{s}/SKILL.md\n\n" + (root / f"skills/{s}/SKILL.md").read_text()
    return t


def call(model, system, prompt):
    return subprocess.run(BASE + ["--model", model, "--system-prompt", system, prompt],
                          capture_output=True, text=True, timeout=900, cwd=OUT).stdout.strip()


def respond(root, sc):
    return call("sonnet", "You are Claude, chatting with a person. This skill is loaded and you follow it:\n\n<skill>\n"
                + skill(root, sc["subs"]) + "\n</skill>\n\n" + ENV, sc["msg"])


def prose_words(t):
    return len(re.sub(r"```.*?```", " ", t, flags=re.S).split())


def one(sc, rep):
    r = {"old": respond(OLD, sc), "new": respond(NEW, sc)}
    order = ["old", "new"]
    random.shuffle(order)
    out = call("opus", "You grade tutoring replies. Output JSON only.",
               JUDGE.format(msg=sc["msg"], rubric=sc["rubric"], a=r[order[0]], b=r[order[1]]))
    j = json.loads(out[out.find("{"): out.rfind("}") + 1])
    m = {"A": order[0], "B": order[1]}
    res = {"id": sc["id"], "rep": rep, "replies": r, "order": order, "judge": j,
           "score": {m["A"]: j["score_A"], m["B"]: j["score_B"]}, "winner": m.get(j["winner"], "tie"),
           "leak": {m["A"]: j["leaks_graded_answers_A"], m["B"]: j["leaks_graded_answers_B"]},
           "words": {k: prose_words(v) for k, v in r.items()},
           "bold": {k: len(re.findall(r"\*\*[^*]+\*\*", v)) for k, v in r.items()},
           "widget": {k: "```show_widget" in v for k, v in r.items()},
           "answer_boxes": {k: sum(len(re.findall(p, b)) for b in re.findall(r"```show_widget(.*?)```", v, flags=re.S)
                                   for p in (r"<input(?![^>]*type=.(?:range|button|radio|checkbox))", r"<textarea"))
                            for k, v in r.items()}}
    (OUT / f"{sc['id']}-{rep}.json").write_text(json.dumps(res, indent=1))
    return res


jobs = [(s, k) for s in SCEN if not ONLY or s["id"] in ONLY for k in range(REPS)]
with cf.ThreadPoolExecutor(6) as ex:
    res = list(ex.map(lambda a: one(*a), jobs))
for s in SCEN:
    rs = [r for r in res if r["id"] == s["id"]]
    if not rs:
        continue
    f = lambda arm, key: [r[key][arm] for r in rs]
    print(s["id"], "wins old/new/tie", sum(r["winner"] == "old" for r in rs), sum(r["winner"] == "new" for r in rs),
          sum(r["winner"] == "tie" for r in rs), "| score", f("old", "score"), f("new", "score"),
          "| words", f("old", "words"), f("new", "words"), "| bold", f("old", "bold"), f("new", "bold"),
          "| leak", f("old", "leak"), f("new", "leak"), "| widget", f("old", "widget"), f("new", "widget"),
          "| answer boxes", f("old", "answer_boxes"), f("new", "answer_boxes"), flush=True)
