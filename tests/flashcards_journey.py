#!/usr/bin/env python3
"""Open the flashcard deck template offline and check study flow, math rendering, exports and layout."""
import json
import os
import re
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

TEMPLATE = Path(__file__).resolve().parents[1] / 'templates' / 'flashcards-deck.html'
URL = TEMPLATE.as_uri()
SHOTS = Path(os.environ.get('DECK_SHOTS', '/tmp/deck-shots'))
SHOTS.mkdir(parents=True, exist_ok=True)
KEY = 'myelinate-deck:BIOL 101 \u00b7 Exam 3|Example Deck'


def make_deck(cards, **extra):
    """Serialize a deck the way the template asks: a real serializer, with < escaped."""
    return json.dumps({'title': 'T', **extra, 'cards': cards}).replace('<', '\\u003c')


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print('PASS:', message)


def variant(deck_json, into=None):
    """Write a copy of the template with different deck JSON and return its file URL (into: reuse that file path)."""
    html = TEMPLATE.read_text()
    html = re.sub(r'(<script type="application/json" id="deck">).*?(</script>)', lambda m: m.group(1) + deck_json + m.group(2), html, count=1, flags=re.S)
    path = Path(into) if into else Path(tempfile.mkdtemp(prefix='deck-variant-')) / 'deck.html'
    path.write_text(html)
    return path.as_uri()


def open_page(browser, width, scheme, motion, url=URL):
    context = browser.new_context(viewport={'width': width, 'height': 900}, color_scheme=scheme, reduced_motion=motion)
    requests = []

    def handle(route):
        if route.request.url.startswith('file://'):
            route.continue_()
        else:
            requests.append(route.request.url)
            route.abort()

    context.route('**/*', handle)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(url)
    return context, page, errors, requests


def front_text(page):
    return page.locator('#front').inner_text()


def probe(page, text, tex=False):
    return page.evaluate("""([text, tex]) => {
        const d = document.createElement('div');
        d.innerHTML = window.renderMath(text, {tex});
        const q = s => d.querySelectorAll(s).length;
        return {math: q('math'), msup: q('msup'), msub: q('msub'), msubsup: q('msubsup'), mfrac: q('mfrac'), mroot: q('mroot'),
                msqrt: q('msqrt'), error: q('.math-error'), script: q('script'), text: d.textContent, errTitle: (d.querySelector('.math-error') || {}).title || ''};
    }""", [text, tex])


def stored(page):
    return page.evaluate("k => JSON.parse(localStorage.getItem(k) || 'null')", KEY)


def page_plain_bold(page):
    return page.evaluate('renderMath.plain("\\\\(\\\\mathbf{v}\\\\)")') == 'v'


def rate_through(page, rating, count):
    for _ in range(count):
        page.locator('#show').click()
        page.locator(f'#rate-{rating}').click()


with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for width, scheme, motion in [(1280, 'light', 'no-preference'), (360, 'dark', 'reduce')]:
        tag = f'{width}px'
        context, page, errors, requests = open_page(browser, width, scheme, motion)

        # Loading and header
        check(page.locator('h1').inner_text() == 'Example Deck', f'{tag} title shown')
        check('8 cards' in page.locator('#deck-meta').inner_text() and 'BIOL 101' in page.locator('#deck-meta').inner_text(), f'{tag} header shows count and course')
        check(page.locator('#browse-list li').count() == 8, f'{tag} deck has 8 cards')
        check('Card 1 of 8 · 7 left this round' in page.locator('#progress').inner_text(), f'{tag} status line starts at card 1 of 8')
        check('Due today: 8' in page.locator('#due-count').inner_text(), f'{tag} all cards due on first visit')
        check(page.locator('#back-panel').is_hidden(), f'{tag} back hidden before reveal')
        check('Hardy' in front_text(page), f'{tag} first card front shown')
        check(page.locator('label[for=answer]').inner_text() == 'Your answer (say it or type it)', f'{tag} answer label')
        check('\\' not in front_text(page), f'{tag} first front has no raw backslashes')

        # Reveal by button, with typed answer beside the back
        page.locator('#answer').fill('p squared plus 2pq plus q squared')
        page.locator('#show').click()
        check(page.locator('#back-panel').is_visible(), f'{tag} reveal by button works')
        check('p squared plus 2pq plus q squared' in page.locator('#typed').inner_text(), f'{tag} typed answer shown')
        both = page.locator('.compare').evaluate("""el => { const k = [...el.children].map(c => c.getBoundingClientRect()); return {sameRow: Math.abs(k[0].top - k[1].top) < 4, sameCol: Math.abs(k[0].left - k[1].left) < 4}; }""")
        check(both['sameRow'] if width == 1280 else both['sameCol'], f'{tag} typed answer sits beside (wide) or above (phone) the back')
        check(page.locator('#back math').count() >= 1, f'{tag} back renders MathML')
        check(page.locator('#hint math').count() == 1 and 'Genotypes add to 1' in page.locator('#hint').inner_text(), f'{tag} hint shown after reveal with pandoc math')
        check(page.locator('#answer').is_disabled(), f'{tag} answer locked after reveal')

        # Keyboard rate: 1 = Again requeues card
        first = front_text(page)
        page.keyboard.press('1')
        check('Card 2 of 9' in page.locator('#progress').inner_text(), f'{tag} Again keeps card in round (round grows to 9)')
        check(front_text(page) != first, f'{tag} next card follows Again')
        check(page.locator('#front math').count() >= 1 and page.locator('#front').inner_text().count('\\') == 0, f'{tag} a front that contains math renders MathML with no raw backslashes')
        saved = stored(page)
        check(saved['cards']['hw1']['interval'] == 0 and 9 * 60000 < saved['cards']['hw1']['due'] - saved['cards']['hw1']['last'] <= 10 * 60000, f'{tag} Again schedules 10 minutes')

        # Reveal by keyboard (Space, then Enter on a fresh card)
        page.keyboard.press('Space')
        check(page.locator('#back-panel').is_visible(), f'{tag} Space reveals')
        page.keyboard.press('3')
        check(stored(page)['cards']['af1']['interval'] == 1, f'{tag} Good on a new card sets 1 day')
        page.keyboard.press('Enter')
        check(page.locator('#back-panel').is_visible(), f'{tag} Enter reveals')
        page.keyboard.press('2')
        exp = stored(page)['cards']['exp1']
        check(exp['interval'] == 1, f'{tag} Hard on a new card is at least 1 day')
        page.keyboard.press('Enter')
        page.keyboard.press('4')
        check(stored(page)['cards']['log1']['interval'] == 3, f'{tag} Easy on a new card jumps two rungs (3 days)')
        check('Space' not in page.locator('#answer').input_value(), f'{tag} shortcuts do not type into the answer box')

        # Typing in the textarea never triggers shortcuts
        page.locator('#answer').focus()
        page.keyboard.type('3 4 ')
        check(page.locator('#back-panel').is_hidden(), f'{tag} typing Space/digits in the answer box does not reveal or rate')
        page.keyboard.press('Control+Enter')
        check(page.locator('#back-panel').is_visible(), f'{tag} Ctrl+Enter in the box reveals')
        check(page.locator('#typed').inner_text() == '3 4', f'{tag} typed digits kept as text')
        page.locator('#rate-good').click()
        page.locator('#answer').focus()
        page.keyboard.press('Meta+Enter')
        check(page.locator('#back-panel').is_visible(), f'{tag} Cmd+Enter in the box reveals')
        page.locator('#rate-good').click()

        # Finish the round: the card rated Again comes back as the last card of round 1
        seen = []
        while 'Round 2' not in page.locator('#progress').inner_text():
            seen.append(front_text(page))
            page.locator('#show').click()
            page.locator('#rate-good').click()
        check(seen.count(first) == 1 and seen[-1] == first, f'{tag} Again card reappears at the end of the round ({len(seen)} more cards)')
        check('Card 1 of' in page.locator('#progress').inner_text(), f'{tag} round 2 position resets')

        # Persistence across reload
        before = stored(page)
        page.reload()
        check(stored(page) == before, f'{tag} schedule survives reload')
        check('Due today:' in page.locator('#due-count').inner_text(), f'{tag} due count shown after reload')
        check(page.locator('#browse-list li').count() == 8, f'{tag} deck still 8 cards after reload')

        # Ladder: Good in separate sessions climbs 1 -> 3 -> 7 -> 14 -> 30 -> 30
        page.evaluate("k => localStorage.removeItem(k)", KEY)
        steps = []
        for _ in range(6):
            page.evaluate("""k => { const o = JSON.parse(localStorage.getItem(k)) || {v: 1, cards: {}}; ['hw1','af1','exp1','log1','lam1','rk1','app1','clz1'].forEach(i => { o.cards[i] = o.cards[i] || {interval: 0, reps: 1}; o.cards[i].due = 1; }); localStorage.setItem(k, JSON.stringify(o)); }""", KEY)
            page.reload()
            check('Hardy' in front_text(page), 'overdue-or-new first card is shown first')
            page.locator('#show').click()
            page.locator('#rate-good').click()
            steps.append(stored(page)['cards']['hw1']['interval'])
        check(steps == [1, 3, 7, 14, 30, 30], f'{tag} Good ladder 1 -> 3 -> 7 -> 14 -> 30 (got {steps})')

        # Hard, Good and Easy from a 7 day interval
        page.evaluate("k => localStorage.setItem(k, JSON.stringify({v: 1, cards: Object.fromEntries(['hw1','af1','exp1','log1','lam1','rk1','app1','clz1'].map(i => [i, {interval: 7, due: 1, reps: 1}]))}))", KEY)
        page.reload()
        for expected in ['hard', 'good', 'easy']:
            page.locator('#show').click()
            page.locator(f'#rate-{expected}').click()
        s = stored(page)['cards']
        check(s['hw1']['interval'] == 3.5 and s['af1']['interval'] == 14 and s['exp1']['interval'] == 30, f'{tag} Hard halves (7 -> 3.5), Good climbs (7 -> 14), Easy skips (7 -> 30)')
        check(s['af1']['due'] > s['hw1']['due'] > 0 and s['exp1']['due'] > s['af1']['due'], f'{tag} due dates follow intervals')
        page.evaluate("k => localStorage.removeItem(k)", KEY)
        page.reload()

        # Three correct recalls retire a card from the session
        page.locator('#tag-filter').select_option('Life history')
        check('Card 1 of 1' in page.locator('#progress').inner_text(), f'{tag} tag filter narrows the session')
        check('r-selected' in front_text(page) or 'Contrast' in front_text(page), f'{tag} filtered card is the Life history card')
        rate_through(page, 'good', 2)
        check(page.locator('#done').is_hidden() and 'Round 3' in page.locator('#progress').inner_text(), f'{tag} card still needs a third recall')
        rate_through(page, 'good', 1)
        check(page.locator('#done').is_visible(), f'{tag} card leaves the session after 3 correct recalls')
        page.locator('#again-session').click()
        check(page.locator('#card').is_visible(), f'{tag} Study again restarts')
        check(stored(page)['cards']['rk1']['interval'] == 1, f'{tag} three Goods in one session only climb one rung')
        practised = stored(page)['cards']['rk1']
        page.locator('#show').click()
        page.locator('#rate-good').click()
        after = stored(page)['cards']['rk1']
        check(after['interval'] == practised['interval'] == 1 and after['due'] == practised['due'], f'{tag} Study again on a not-due card leaves interval and due unchanged')
        for _ in range(4):
            page.locator('#again-session').click()
            page.locator('#show').click()
            page.locator('#rate-easy').click()
        check(stored(page)['cards']['rk1']['interval'] == 1, f'{tag} five restarts do not climb the ladder')

        def seed(state):
            page.evaluate("([k, st]) => localStorage.setItem(k, JSON.stringify({v: 1, cards: {rk1: st}}))", [KEY, state])
            page.reload()
            page.locator('#tag-filter').select_option('Life history')

        seed({'interval': 7, 'due': 1, 'reps': 1})
        page.locator('#show').click()
        page.locator('#rate-good').click()
        check(page.locator('#done').is_visible() and stored(page)['cards']['rk1']['interval'] == 14, f'{tag} a due review card leaves after one Good')
        seed({'interval': 7, 'due': 1, 'reps': 1})
        page.locator('#show').click()
        page.locator('#rate-hard').click()
        check(page.locator('#done').is_visible(), f'{tag} Hard also counts as a correct recall for a review card')
        seed({'interval': 7, 'due': 1, 'reps': 1})
        page.locator('#show').click()
        page.locator('#rate-again').click()
        check(page.locator('#done').is_hidden() and 'of 2' in page.locator('#progress').inner_text(), f'{tag} Again still requeues a review card')
        seed({'interval': 8, 'due': 1, 'reps': 0})
        rate_through(page, 'hard', 2)
        check(page.locator('#done').is_hidden() and stored(page)['cards']['rk1']['interval'] == 4, f'{tag} Hard adjusts the interval once per card per session (8 -> 4, got {stored(page)["cards"]["rk1"]["interval"]})')

        # Reset progress with confirm
        page.once('dialog', lambda d: d.dismiss())
        page.locator('#reset-progress').click()
        check(stored(page) is not None, f'{tag} cancelled confirm keeps progress')
        page.once('dialog', lambda d: d.accept())
        page.locator('#reset-progress').click()
        check(stored(page) is None, f'{tag} accepted confirm clears progress')

        # Shuffle, tag filter all
        page.locator('#tag-filter').select_option('')
        page.locator('#shuffle').check()
        check('Card 1 of 8' in page.locator('#progress').inner_text(), f'{tag} shuffle keeps all 8 cards')
        page.locator('#shuffle').uncheck()

        # Browse mode
        page.locator('#mode-browse').click()
        check(page.locator('#browse').is_visible() and page.locator('#study').is_hidden(), f'{tag} browse mode swaps views')
        check(page.locator('#browse-list li').count() == 8, f'{tag} browse lists all 8 cards')
        browse_text = page.locator('#browse-list').inner_text()
        check(page.locator('#browse .math-error, .math-error').count() == 0, f'{tag} no .math-error anywhere in the shipped deck')
        for raw in ['\\frac', '^{', '\\(', '$', '\\[', '\\Delta', '{{c']:
            check(raw not in browse_text, f'{tag} browse text has no raw {raw!r}')
        check(page.locator('#browse math').count() >= 15, f'{tag} browse list has MathML ({page.locator("#browse math").count()} elements)')
        check(page.locator('#browse msup').count() > 0 and page.locator('#browse mfrac').count() > 0 and page.locator('#browse msubsup, #browse msub').count() > 0, f'{tag} browse has superscripts, fractions and subscripts')
        check('Δ' in browse_text and 'λ' in browse_text, f'{tag} Greek letters render as characters')
        check(page.locator('#browse mark.cloze-answer').count() == 2, f'{tag} cloze answers highlighted in browse')
        check('<script' not in page.locator('#browse-list').inner_html(), f'{tag} no script injected in browse')
        scroll = page.evaluate('document.scrollingElement.scrollWidth')
        check(scroll <= width, f'{tag} browse has no horizontal scroll ({scroll} <= {width})')
        page.screenshot(path=str(SHOTS / f'browse-{width}-{scheme}.png'), full_page=True)

        # Study screenshots for the Hardy-Weinberg card
        page.locator('#mode-study').click()
        page.evaluate("k => localStorage.removeItem(k)", KEY)
        page.reload()
        page.screenshot(path=str(SHOTS / f'front-{width}-{scheme}.png'), full_page=True)
        page.locator('#answer').fill('p squared plus two p q plus q squared equals one')
        page.locator('#show').click()
        scroll = page.evaluate('document.scrollingElement.scrollWidth')
        check(scroll <= width, f'{tag} revealed card has no horizontal scroll ({scroll} <= {width})')
        page.wait_for_timeout(450)
        page.screenshot(path=str(SHOTS / f'back-{width}-{scheme}.png'), full_page=True)
        page.locator('#rate-good').click()

        # Cloze card front and back
        page.locator('#tag-filter').select_option('Population genetics')
        seen_cloze = False
        for _ in range(6):
            if page.locator('#front .cloze-blank').count():
                seen_cloze = True
                check('[ … ]' in front_text(page) and 'very large' not in front_text(page), f'{tag} cloze front shows blanks without answers')
                page.locator('#show').click()
                check(page.locator('#back mark.cloze-answer').count() == 2 and 'genetic drift' in page.locator('#back').inner_text(), f'{tag} cloze back highlights answers')
                break
            page.locator('#show').click()
            page.locator('#rate-good').click()
        check(seen_cloze, f'{tag} cloze card reached')

        # Exports
        quizlet = page.evaluate('window.deckExports.quizlet()')
        lines = [ln for ln in quizlet.split('\n') if ln]
        check(len(lines) == 8 and all(ln.count('\t') == 1 for ln in lines), f'{tag} Quizlet export: 8 lines, exactly one tab each')
        check('p² + 2pq + q² = 1' in quizlet, f'{tag} Quizlet export converts math to Unicode (p² + 2pq + q² = 1)')
        check('(120)/(200)' in quizlet and 'Nₜ' in quizlet and 'ΔN' in quizlet and 'λ' in quizlet, f'{tag} Quizlet export: fraction, subscript, Greek')
        check('\\' not in quizlet and '^{' not in quizlet and '**' not in quizlet, f'{tag} Quizlet export has no TeX or markup')
        anki = page.evaluate('window.deckExports.anki()')
        check(anki.startswith('#separator:tab\n#html:true\n#notetype:Basic\n#tags column:3\n'), f'{tag} Anki export starts with #separator:tab and #notetype:Basic')
        check('\\(p^2\\)' in anki and '\\[p^2 + 2pq + q^2 = 1\\]' in anki, f'{tag} Anki export keeps MathJax delimiters')
        check(all(len(ln.split('\t')) == 3 for ln in anki.split('\n')[4:] if ln) and 'Population_genetics' in anki, f'{tag} Anki rows have front, back, tags')
        check('{{c1::' not in anki, f'{tag} cloze card kept out of the basic Anki file')
        cloze = page.evaluate('window.deckExports.ankiCloze()')
        check(cloze.startswith('#separator:tab\n#html:true\n#notetype:Cloze\n') and '{{c1::very large}}' in cloze and '{{c2::genetic drift}}' in cloze, f'{tag} cloze Anki file has #notetype:Cloze and cloze markers')
        with page.expect_download() as info:
            page.locator('#export-quizlet').click()
        check(info.value.suggested_filename == 'example-deck-quizlet.txt', f'{tag} Quizlet download filename from title')
        with page.expect_download() as info:
            page.locator('#export-anki-cloze').click()
        check(info.value.suggested_filename == 'example-deck-anki-cloze.txt', f'{tag} cloze download filename from title')

        # No private-use or zero-width characters hide in the source
        source = TEMPLATE.read_text(encoding='utf-8')
        hidden = [hex(ord(ch)) for ch in source if 0xE000 <= ord(ch) <= 0xF8FF or 0x200B <= ord(ch) <= 0x200D]
        check(not hidden, f'{tag} template source has no private-use or zero-width characters ({hidden})')

        # Layout and hygiene
        scroll = page.evaluate('document.scrollingElement.scrollWidth')
        check(scroll <= width, f'{tag} no horizontal scroll ({scroll} <= {width})')
        if width == 360:
            check(page.evaluate('[...document.querySelectorAll("button")].filter(b => b.offsetParent).every(b => b.getBoundingClientRect().height >= 44)'), f'{tag} visible buttons are at least 44px tall')
        check(not requests, f'{tag} no network requests attempted ({requests})')
        check(not errors, f'{tag} no page errors ({errors})')

        # Print layout
        page.emulate_media(media='print')
        page.locator('#mode-study').evaluate('el => el.click()')
        check(page.locator('#browse').is_visible() and page.locator('#study').is_hidden() and page.locator('.toolbar').is_hidden(), f'{tag} print shows the browse list and hides study and controls')
        check(page.locator('#browse-list').evaluate('el => getComputedStyle(el).columnCount') == '2', f'{tag} print list is two-column')
        check(page.locator('button:visible').count() == 0, f'{tag} print shows no buttons')
        page.emulate_media(media='screen')
        context.close()

    # Math unit cases
    context, page, errors, requests = open_page(browser, 1280, 'light', 'no-preference')
    r = probe(page, 'p^2 + 2pq + q^2 = 1', tex=True)
    check(r['msup'] == 2, f'renderMath: p^2 + 2pq + q^2 = 1 has exactly 2 msup (got {r["msup"]})')
    check(probe(page, '\\frac{dN}{dt}', tex=True)['mfrac'] == 1, 'renderMath: \\frac{dN}{dt} has mfrac')
    check(probe(page, '\\dfrac{a}{b} + \\tfrac{1}{2}', tex=True)['mfrac'] == 2, 'renderMath: dfrac and tfrac')
    check('Δ' in probe(page, '\\Delta N', tex=True)['text'], 'renderMath: \\Delta N contains Δ')
    check(probe(page, 'x_i^2', tex=True)['msubsup'] == 1, 'renderMath: x_i^2 has msubsup')
    check(probe(page, 'N_{t+1}', tex=True)['msub'] == 1, 'renderMath: braced subscript has msub')
    check(probe(page, '\\sqrt[3]{x}', tex=True)['mroot'] == 1, 'renderMath: \\sqrt[3]{x} has mroot')
    check(probe(page, '\\sqrt{x}', tex=True)['msqrt'] == 1, 'renderMath: \\sqrt{x} has msqrt')
    r = probe(page, '\\bogus{x}', tex=True)
    check(r['error'] == 1 and r['math'] == 0 and r['errTitle'] == 'unsupported: \\bogus' and '\\bogus{x}' in r['text'], 'renderMath: \\bogus{x} yields .math-error without throwing')
    r = probe(page, '\\frac{a}{b', tex=True)
    check(r['error'] == 1 and 'unbalanced' in r['errTitle'], 'renderMath: unbalanced braces yield .math-error')
    r = probe(page, '$5 and $6')
    check(r['math'] == 0 and r['text'] == '$5 and $6', 'renderMath: "$5 and $6" stays text under the pandoc rule')
    check(probe(page, 'costs $5 or $x$ here')['math'] == 1, 'renderMath: $x$ is math, $5 stays text')
    check(probe(page, 'it is \\$5 and \\$6')['text'] == 'it is $5 and $6', 'renderMath: escaped dollars are literal')
    r = probe(page, '<script>alert(1)</script>')
    check(r['script'] == 0 and r['text'] == '<script>alert(1)</script>', 'renderMath: <script> renders as text, not an element')
    check(probe(page, 'a **b** and *c*')['text'] == 'a b and c', 'renderMath: bold and italic markup')
    check(probe(page, '2 * 3 * 4')['text'] == '2 * 3 * 4', 'renderMath: spaced asterisks stay text')
    check(probe(page, '\\left( \\frac{1}{2} \\right)^2 \\cdot \\pm \\infty \\to \\rightleftharpoons', tex=True)['error'] == 0, 'renderMath: left/right, cdot, pm, infty, arrows parse')
    check(probe(page, '\\overline{x} \\bar{y} \\hat{z} \\sum_{i=1}^{n} x_i \\int_0^1 f \\partial \\ln x \\sin\\theta 90^\\circ 5\\% \\,\\; \\quad \\text{rate} \\mathrm{kg}', tex=True)['error'] == 0, 'renderMath: overline, bar, hat, sum, int, functions, degrees, spacing, text')
    ok = page.evaluate("""() => ['alpha','beta','gamma','delta','epsilon','zeta','eta','theta','iota','kappa','lambda','mu','nu','xi','omicron','pi','rho','sigma','tau','upsilon','phi','chi','psi','omega',
        'Gamma','Delta','Theta','Lambda','Xi','Pi','Sigma','Upsilon','Phi','Psi','Omega'].every(n => !window.renderMath('\\\\' + n, {tex: true}).includes('math-error'))""")
    check(ok, 'renderMath: every Greek letter parses')
    plain = page.evaluate("""() => ['x^2','x_t','\\\\frac{a}{b}','\\\\alpha \\\\cdot \\\\beta','a \\\\to b','a \\\\le b','x_{t+1}','x_i^2'].map(s => window.renderMath.plain('\\\\(' + s + '\\\\)'))""")
    check(plain == ['x²', 'xₜ', '(a)/(b)', 'α·β', 'a → b', 'a ≤ b', 'xₜ₊₁', 'xᵢ²'], f'plain-text math conversion {plain}')
    check(page.evaluate('window.renderMath.plain("\\\\(y_{q}\\\\)")') == 'y_q', 'plain-text subscript falls back to underscore when no glyph exists')
    mr = page.evaluate("""() => {
        const d = document.createElement('div'); d.innerHTML = window.renderMath('\\\\mathrm{H_2O}', {tex: true});
        const sub = d.querySelector('msub');
        return {msub: d.querySelectorAll('msub').length, upright: [...d.querySelectorAll('mi')].map(e => e.textContent + ':' + e.getAttribute('mathvariant')), text: d.textContent, sub: sub ? sub.children[0].textContent : null};
    }""")
    check(mr['msub'] == 1 and mr['upright'] == ['H:normal', 'O:normal'] and '_' not in mr['text'], f'renderMath: \\mathrm{{H_2O}} is an upright msub with no underscore text ({mr})')
    check('Δ' in probe(page, '\\mathrm{\\Delta G}', tex=True)['text'] and '\\' not in probe(page, '\\mathrm{\\Delta G}', tex=True)['text'], 'renderMath: \\mathrm{\\Delta G} gives Δ')
    check(probe(page, '\\text{a_b}', tex=True)['text'] == 'a_b', 'renderMath: \\text{} stays raw text')
    check(page.evaluate('[renderMath.plain("\\\\(\\\\mathrm{H_2O}\\\\)"), renderMath.plain("\\\\(\\\\mathrm{\\\\Delta G}\\\\)")]') == ['H₂O', 'ΔG'], 'plain-text math: \\mathrm{H_2O} -> H₂O, \\mathrm{\\Delta G} -> ΔG')
    sup10 = page.evaluate("""() => { const d = document.createElement('div'); d.innerHTML = window.renderMath('x^10', {tex: true}); const m = d.querySelectorAll('msup'); return {n: m.length, exp: m[0] && m[0].children[1].textContent, text: d.textContent}; }""")
    check(sup10['n'] == 1 and sup10['exp'] == '1' and sup10['text'] == 'x10', f'renderMath: x^10 follows TeX (superscript 1, then 0): {sup10}')
    deg = probe(page, '90^\\circ', tex=True)['text']
    deg2 = probe(page, '90^{\\circ}', tex=True)['text']
    comp = probe(page, 'f \\circ g', tex=True)['text']
    check(deg == '90°' and deg2 == '90°' and '∘' in comp and '°' not in comp, f'renderMath: ^\\circ is a degree sign, bare \\circ is the composition ring ({deg!r}, {deg2!r}, {comp!r})')
    check(not requests and not errors, 'math unit page: no requests, no page errors')
    context.close()

    # Hostile and broken decks
    hostile = json.dumps({'title': 'Evil', 'cards': [{'id': 'x', 'front': '<script>window.__pwned=1</script><img src=x onerror="window.__pwned=2">', 'back': '<b>bold?</b> \\(x\\)'}]}).replace('<', '\\u003c')
    context, page, errors, requests = open_page(browser, 1280, 'light', 'no-preference', variant(hostile))
    check(page.evaluate('window.__pwned') is None and page.locator('#front script, #front img').count() == 0, 'hostile card HTML is never injected')
    check('<script>window.__pwned=1</script>' in front_text(page), 'hostile card shows as visible text')
    page.locator('#show').click()
    check('<b>bold?</b>' in page.locator('#back').inner_text() and page.locator('#back b').count() == 0, 'hostile back shows as text')
    check(not requests, 'hostile deck made no requests (the escaped img never loads)')
    context.close()
    for label, deck_json in [('invalid JSON', '{not json'), ('missing cards', '{"title":"T"}'), ('every card invalid', '{"title":"T","cards":[{"front":"","back":"x"}]}')]:
        context, page, errors, requests = open_page(browser, 360, 'dark', 'reduce', variant(deck_json))
        err = page.locator('#deck-error')
        check(err.is_visible() and len(err.inner_text()) > 20 and page.locator('#app').is_hidden(), f'{label}: clear on-page error instead of a blank page')
        check(err.get_attribute('role') == 'alert' and not errors, f'{label}: error is announced and nothing threw')
        audit = page.evaluate('deckAudit()')
        check(audit['cards'] == 0 and audit['fatal'] == err.inner_text(), f'{label}: deckAudit reports the fatal error')
        context.close()

    # One bad card must not kill the deck
    mixed = make_deck([{'front': 'Q1', 'back': 'A1'}, {'front': 'Q2', 'back': ''}, {'type': 'cloze', 'front': 'The {{c1::mitochondrion}} makes ATP.', 'back': ''}, {'front': '', 'back': 'orphan'}])
    context, page, errors, requests = open_page(browser, 390, 'dark', 'reduce', variant(mixed))
    skipped = page.locator('#deck-skipped')
    check(page.locator('#app').is_visible() and page.locator('#deck-error').is_hidden() and page.locator('#browse-list li').count() == 2, 'invalid cards are skipped and the rest stay studyable')
    check(skipped.is_visible() and 'Card 2 skipped' in skipped.inner_text() and 'Card 4 skipped' in skipped.inner_text() and 'Card 3' not in skipped.inner_text(), 'non-fatal notice lists each skipped card; a cloze card with an empty back is valid')
    check('2 cards' in page.locator('#deck-meta').inner_text() and not errors, 'header counts only the valid cards and nothing threw')
    context.close()

    # Lost backslashes in the JSON are caught, not rendered as wrong math
    lost = r'{"title":"T","cards":[{"front":"\\(\frac{1}{2}\\)","back":"x"}]}'  # JSON text: \frac undoubled -> form feed
    context, page, errors, requests = open_page(browser, 390, 'light', 'reduce', variant(lost))
    msg = page.locator('#deck-error').inner_text()
    check(page.locator('#deck-error').is_visible() and 'Card 1 skipped' in msg and 'a TeX backslash was probably not doubled in the JSON' in msg and page.locator('#app').is_hidden(), f'form-feed from an undoubled \\frac is rejected with a clear error ({msg[:80]!r})')
    context.close()
    lost = r'{"title":"T","cards":[{"front":"ok","back":"fine"},{"front":"Define \\(\nu\\) here","back":"x"},{"front":"b","back":"\\(a \times b\\)"}]}'
    context, page, errors, requests = open_page(browser, 390, 'light', 'reduce', variant(lost))
    msg = page.locator('#deck-skipped').inner_text()
    check('Card 2 skipped' in msg and 'Card 3 skipped' in msg and 'a TeX backslash was probably not doubled' in msg and page.locator('#browse-list li').count() == 1, f'newline (\\nu) inside inline math and tab (\\times) are rejected per card ({msg[:60]!r})')
    context.close()

    # Stable ids: inserting a card at index 0 keeps schedules on the same fronts
    path = Path(tempfile.mkdtemp(prefix='deck-ids-')) / 'deck.html'
    base = [{'front': 'Alpha question', 'back': 'a'}, {'front': 'Beta question', 'back': 'b'}, {'front': 'Gamma question', 'back': 'c'}]
    url = variant(make_deck(base), into=path)
    context, page, errors, requests = open_page(browser, 1280, 'light', 'no-preference', url)
    page.locator('#show').click()
    page.locator('#rate-good').click()
    before_ids = page.evaluate("() => { const o = JSON.parse(localStorage.getItem('myelinate-deck:|T')); return Object.keys(o.cards); }")
    check(len(before_ids) == 1 and not any(i in ('c1', 'c2', 'c3') for i in before_ids), f'ids come from the front text, not position ({before_ids})')
    variant(make_deck([{'front': 'Inserted question', 'back': 'z'}] + base), into=path)
    page.reload()
    check('Inserted question' in front_text(page) and 'Due today: 3' in page.locator('#due-count').inner_text(), 'after inserting a card at index 0, the reviewed card is still the one scheduled (Alpha not due, the new card due first)')
    page.locator('#mode-browse').click()
    check(page.evaluate("() => Object.keys(JSON.parse(localStorage.getItem('myelinate-deck:|T')).cards)") == before_ids, 'saved schedule keys are unchanged by the insert')
    context.close()
    # Old storage key (title only) is still read once
    legacy = make_deck(base)
    context, page, errors, requests = open_page(browser, 1280, 'light', 'no-preference', variant(legacy))
    first_id = before_ids[0]
    page.evaluate("([k, id]) => { localStorage.setItem(k, JSON.stringify({v: 1, cards: {[id]: {interval: 3, due: Date.now() + 86400000, reps: 1}}})); }", ['myelinate-deck:T', first_id])
    page.reload()
    check('Due today: 2' in page.locator('#due-count').inner_text(), 'progress saved under the old title-only key is still read')
    context.close()

    # Exports: hints, cloze brace guard, MathML-free text
    exp = make_deck([{'id': 'b1', 'front': 'Water?', 'back': '\\(\\mathrm{H_2O}\\)', 'hint': 'Think <b>two</b> hydrogens \\(x^2\\)'},
                     {'id': 'c1', 'type': 'cloze', 'front': '{{c1::\\(\\sqrt{\\frac{a}{b}}\\)}} is a root', 'back': '', 'hint': 'a over b'}])
    context, page, errors, requests = open_page(browser, 1280, 'light', 'no-preference', variant(exp))
    anki = page.evaluate('window.deckExports.anki()')
    cloze = page.evaluate('window.deckExports.ankiCloze()')
    quizlet = page.evaluate('window.deckExports.quizlet()')
    check('<br><i>Hint: Think &lt;b&gt;two&lt;/b&gt; hydrogens \\(x^2\\)</i>' in anki, 'Anki basic export appends the hint, escaped except its math')
    check('<i>Hint: a over b</i>' in cloze, 'Anki cloze export carries the hint')
    check('H₂O (Hint: Think <b>two</b> hydrogens x²)' in quizlet, 'Quizlet export appends the hint and writes H₂O')
    check('{{c1::\\(\\sqrt{\\frac{a}{b} }\\)}}' in cloze and '}}\\)' not in cloze, 'Anki cloze export turns TeX "}}" into "} }" so the cloze does not end early')
    check(not errors, 'export deck: nothing threw')
    context.close()

    # ---- Follow-up fixes from issue #21 ------------------------------------------
    def one(deck_json, width=1280, **kw):
        ctx = browser.new_context(viewport={'width': width, 'height': 900}, **kw)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda error: errs.append(str(error)))
        return ctx, pg, errs

    def tstore(pg, key='myelinate-deck:|T'):
        return pg.evaluate("k => JSON.parse(localStorage.getItem(k) || 'null')", key)

    # 1 escaped dollar in cloze and in math, across render, browse and all exports
    dl = make_deck([{'id': 'd1', 'type': 'cloze', 'front': 'Price is {{c1::\\$5}} today', 'back': 'It costs \\(\\$5\\) in total.'}])
    ctx, pg, errs = one(dl)
    pg.goto(variant(dl))
    pg.locator('#show').click()
    check('Price is $5 today' in pg.locator('#back').text_content() and 'costs $5 in' in pg.locator('#back').text_content(), 'escaped dollar: revealed cloze and \\(\\$5\\) show $5')
    pg.locator('#mode-browse').click()
    bt = pg.locator('#browse-list').text_content()
    check('Price is $5 today' in bt and 'costs $5 in' in bt, 'escaped dollar: browse shows $5')
    qz, ak, akc = pg.evaluate('[deckExports.quizlet(), deckExports.anki(), deckExports.ankiCloze()]')
    check('Price is $5 today' in qz and '$5 in total' in qz and not re.search('[\ue000-\uf8ff]', qz), 'escaped dollar: Quizlet export has $5 and no private-use glyphs')
    check('{{c1::$5}}' in akc and not re.search('[\ue000-\uf8ff]', akc + ak), 'escaped dollar: Anki cloze keeps {{c1::$5}}')
    r = probe(pg, '\\(\\$5\\)')
    check(r['text'] == '$5' and r['math'] == 1, 'escaped dollar inside inline math renders $5')
    check(not errs, 'escaped dollar: nothing threw')
    ctx.close()

    # 2 Again on a not-due card applies the lapse
    now_ms = int(__import__('time').time() * 1000)
    ag = make_deck([{'id': 'a', 'front': 'Q', 'back': 'A'}])
    ctx, pg, errs = one(ag)
    pg.goto(variant(ag))
    pg.evaluate("([k, n]) => localStorage.setItem(k, JSON.stringify({v: 1, cards: {a: {interval: 30, due: n + 30 * 86400000, reps: 4}}}))", ['myelinate-deck:|T', now_ms])
    pg.reload()
    pg.locator('#show').click()
    pg.locator('#rate-again').click()
    s = tstore(pg)['cards']['a']
    check(s['interval'] == 0 and 9 * 60000 < s['due'] - s['last'] <= 10 * 60000, f'Again on a not-due card lapses it to interval 0, due in 10 minutes ({s})')
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check(tstore(pg)['cards']['a']['interval'] == 1, 'a lapsed card is live for the rest of the session (Good then climbs to 1 day)')
    ctx.close()

    # 3 Calendar-day scheduling
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    tz = ZoneInfo('America/Chicago')
    t0 = datetime(2026, 11, 3, 8, 5, tzinfo=tz)
    t0ms = int(t0.timestamp() * 1000)
    rollover = int(datetime(2026, 11, 4, 4, 0, tzinfo=tz).timestamp() * 1000)
    cd = make_deck([{'id': 'a', 'front': 'Q', 'back': 'A'}])
    ctx, pg, errs = one(cd, timezone_id='America/Chicago')
    pg.clock.set_fixed_time(t0)
    pg.goto(variant(cd))
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check(tstore(pg)['cards']['a']['due'] == rollover, 'Good schedules 04:00 local of the scheduling day + 1')
    pg.clock.set_fixed_time(t0 + timedelta(minutes=1))
    pg.reload()
    check('Due today: 0' in pg.locator('#due-count').inner_text(), 'a card rated Good is not due again later the same day')
    pg.clock.set_fixed_time(t0 + timedelta(days=1) - timedelta(minutes=10))
    pg.reload()
    check('Due today: 1' in pg.locator('#due-count').inner_text(), 'next morning at 07:55 the card is already due')
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check(tstore(pg)['cards']['a']['interval'] == 3, 'the card is live: rating it next morning climbs the ladder (1 -> 3)')
    ctx.close()

    # 3b day rollover at 04:00: 23:55 Good, 00:05 next day is still the same scheduling day
    late = datetime(2026, 11, 3, 23, 55, tzinfo=tz)
    ctx, pg, errs = one(cd, timezone_id='America/Chicago')
    pg.clock.set_fixed_time(late)
    pg.goto(variant(cd))
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check(tstore(pg)['cards']['a']['due'] == rollover, 'Good at 23:55 is due at 04:00 the next day')
    pg.clock.set_fixed_time(late + timedelta(minutes=10))
    pg.reload()
    check('Due today: 0' in pg.locator('#due-count').inner_text() and pg.locator('#card').is_hidden() is False, 'at 00:05 next day the card is not due yet (Due today 0)')
    check(pg.evaluate("() => document.querySelector('#progress').textContent").startswith('Card 1 of 1'), 'at 00:05 the card is only in the practice queue')
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check(tstore(pg)['cards']['a']['interval'] == 1, 'at 00:05 the card is not live: practice leaves its interval alone')
    pg.clock.set_fixed_time(late + timedelta(hours=8))
    pg.reload()
    check('Due today: 1' in pg.locator('#due-count').inner_text(), 'at 07:55 next day the card is due')
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check(tstore(pg)['cards']['a']['interval'] == 3, 'at 07:55 next day the card is live (1 -> 3)')
    ctx.close()

    # 4 newline in display math
    dm = make_deck([{'id': 'a', 'front': 'Q1', 'back': '\\[a \ne b\\]'}, {'id': 'b', 'front': 'Q2', 'back': '\\[a\n= b\\]'},
                    {'id': 'c', 'front': 'Q3', 'back': '\\[\nabla f\\]'}, {'id': 'd', 'front': 'Q4', 'back': '\\[a\n 2 + b\\]'}])
    ctx, pg, errs = one(dm)
    pg.goto(variant(dm))
    sk = pg.locator('#deck-skipped').inner_text()
    check('Card 3 skipped' in sk and 'Card 1' not in sk and 'Card 2' not in sk and 'Card 4' not in sk and pg.locator('#browse-list li').count() == 3, f'a lost long command (\\nabla) in display math is skipped; a one-letter stem or operator line loads ({sk[:50]!r})')
    w = pg.evaluate('deckAudit()')['possibleLostBackslash']
    check([x['card'] for x in w] == ['a'], f'display line starting with "e" is reported as a possible lost \\ne, not skipped ({w})')
    ctx.close()

    # 4e (#23) display math starting with a variable e or u; lost backslashes after a tab or CR; code cards in deckAudit
    ex = make_deck([{'id': 'grow', 'front': 'Q', 'back': '\\[\ne^{rt}\n\\]'}, {'id': 'kin', 'front': 'Q', 'back': '\\[\nu = v - at\n\\]'},
                    {'id': 'bf', 'front': 'Q', 'back': '\\(\textbf{F} = m\\)'}, {'id': 'times', 'front': 'Q', 'back': '3 \times 4 = 12'},
                    {'id': 'arrow', 'front': 'Q', 'back': 'A \rightarrow B'}, {'id': 'code', 'front': 'What does \\n do in a Python string?', 'back': 'Starts a new line; C:\\Users and \\d+ are fine too.'},
                    {'id': 'tsv', 'front': 'Term', 'back': 'Producer:\tan organism that makes its own food'}])
    ctx, pg, errs = one(ex)
    pg.goto(variant(ex))
    sk = pg.locator('#deck-skipped').inner_text()
    a = pg.evaluate('deckAudit()')
    ids = [c for c in ['grow', 'kin', 'times', 'arrow', 'code', 'tsv']]
    check('Card 3 skipped' in sk and 'tab or carriage return before a letter inside math' in sk and sk.count('skipped') == 1, f'a lost \\textbf (tab + "extbf") inside math is skipped, nothing else ({sk[:80]!r})')
    check(pg.locator('#browse-list li').count() == 6 and not errs, 'e^{rt} and u = v - at on their own display lines load')
    warned = sorted(x['card'] for x in a['possibleLostBackslash'])
    check(warned == ['arrow', 'grow', 'kin', 'times', 'tsv'], f'one-letter display stems and tab/CR before a command name outside math are warnings ({warned})')
    check(a['rawTeX'] == [], f'a code card with \\n, C:\\Users and \\d+ is not reported as raw TeX ({a["rawTeX"]})')
    ctx.close()

    # 4b display math on its own lines loads; a lost stem is caught from the engine's own tables
    own = r'{"title":"T","cards":[{"front":"Q1","back":"\\[\nE = mc^2\n\\]"},{"front":"Q2","back":"\\[\nx^2\n\\]"},{"front":"Q3","back":"\\(a\n+ b\\)"},{"front":"Q4","back":"\\[a \neq b\\]"},{"front":"Q5","back":"\\[\nabla f\\]"},{"front":"Q6","back":"\\(a \neq b\\)"},{"front":"Q7","back":"\\(\notin S\\)"},{"front":"Q8","back":"$x\nu y$"}]}'
    ctx, pg, errs = one(own)
    pg.goto(variant(own))
    sk = pg.locator('#deck-skipped').inner_text()
    check(pg.locator('#browse-list li').count() == 3 and not any(f'Card {k} ' in sk for k in (1, 2, 3)), f'display math on its own lines and a plain line break in inline math load ({sk[:80]!r})')
    check(all(f'Card {k} skipped' in sk for k in (4, 5, 6, 7, 8)), f'lost-stem newlines (\\ne, \\nabla, \\neq, \\notin, \\nu) are skipped ({sk[:80]!r})')
    check(re.search(r'Card 4 skipped: "back" has a line break before a command name inside display math', sk) and re.search(r'Card 6 skipped: "back" has a line break before a command name inside inline math', sk), 'display math has its own skip message, inline keeps "inline math"')
    ctx.close()

    # 4c lost tab backslash: stems come from the engine's tables (\therefore)
    tt = r'{"title":"T","cards":[{"front":"ok","back":"fine"},{"front":"Q2","back":"\\(a \therefore b\\)"},{"front":"Q3","back":"\\(a\t+ b\\)"}]}'
    ctx, pg, errs = one(tt)
    pg.goto(variant(tt))
    sk = pg.locator('#deck-skipped').inner_text()
    check('Card 2 skipped' in sk and 'tab or carriage return before a letter inside math' in sk and 'Card 3' not in sk and pg.locator('#browse-list li').count() == 2, f'undoubled \\therefore (tab + "herefore") is skipped, a plain tab is not ({sk[:60]!r})')
    ctx.close()
    # 4d lost CR backslash (\rho): checked before CRLF normalization; a CRLF study guide still loads
    rr = r'{"title":"T","cards":[{"front":"ok","back":"fine"},{"front":"Q2","back":"\\(\rho = m/V\\)"},{"front":"Q3","back":"line one\r\nline two \\(x\\)"}]}'
    ctx, pg, errs = one(rr)
    pg.goto(variant(rr))
    sk = pg.locator('#deck-skipped').inner_text()
    check('Card 2 skipped' in sk and 'tab or carriage return before a letter inside math' in sk and 'Card 3' not in sk and pg.locator('#browse-list li').count() == 2, f'undoubled \\rho (CR + "ho") is skipped, CRLF text is not ({sk[:60]!r})')
    ctx.close()

    # 5 template comment gives one escaping rule
    cm = re.search(r'<!-- To make a deck.*?-->', TEMPLATE.read_text(encoding='utf-8'), re.S).group(0)
    check('"</"' not in cm and 'every "<"' in cm, 'template comment names one rule: replace every "<"')

    # 6 CRLF, lone CR and tabs
    cr = make_deck([{'id': 'a', 'front': 'Q\ta\tb', 'back': 'line one\r\nline two\rline three'}, {'id': 'b', 'front': 'Q2', 'back': '\\(a\t+ b\\)'}, {'id': 'c', 'front': 'Q3', 'back': '\\(a \times b\\)'}])
    ctx, pg, errs = one(cr)
    pg.goto(variant(cr))
    sk = pg.locator('#deck-skipped').inner_text()
    check(pg.locator('#browse-list li').count() == 2 and 'Card 3 skipped' in sk and 'Card 1' not in sk and 'Card 2 ' not in sk, f'CRLF and a plain tab load; a tab before a TeX stem inside math is rejected ({sk[:60]!r})')
    pg.locator('#show').click()
    check(pg.locator('#back br').count() == 2 and pg.locator('#back').inner_text().split('\n')[:3] == ['line one', 'line two', 'line three'], 'CRLF back renders as separate lines')
    check('Q a b' in front_text(pg), 'a tab between words becomes a space')
    ctx.close()

    # 7 ids that collide with Object.prototype
    pr = make_deck([{'id': 'constructor', 'front': 'Q1', 'back': 'A1'}, {'id': '__proto__', 'front': 'Q2', 'back': 'A2'}, {'id': 'toString', 'front': 'Q3', 'back': 'A3'}])
    ctx, pg, errs = one(pr)
    pg.goto(variant(pr))
    rate_through(pg, 'good', 3)
    st = pg.evaluate("k => { const c = JSON.parse(localStorage.getItem(k)).cards; return Object.keys(c).sort().map(i => i + ':' + c[i].interval); }", 'myelinate-deck:|T')
    check(st == ['__proto__:1', 'constructor:1', 'toString:1'], f'ids constructor, __proto__ and toString are saved ({st})')
    pg.reload()
    check('Due today: 0' in pg.locator('#due-count').inner_text() and not errs, 'those ids reload as scheduled, not due')
    ctx.close()

    # 8 and 9 extra commands, function application, text spacing
    ctx, pg, errs = one(None)
    pg.goto(URL)
    def tex(s):
        return pg.evaluate("""s => { const d = document.createElement('div'); d.innerHTML = window.renderMath(s, {tex: true});
            return {err: d.querySelectorAll('.math-error').length, text: d.textContent, html: d.innerHTML, alt: (d.querySelector('math') || {getAttribute: () => ''}).getAttribute('alttext')}; }""", s)
    for cmd in ['\\vec{F}', '\\mathbf{v}', '\\hbar', "f'(x)", '\\prime', '\\lim_{x\\to 0} f(x)', '\\displaystyle \\frac{a}{b}', '\\dot{x}', '\\ddot{x}', '\\tilde{x}',
                'a \\longrightarrow b', 'a \\Longrightarrow b', 'a \\iff b', 'a \\implies b', 'a \\mid b', 'a \\ldots b \\cdots c \\dots', '\\binom{n}{k}']:
        check(tex(cmd)['err'] == 0, f'renders without error: {cmd}')
    check(re.search(r'<mover accent="true">.*<mi>F</mi>.*<mo>→</mo></mover>', tex('\\vec{F}')['html']), '\\vec puts U+2192 over the base')
    bold = pg.evaluate("""() => {
        const box = document.createElement('div'); box.style.fontSize = '32px';
        box.innerHTML = renderMath('\\\\mathbf{v} \\\\mathbf{V12\\\\alpha\\\\Omega} v', {tex: true});
        document.body.append(box);
        const mi = [...box.querySelectorAll('mi')];
        const out = {cp: [...mi[0].textContent].map(c => c.codePointAt(0).toString(16)), all: [...box.querySelectorAll('mi, mn')].map(e => [...e.textContent].map(c => c.codePointAt(0).toString(16)).join(' ')),
                     bw: mi[0].getBoundingClientRect().width, pw: mi[mi.length - 1].getBoundingClientRect().width, mv: mi[0].getAttribute('mathvariant'), html: box.innerHTML};
        box.remove(); return out; }""")
    check(bold['cp'] == ['1d42f'] and bold['mv'] == 'normal' and 'bold' not in bold['html'].replace('mathbf', ''), f'\\mathbf{{v}} is U+1D42F with mathvariant normal ({bold["cp"]})')
    check(bold['all'][1:5] == ['1d415', '1d7cf 1d7d0', '1d6c2', '1d6c0'], f'\\mathbf maps capitals, digits, Greek lowercase and capitals ({bold["all"]})')
    check(abs(bold['bw'] - bold['pw']) > 0.5, f'\\mathbf{{v}} is a different glyph from plain italic v (width {bold["bw"]:.2f} vs {bold["pw"]:.2f})')
    check(page_plain_bold(pg), 'Quizlet plain text for \\mathbf stays ASCII')
    check('ℏ' in tex('\\hbar')['text'] and '′' in tex("f'")['text'] and '′' in tex('\\prime')['text'], '\\hbar and prime')
    check('<munder><mo movablelimits="true">lim</mo>' in tex('\\lim_{x\\to 0} f')['html'], '\\lim puts its limit underneath')
    check('linethickness="0"' in tex('\\binom{n}{k}')['html'] and tex('\\binom{n}{k}')['text'].count('(') + tex('\\binom{n}{k}')['text'].count(')') == 2, '\\binom is a rule-less fraction in parentheses')
    check(tex('\\ce{H2O}')['err'] == 1 and tex('\\begin{pmatrix}a\\end{pmatrix}')['err'] == 1, '\\ce and environments stay unsupported errors')
    gap = pg.evaluate("""() => {
        const box = document.createElement('div'); box.style.fontSize = '32px';
        box.innerHTML = renderMath('\\\\ln x', {tex: true}); document.body.append(box);
        const [a, b] = box.querySelectorAll('mi');
        const out = {gap: b.getBoundingClientRect().left - a.getBoundingClientRect().right, fs: parseFloat(getComputedStyle(box.querySelector('math')).fontSize)};
        box.remove(); return out; }""")
    check(gap['gap'] > 0.1 * gap['fs'], f'rendered: gap between "ln" and "x" is {gap["gap"]:.2f}px > 0.1em ({0.1 * gap["fs"]:.2f}px)')
    check('\u2061' in tex('\\sin\\theta')['html'] and '\u2061' in tex('\\lim_{x\\to 0} f')['html'], 'function names emit function application (U+2061)')
    check('\u2061' not in tex('\\ln(x)')['html'], 'no function application mo in \\ln(x)')
    check(tex('\\text{ 5 }')['text'] == '\u00a05\u00a0' and tex('5\\text{ mL}')['text'] == '5\u00a0mL', '\\text keeps leading and trailing spaces as no-break spaces')
    check(not errs, 'extra commands: nothing threw')
    ctx.close()

    # 10 done screen tells the truth about saving
    ds = make_deck([{'id': 'a', 'front': 'Q', 'back': 'A'}])
    ctx, pg, errs = one(ds)
    pg.goto(variant(ds))
    pg.evaluate("k => localStorage.setItem(k, JSON.stringify({v: 1, cards: {a: {interval: 7, due: 1, reps: 1}}}))", 'myelinate-deck:|T')
    pg.reload()
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    check('next review dates are saved' in pg.locator('#done-text').inner_text(), 'done screen: live rating -> dates saved')
    pg.locator('#again-session').click()
    pg.locator('#show').click()
    pg.locator('#rate-good').click()
    dt = pg.locator('#done-text').inner_text()
    check('Practice only: no review dates changed.' in dt and 'saved' not in dt, 'done screen: practice-only session says nothing was changed')
    ctx.close()
    ctx, pg, errs = one(ds)
    pg.add_init_script("Storage.prototype.setItem = () => { throw new Error('quota'); }")
    pg.goto(variant(ds))
    rate_through(pg, 'good', 3)
    dt = pg.locator('#done-text').inner_text()
    check("Review dates were updated but couldn't be saved in this browser; they reset when you close the page." in dt and 'are saved' not in dt and 'Practice only' not in dt, f'done screen: failed save says dates could not be saved ({dt!r})')
    ctx.close()

    # deckAudit
    ctx, pg, errs = one(None)
    pg.goto(URL)
    a = pg.evaluate('deckAudit()')
    check(a['cards'] == 8 and a['skipped'] == [] and a['mathErrors'] == [] and a['rawTeX'] == [], f'deckAudit on the example deck: 8 cards, 0 errors, no raw TeX ({a})')
    ctx.close()
    ad = make_deck([{'id': 'ok', 'front': 'Fine \\(x^2\\)', 'back': 'yes'}, {'id': 'chem', 'front': 'Water', 'back': '\\(\\ce{H2O}\\)'}, {'id': 'bad', 'front': '', 'back': 'x'}])
    ctx, pg, errs = one(ad)
    pg.goto(variant(ad))
    a = pg.evaluate('deckAudit()')
    check(a['cards'] == 2 and len(a['skipped']) == 1 and len(a['mathErrors']) == 1 and a['mathErrors'][0]['card'] == 'chem' and '\\ce{H2O}' in a['mathErrors'][0]['source'], f'deckAudit lists the \\ce error and skipped card ({a})')
    check(a['rawTeX'] == [], f'deckAudit: rendered \\ce error is reported under mathErrors only ({a["rawTeX"]})')
    ctx.close()
    rt = make_deck([{'id': 'nodelim', 'front': 'Q1', 'back': '\\frac{a}{b}'}, {'id': 'noclose', 'front': 'Q2', 'back': '\\(x^2'}, {'id': 'fine', 'front': 'Q3', 'back': 'plain \\(x^2\\) and $y_{1}$ and \\$5'}])
    ctx, pg, errs = one(rt)
    pg.goto(variant(rt))
    a = pg.evaluate('deckAudit()')
    got = {(r['card'], r['field']): r['rawTeX'] for r in a['rawTeX']}
    check(set(got) == {('nodelim', 'back'), ('noclose', 'back')} and '\\frac{a}{b}' in got[('nodelim', 'back')] and '\\(x^2' in got[('noclose', 'back')] and a['mathErrors'] == [], f'deckAudit reports TeX outside math in rawTeX ({a})')
    ctx.close()
    browser.close()
print('PASS: flashcards journey complete')
