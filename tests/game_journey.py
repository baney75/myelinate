#!/usr/bin/env python3
"""Open the exam game template offline and play it: gate, stages, misses, retests, mock, delayed recheck, audit, layout."""
import json
import re
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

TEMPLATE = Path(__file__).resolve().parents[1] / 'templates' / 'exam-game.html'


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print('PASS:', message)


def variant(mutate):
    html = TEMPLATE.read_text()
    block = re.search(r'(<script type="application/json" id="game">)(.*?)(</script>)', html, re.S)
    data = json.loads(block.group(2))
    mutate(data)
    text = json.dumps(data).replace('<', '\\u003c')
    html = html[:block.start(2)] + text + html[block.end(2):]
    path = Path(tempfile.mkdtemp(prefix='game-')) / 'game.html'
    path.write_text(html)
    return path.as_uri()


def open_page(browser, url, width=1000, scheme='light'):
    context = browser.new_context(viewport={'width': width, 'height': 860}, color_scheme=scheme)
    outside = []

    def handle(route):
        if route.request.url.startswith('file://'):
            route.continue_()
        else:
            outside.append(route.request.url)
            route.abort()

    context.route('**/*', handle)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(url)
    return page, errors, outside


def card(page):
    return page.evaluate("""() => { const c = __game.card; if (!c) return null;
      return {id: c.id, type: c.type, answer: c.answer, answers: c.answers, rhs: c.f && c.f.rhs, model: c.model}; }""")


def right(page, c):
    if c['type'] == 'sort':
        page.keyboard.press(str(c['answer'] + 1))
        return
    value = {'formula': c['rhs'], 'term': (c['answers'] or [''])[0], 'num': str(c['answer']), 'free': (c['model'] or '').replace('$', '')}[c['type']]
    page.fill('#ans', value)
    page.keyboard.press('Enter')


def wrong(page, c):
    if c['type'] == 'sort':
        page.keyboard.press(str((c['answer'] + 1) % 3 + 1))
    else:
        page.fill('#ans', '99999' if c['type'] == 'num' else 'zzz')
        page.keyboard.press('Enter')


def play_stage(page, limit=120):
    """Answer until the result screen, answering everything right."""
    for _ in range(limit):
        if page.locator('.fb.ok').count():
            page.keyboard.press('Enter')
            page.wait_for_timeout(180)
            if page.locator('.fb.ok').count():
                page.wait_for_timeout(1400)
            continue
        if page.evaluate('__game.view') != 'play':
            return
        c = card(page)
        right(page, c)
        page.wait_for_timeout(170)
    raise AssertionError('stage did not finish')


def learn_all(page):
    while page.evaluate('__game.view') in ('home', 'learn'):
        if page.evaluate('__game.view') == 'home':
            page.click('#go')
            continue
        typed = page.evaluate("document.querySelector('.hero').textContent")
        check(typed, 'learn screen shows the formula')
        text = page.evaluate("JSON.parse(document.getElementById('game').textContent).formulas.filter(f=>f.tier==='memorize')[+document.querySelector('.label').textContent.match(/Learn (\\d+)/)[1]-1].rhs")
        page.fill('#ans', text)
        page.keyboard.press('Enter')


def exam_all(page):
    while page.evaluate('__game.view') == 'exam':
        right(page, card(page))
        page.wait_for_timeout(40)


with sync_playwright() as p:
    browser = p.chromium.launch()
    url = TEMPLATE.as_uri()
    page, errors, outside = open_page(browser, url)

    audit = page.evaluate('gameAudit()')
    check(audit['ok'], f'the example passes gameAudit: {audit}')
    check(page.locator('#mockB').is_disabled(), 'the mock stays locked before the gate')
    check(page.locator('.st[data-t="basics"]').is_disabled(), 'topics stay locked before the gate')
    check('readiness' not in page.inner_text('body').lower(), 'home shows no readiness claim')
    check('of' in page.inner_text('.bignum'), 'home shows items cleared as counts')

    # typed input
    ok = page.evaluate("""() => { const g = __game; return {
      deltaOk: g.checkFormula('Δx/Δt', ['Δx/Δt']), deltaWord: g.checkFormula('delta x/delta t', ['Δx/Δt']), deltaInverted: !g.checkFormula('Δt/Δx', ['Δx/Δt']), deltaProduct: !g.checkFormula('x t', ['Δx/Δt']), dNdt: g.checkFormula('dN/dt', ['dN/dt']), dNdtInverted: !g.checkFormula('dt/dN', ['dN/dt']), piJoined: g.checkFormula('2pi r', ['2 π r']), piSquare: g.checkFormula('4pi r^2', ['4 π r^2']), muSub: g.checkFormula('mu_0 I', ['μ_0 I']), piValue: Math.abs(g.evalExpr('2pi') - 6.2832) < 0.001, domainSE: g.checkFormula('sqrt(p*(1-p)/n)', ['sqrt(p(1-p)/n)']), domainGamma: g.checkFormula('sqrt(1-v^2/c^2)', ['sqrt(1-v^2/c^2)']), domainLn: g.checkFormula('ln(1-p)', ['ln(1-p)']), domainWrong: !g.checkFormula('sqrt(1-v^2/c)', ['sqrt(1-v^2/c^2)']), domainWrong2: !g.checkFormula('ln(1+p)', ['ln(1-p)']), plain: g.checkFormula('V = I*R', ['IR']), lower: g.checkFormula('i r', ['IR']), notInverse: !g.checkFormula('I/R', ['IR']),
      lambda: g.checkFormula('N0 lambda^t', ['N_0 λ^t']), sub: g.checkFormula('n_0 R^t', ['N_0 R^t']),
      caseMatters: !g.checkFormula('N_0 r^t', ['N_0 R^t'], true), sum: g.checkFormula('sum l_x m_x', ['Σ l_x m_x']),
      commute: g.checkFormula('e^(r t) N_0', ['N_0 e^(rt)']), groupKept: !g.checkFormula('K-N/K', ['(K-N)/K']), group2: !g.checkFormula('a+b/c', ['(a+b)/c']),
      group3: !g.checkFormula('2^n-1', ['2^(n-1)']), frac: g.checkFormula('(M*C)/R', ['M C/R']), brace: g.checkFormula('e^{rt}', ['e^(r t)']),
      subPlus: g.checkFormula('n_{x+1}/n_x', ['n_{x+1}/n_x']), pi: g.checkFormula('pi r^2', ['π r^2']), empty: !g.checkFormula('', ['IR']),
      typo: g.checkTerm('semelparus', ['semelparous']), wrong: !g.checkTerm('voltage', ['current']), article: g.checkTerm('the current', ['current']),
      opposite: !g.checkTerm('hyperglycemia', ['hypoglycemia']), afferent: !g.checkTerm('efferent', ['afferent']), ketone: !g.checkTerm('ketone', ['ketose']),
      alpha: !g.checkTerm('alpha helix', ['beta helix']), near: !g.checkTerm('coronal', ['coronary'], ['coronal']), vitamin: !g.checkTerm('vitamin', ['vitamin a']),
      setup: Math.abs(g.evalExpr('300*e^(0.229*6)') - 1185.34) < .01, comma: g.evalExpr('1,186') === 1186, implicit: g.evalExpr('2(3+1)') === 8,
      junk: g.evalExpr('abc') === null, code: g.evalExpr('alert(1)') === null, sci: g.evalExpr('2e3') === 2000, sci2: Math.abs(g.evalExpr('1.2x10^3') - 1200) < 1e-9,
      eKept: Math.abs(g.evalExpr('2e^3') - 40.17) < .01, unit: g.readNum('40 V').v === 40, money: g.readNum('$40').v === 40, none: g.readNum('2*') === null,
      small: g.fmt(0.00042) === '0.00042', small2: g.fmt(0.0123) === '0.0123', big: g.fmt(1186.4) === '1,186' }; }""")
    ok = {k: v for k, v in ok.items() if not v}
    check(not ok, f'formula, term and number checks behave: {ok}')
    deriv = page.evaluate("__game.mathHTML('dN/dt = rN')")
    check(deriv.index('frac') < deriv.index('dt') and 'dt</span></span>' in deriv, 'dN/dt renders as one fraction')
    html = page.evaluate("__game.mathHTML('N_t = K N_0/(N_0+(K-N_0)e^(-r t))')")
    check('frac' in html and '<sub>' in html and '<sup>' in html and '−' in html, 'a typed fraction with exponent renders as math')
    check('frac' in page.evaluate("__game.mathHTML('n_{t+1}/n_t')"), 'braced subscripts render')
    for partial in ('(', 'a/', 'x^', 'n_', 'e^(', ')', '/', '^^'):
        page.evaluate('s => __game.mathHTML(s)', partial)
    check(True, 'half-typed math never throws')
    check('<' not in re.sub(r'</?(span|sub|sup)[^>]*>', '', page.evaluate("__game.mathHTML('<img src=x>')")), 'typed HTML is escaped in the preview')

    # gate: learn, drill, a miss, retype, fail the test once, retest, pass
    learn_all(page)
    c = card(page)
    formula_seen = False
    for _ in range(60):
        c = card(page)
        if c['type'] == 'formula':
            formula_seen = True
            page.fill('#ans', 'zzz')
            page.keyboard.press('Enter')
            page.wait_for_timeout(50)
            check('retype' in page.inner_text('#fb').lower(), 'a wrong formula shows the answer and asks to retype')
            page.fill('#ans', 'still wrong')
            page.keyboard.press('Enter')
            check(page.locator('.fb.no').count() == 1, 'a wrong retype does not advance')
            page.fill('#ans', c['rhs'])
            page.keyboard.press('Enter')
            page.wait_for_timeout(120)
            break
        right(page, c)
        page.wait_for_timeout(1500 if c['type'] == 'num' else 900)
        if page.evaluate('__game.view') != 'play':
            break
    check(formula_seen, 'the gate drills formulas')
    play_stage(page)
    check(page.evaluate('__game.view') == 'result', 'the gate drill finishes')
    page.click('#go')
    check(page.evaluate('__game.view') == 'exam', 'the gate test follows the drill')
    check(page.locator('#fb').count() == 0, 'the test gives no feedback')
    wrong(page, card(page))
    page.wait_for_timeout(40)
    exam_all(page)
    check('It takes' in page.inner_text('body'), 'one miss holds the gate shut')
    check(not page.evaluate('__game.progress.gate'), 'a failed test does not open the gate')
    page.click('#go')
    play_stage(page)
    page.click('#go')
    exam_all(page)
    check('from a blank page' in page.inner_text('body'), 'a perfect test passes the gate')
    page.click('#go')

    # stage
    check(page.locator('.st[data-t="basics"]').is_enabled(), 'topics open after the gate')
    page.click('.st[data-t="basics"]')
    check(page.evaluate('__game.view') == 'brief', 'a stage opens with its brief')
    page.click('#go')
    miss_free = False
    unread_seen = False
    for _ in range(80):
        if page.evaluate('__game.view') != 'play':
            break
        if page.locator('.fb.ok').count():
            page.keyboard.press('Enter')
            page.wait_for_timeout(200)
            continue
        c = card(page)
        if c['type'] == 'free' and not miss_free:
            miss_free = True
            wrong(page, c)
            page.wait_for_timeout(60)
            check('can miss a good answer' in page.inner_text('#fb').lower(), 'free answers say the check is key-word matching')
            page.click('#had')
            page.wait_for_timeout(60)
            continue
        if c['type'] == 'num' and not unread_seen:
            unread_seen = True
            before = page.evaluate('JSON.stringify(__game.progress.w)')
            page.fill('#ans', 'about forty-ish')
            page.keyboard.press('Enter')
            check(page.locator('#unread').count() == 1 and page.evaluate('JSON.stringify(__game.progress.w)') == before, 'unreadable input asks again and costs nothing')
        if page.locator('#cont').count():
            page.click('#cont')
            continue
        right(page, c)
        page.wait_for_timeout(180)
    if page.evaluate('__game.view') == 'result':
        page.click('#back')
    check(miss_free, 'a free item was missed and counted by the learner')
    check('on your own judgment' in page.inner_text('body').lower(), 'self-counted answers are labeled on the map')

    # progress survives a reload
    page.reload()
    check(page.evaluate('!!__game.progress.gate'), 'progress survives a reload')

    # recheck after the delay
    page.evaluate("() => { const k = 'myelinate-game:Circuits Exam Game'; const p = JSON.parse(localStorage.getItem(k)); p.gate = Date.now() - 9*3600e3; localStorage.setItem(k, JSON.stringify(p)); }")
    page.reload()
    check('Delayed recheck' in page.inner_text('body'), 'the delayed recheck appears after its delay')
    page.click('#go')
    wrong(page, card(page))
    page.wait_for_timeout(40)
    exam_all(page)
    check('held' in page.inner_text('body'), 'the recheck reports what held')
    page.reload()
    check('last delayed recheck' in page.inner_text('body').lower(), 'the map shows the last recheck result')
    check(not page.evaluate('__game.progress.recheck'), 'a failed recheck stays open')
    gate_left = page.evaluate("Object.keys(__game.progress.c).filter(k => k.startsWith('f:')).length")
    check(gate_left < 2, 'a recheck miss sends that formula back to drilling')

    # mock
    page.click('#mockB')
    check(page.evaluate('__game.view') == 'exam', 'the mock runs')
    exam_all(page)
    body = page.inner_text('body').lower()
    check('auto-marked' in body and 'practice score' in body and 'compare these yourself' in body, 'the mock labels its score and leaves short answers to the learner')

    # sheet, dark mode, phone width
    page.click('#go')
    page.click('#sheet')
    sheet = page.inner_text('body').lower()
    check('memorize' in sheet and 'provided on the exam' in sheet and 'units:' in sheet, 'the sheet shows tiers and units')
    check(not errors, f'no page errors: {errors}')
    check(not outside, f'no network requests: {outside}')

    for scheme in ('light', 'dark'):
        phone, errs, _ = open_page(browser, url, width=380, scheme=scheme)
        check(phone.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'no sideways scroll at phone width, {scheme}')
        check(not errs, f'no page errors at phone width, {scheme}')

    # the audit catches what it claims to
    resetter, _, _ = open_page(browser, url)
    resetter.evaluate("localStorage.setItem('myelinate-game:Circuits Exam Game', JSON.stringify({gate: 1, c: {b1: 1}, seen: {}}))")
    resetter.reload()
    resetter.click('#reset')
    check(resetter.evaluate('!!__game.progress.gate'), 'the first Reset click only asks')
    resetter.click('#reset')
    check(not resetter.evaluate('__game.progress.gate'), 'the second Reset click erases progress')

    def broken(d):
        items = d['topics'][0]['items']
        items[0]['src'] = ''
        items[1]['answer'] = 9
        items[2]['expr'] = 'v/nothing'
        items[4]['model'] = 'unrelated'
        items[4]['brief'] = 'raw \\frac{a}{b}'
        items.append(dict(items[0], src='x'))
        d['formulas'][0]['alts'] = ['Q']
        d['formulas'][0]['units'] = ''
    bad, _, _ = open_page(browser, variant(broken))
    a = bad.evaluate('gameAudit()')
    check(not a['ok'] and 'b1' in a['noSource'] and 'b2' in a['badSort'] and 'ohm_i' in a['badNumber'] and 'b5' in a['modelFailsRubric']
          and any('brief' in p for p in a['rawTeX']) and 'b1' in a['duplicateIds'] and 'ohm' in a['formulaAltsMissRhs'] and 'ohm' in a['noUnits'], f'gameAudit catches each fault: {a}')

    def edge(d):
        d['formulas'][0]['apply'] = None
        d['formulas'][2]['apply'] = {'id': 'x'}
        d['topics'][0]['items'].append({'id': 'q9', 'type': 'num', 'obj': 'units', 'src': 'x', 'q': 'Find $n_{t+1}$ from \\$5.', 'answer': 5, 'why': 'Is it? Yes.'})
        d['topics'][0]['items'].append({'id': 'q8', 'type': 'sort', 'obj': 'only', 'src': 'x', 'q': 'q', 'options': ['a', 'b'], 'answer': 0, 'why': 'costs $5 and sells for $10'})
    e, _, _ = open_page(browser, variant(edge))
    a = e.evaluate('gameAudit()')
    check('q9' not in a['badNumber'], 'the audit accepts braces inside math and a question mark in a reason')
    check('only' in a['sortOnly'] and a['suspectMath'] and 'ser' in a['applyIgnored'], 'the audit flags sort-only objectives, prose read as math and an ignored apply')

    def no_gate(d):
        d['formulas'] = []
        d['exam']['math'] = ['ohm_i']
    free, errs, _ = open_page(browser, variant(no_gate))
    check(free.locator('.st[data-t="basics"]').is_enabled() and not errs, 'a game with nothing to memorize has no gate')
    check(page.evaluate('gameAudit().progressSaves') is True, 'the audit reports that progress saves when storage works')
    blocked = browser.new_context()
    blocked.add_init_script("Object.defineProperty(window, 'localStorage', {get() { throw new Error('blocked'); }});")
    bp = blocked.new_page()
    bp.goto(url)
    check(bp.evaluate('gameAudit().progressSaves') is False, 'the audit reports when a sandbox blocks storage')
    check('Progress resets' in bp.inner_text('body'), 'the page tells the learner when progress will not save')
    blocked.close()
    browser.close()
print('All game journey checks passed.')
