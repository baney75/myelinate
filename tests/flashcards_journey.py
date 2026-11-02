#!/usr/bin/env python3
"""Open the flashcard deck template offline and check study flow, math rendering, exports and layout."""
import json
import re
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

TEMPLATE = Path(__file__).resolve().parents[1] / 'templates' / 'flashcards-deck.html'
URL = TEMPLATE.as_uri()
SHOTS = Path('/tmp/deck-shots')
SHOTS.mkdir(exist_ok=True)
KEY = 'myelinate-deck:Example Deck'


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print('PASS:', message)


def variant(deck_json):
    """Write a copy of the template with different deck JSON and return its file URL."""
    html = TEMPLATE.read_text()
    html = re.sub(r'(<script type="application/json" id="deck">).*?(</script>)', lambda m: m.group(1) + deck_json + m.group(2), html, count=1, flags=re.S)
    path = Path(tempfile.mkdtemp(prefix='deck-variant-')) / 'deck.html'
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
        check(page.locator('#front math').count() == 0 and page.locator('#front').inner_text().count('\\') == 0, f'{tag} front has no raw backslashes')

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
        check(anki.startswith('#separator:tab\n#html:true\n#tags column:3\n'), f'{tag} Anki export starts with #separator:tab')
        check('\\(p^2\\)' in anki and '\\[p^2 + 2pq + q^2 = 1\\]' in anki, f'{tag} Anki export keeps MathJax delimiters')
        check(all(len(ln.split('\t')) == 3 for ln in anki.split('\n')[3:] if ln) and 'Population_genetics' in anki, f'{tag} Anki rows have front, back, tags')
        check('{{c1::' not in anki, f'{tag} cloze card kept out of the basic Anki file')
        cloze = page.evaluate('window.deckExports.ankiCloze()')
        check(cloze.startswith('#separator:tab\n#html:true\n#notetype:Cloze\n') and '{{c1::very large}}' in cloze and '{{c2::genetic drift}}' in cloze, f'{tag} cloze Anki file has #notetype:Cloze and cloze markers')
        with page.expect_download() as info:
            page.locator('#export-quizlet').click()
        check(info.value.suggested_filename == 'example-deck-quizlet.txt', f'{tag} Quizlet download filename from title')
        with page.expect_download() as info:
            page.locator('#export-anki-cloze').click()
        check(info.value.suggested_filename == 'example-deck-anki-cloze.txt', f'{tag} cloze download filename from title')

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
    check(r['msup'] == 2 or r['msup'] >= 1, 'renderMath: p^2 + 2pq + q^2 = 1 has msup')
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
    check(probe(page, '\\overline{x} \\bar{y} \\hat{z} \\sum_{i=1}^{n} x_i \\int_0^1 f \\partial \\ln x \\sin\\theta 90^\\circ 5\\% \\,\; \\quad \\text{rate} \\mathrm{kg}', tex=True)['error'] == 0, 'renderMath: overline, bar, hat, sum, int, functions, degrees, spacing, text')
    ok = page.evaluate("""() => ['alpha','beta','gamma','delta','epsilon','zeta','eta','theta','iota','kappa','lambda','mu','nu','xi','omicron','pi','rho','sigma','tau','upsilon','phi','chi','psi','omega',
        'Gamma','Delta','Theta','Lambda','Xi','Pi','Sigma','Upsilon','Phi','Psi','Omega'].every(n => !window.renderMath('\\\\' + n, {tex: true}).includes('math-error'))""")
    check(ok, 'renderMath: every Greek letter parses')
    plain = page.evaluate("""() => ['x^2','x_t','\\\\frac{a}{b}','\\\\alpha \\\\cdot \\\\beta','a \\\\to b','a \\\\le b','x_{t+1}','x_i^2'].map(s => window.renderMath.plain('\\\\(' + s + '\\\\)'))""")
    check(plain == ['x²', 'xₜ', '(a)/(b)', 'α·β', 'a → b', 'a ≤ b', 'xₜ₊₁', 'xᵢ²'], f'plain-text math conversion {plain}')
    check(page.evaluate('window.renderMath.plain("\\\\(y_{q}\\\\)")') == 'y_q', 'plain-text subscript falls back to underscore when no glyph exists')
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
    for label, deck_json in [('invalid JSON', '{not json'), ('missing cards', '{"title":"T"}'), ('empty card', '{"title":"T","cards":[{"front":"","back":"x"}]}')]:
        context, page, errors, requests = open_page(browser, 360, 'dark', 'reduce', variant(deck_json))
        err = page.locator('#deck-error')
        check(err.is_visible() and len(err.inner_text()) > 20 and page.locator('#app').is_hidden(), f'{label}: clear on-page error instead of a blank page')
        check(err.get_attribute('role') == 'alert' and not errors, f'{label}: error is announced and nothing threw')
        context.close()
    browser.close()
print('PASS: flashcards journey complete')
