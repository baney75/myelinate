#!/usr/bin/env python3
"""SessionStart hook: one line that tells Claude when to load Myelinate.

Claude Code lists every installed skill, but for a question it can answer on its
own ("explain Le Chatelier's principle") the model tends to answer directly and
never calls the Skill tool, so the learning skills don't run. This line names the
moment. It stays silent when MYELINATE_ROUTE_HINT=0.
"""
import os

HINT = ("Myelinate (learning plugin) is installed. When the user wants to learn, understand, study or practice "
        "a subject (a concept, how something works, a class topic, homework or a lab report, an exam, a bare "
        "topic), call the Skill tool for the matching myelinate skill (myelinate:tutor, myelinate:assignment, "
        "myelinate:teach, myelinate:myelinate and so on) before you answer, even for a quick question. "
        "Don't load it for work they want done or for questions about the code, repository, errors or files "
        "in front of them (explain this stack trace, what does this function do), unless they say they want "
        "to learn it.")

if os.environ.get('MYELINATE_ROUTE_HINT', '1') != '0':
    print(HINT)
