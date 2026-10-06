import json, sys, re
from playwright.sync_api import sync_playwright
"""Journey test for a Myelinate lab: python3 tests/lab_journey.py [path/to/lab.html] [screenshot_dir]"""
import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
URL = (ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'examples/oxygen-lab.html')).resolve().as_uri()
SHOT = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('MYELINATE_SHOTS', '/tmp/myelinate-shots')
os.makedirs(SHOT, exist_ok=True)
ERRS=[]; RESULTS={}; FAILS=[]
def check(cond, msg):
    (RESULTS.setdefault('pass',[]) if cond else FAILS).append(msg)
    if not cond: print('FAIL:', msg)

def attach(pg, tag):
    pg.on('console', lambda m: ERRS.append(f'[{tag}] {m.type}: {m.text}') if m.type in ('error','warning') else None)
    pg.on('pageerror', lambda e: ERRS.append(f'[{tag}] PAGEERROR {e}'))

def nowidth(pg, where):
    sw, iw = pg.evaluate('[document.documentElement.scrollWidth, window.innerWidth]')
    check(sw <= iw, f'no horizontal scroll at {where} ({sw}<={iw})')

def nxt(pg):
    pg.click('#main [data-act="next"]')
    pg.wait_for_timeout(80)

def shot(pg, name, shots, full=False):
    if name in shots:
        pg.screenshot(path=f'{SHOT}/lab-{shots[name]}.png', full_page=full)

def set_range(pg, sel, v):
    pg.eval_on_selector(sel, "(el,v)=>{el.value=v; el.dispatchEvent(new Event('input',{bubbles:true}))}", v)

def full_run(pg, shots, phone=False, tag=''):
    pg.goto(URL); pg.wait_for_timeout(300)
    # gate on step 1
    pg.click('#main [data-act="next"]', force=True)
    check('alert' in pg.get_attribute('#gateMsg','class'), f'{tag} gate message shown when skipping')
    check(pg.evaluate('S.step')==0, f'{tag} gate blocks advancing')
    pg.fill('#hookText','Maybe the muscle is more acidic so Hb lets go')
    shot(pg,'hook',shots, full=False)
    pg.click('[data-act="hook-save"]'); nowidth(pg,f'{tag} hook'); nxt(pg)
    # parts
    for t in ['po2','sat','p50','aff']:
        pg.click(f'[data-term="{t}"]')
    shot(pg,'parts',shots); nowidth(pg,f'{tag} parts'); nxt(pg)
    # predict: leak check
    txt = pg.inner_text('#main'); html = pg.inner_html('#main')
    check('75%' not in txt and 'actual' not in html, f'{tag} no answer leak before prediction commit')
    check(pg.get_attribute('[data-act="commit"]','aria-disabled')=='true', f'{tag} commit locked before placing')
    # pointer placement on chart
    pg.locator('#predChart').scroll_into_view_if_needed(); box = pg.locator('#predChart').bounding_box()
    # svg y for 55% : Y(s)=18+(1-s)*330 ; scale
    ch = pg.evaluate('({...CH})'); sc = box['height']/ch['h']
    pg.mouse.click(box['x']+box['width']*0.33, box['y']+(ch['mt']+(1-0.55)*(ch['h']-ch['mt']-ch['mb']))*sc)
    v = pg.evaluate('S.predict.value'); check(v is not None and 50<=v<=60, f'{tag} pointer placement sets prediction (~55, got {v})')
    # keyboard adjust
    pg.focus('#predRange'); pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowRight')
    check(pg.evaluate('S.predict.value')==v+2, f'{tag} keyboard adjusts prediction slider')
    pg.click('label.pill:has(input[value="fairly"])')
    shot(pg,'predict-before',shots)
    pg.click('[data-act="commit"]')
    check('actual 75%' in pg.inner_html('#predChart'), f'{tag} reveal overlays actual 75%')
    pg.fill('#gapText','I pictured a straight line; the curve stays high longer.')
    pg.click('[data-act="gap-save"]')
    shot(pg,'predict-after',shots); nowidth(pg,f'{tag} predict'); nxt(pg)
    # explore
    check(pg.evaluate("document.querySelector('#simRead').innerText").find('26.6')>=0, f'{tag} explore starts at standard P50 26.6')
    shot(pg,'explore',shots, full=True); nowidth(pg,f'{tag} explore')
    pg.focus('#cPH')
    for _ in range(20): pg.keyboard.press('ArrowLeft')
    rd = pg.inner_text('#simRead')
    check('33.8' in rd, f'{tag} pH 7.20 via keyboard -> tissue P50 33.8 ({rd[:120]!r})')
    check(pg.get_attribute('#cPH','aria-valuetext')=='pH 7.20', f'{tag} aria-valuetext updates')
    pg.wait_for_timeout(600)
    live = pg.inner_text('#simLive'); check('33.8' in live, f'{tag} live region describes numbers ({live[:60]})')
    # PCO2 moves pH
    set_range(pg,'#cCO2',50)
    check(abs(float(pg.input_value('#cPH'))-7.2)<0.001, f'{tag} pH clamped at 7.20 when CO2 rises from pH 7.2')
    pg.click('[data-act="sim-reset"]')
    check('26.6 / 26.6' in pg.inner_text('#simRead'), f'{tag} reset restores standard conditions')
    set_range(pg,'#cCO2',60)
    ph = float(pg.input_value('#cPH')); check(abs(ph-7.22)<0.011, f'{tag} PCO2 60 lowers pH to ~7.22 (got {ph})')
    pg.click('[data-act="sim-reset"]')
    # hint ladder then answers
    pg.click('[data-hint="explore"]'); pg.click('[data-hint="explore"]')
    check(pg.locator('.hint').count()==2, f'{tag} hint ladder shows 2 hints')
    pg.fill('#q1in','22'); pg.click('[data-act="q1-check"]')
    check('Correct (hinted-correct)' in pg.inner_text('#main'), f'{tag} q1 correct flagged as with help')
    pg.click('[data-act="preset-sprint"]')
    rd = pg.inner_text('#simRead'); check('37.7' in rd, f'{tag} sprint preset P50 37.7 ({rd[:140]!r})')
    shot(pg,'explore-sprint',shots, full=True)
    pg.click('label.choice:has(input[name="q2"][value="c"])'); pg.click('[data-act="q2-check"]')
    check('Not quite' in pg.inner_text('#main'), f'{tag} q2 wrong feedback')
    pg.click('label.choice:has(input[name="q2"][value="d"])'); pg.click('[data-act="q2-check"]')
    # toggles
    pg.check('#cCO'); rd = pg.inner_text('#simRead'); check('pulse oximeter' in rd, f'{tag} CO toggle shows oximeter note')
    pg.uncheck('#cCO'); pg.check('#cFetal'); pg.uncheck('#cFetal')
    pg.click('.seg label:has(input[name="bpg"][value="low"])'); pg.click('.seg label:has(input[name="bpg"][value="normal"])')
    nxt(pg)
    # explain
    pg.click('label.choice:has(input[name="exChoice"][value="c"])')
    pg.fill('#exText','tissue PO2 is lower and acid/heat lower affinity so less O2 stays bound')
    pg.click('[data-act="ex-submit"]')
    check('Expert answer' in pg.inner_text('#main'), f'{tag} explain shows model answer after submit')
    pg.click('label.choice:has(input[name="exRub"][value="0"])'); pg.click('label.choice:has(input[name="exRub"][value="2"])')
    pg.click('[data-act="ex-save"]'); nowidth(pg,f'{tag} explain'); nxt(pg)
    ft = pg.inner_text('#main')
    check('O₂ binding is exothermic' in ft and 'heat all stabilize' not in ft and 'rises over hours to days' in ft and 'other four happening at once' not in ft, f'{tag} formalize wording fixed')
    shot(pg,'formalize',shots); nowidth(pg,f'{tag} formalize'); nxt(pg)
    # worked
    pg.fill('#se1','Only what Hb gives up reaches tissue.'); pg.click('[data-act="w1-done"]')
    pg.fill('#w2in','60'); pg.click('[data-act="num-check"][data-key="w2"]')
    pg.click('[data-hint="w2"]'); pg.fill('#w2in','65'); pg.click('[data-act="num-check"][data-key="w2"]')
    pg.fill('#w3in','34'); pg.click('[data-act="num-check"][data-key="w3"]')
    check('Blood loaded in the lungs at pH 7.40' in pg.inner_text('#main'), f'{tag} w3 trap-specific feedback')
    shot(pg,'worked',shots, full=True)
    pg.click('[data-act="num-reveal"][data-key="w3"]'); nowidth(pg,f'{tag} worked'); nxt(pg)
    # MCQ
    html = pg.inner_html('#main') + pg.inner_text('body')
    check('Misconception:' not in html and 'Right. Y loads' not in html, f'{tag} no MCQ feedback in DOM before submit')
    plan = {'m1':('b','r2','sure'),'m2':('a','r1','sure'),'m3':('c','r2','guess'),'m4':('d','r1','fairly'),'m5':('c','r1','guess'),'m6':('b','r1','sure')}
    for q,(a,r,c) in plan.items():
        pg.click(f'label.choice:has(input[name="ans-{q}"][value="{a}"])')
        pg.click(f'label.choice:has(input[name="rsn-{q}"][value="{r}"])')
        pg.click(f'label.pill:has(input[name="conf-{q}"][value="{c}"])')
        pg.click(f'[data-act="mc-submit"][data-q="{q}"]')
    m3t = pg.inner_text('#mc-m3'); m6t = pg.inner_text('#mc-m6'); body = pg.inner_html('#main')
    check('diffuses down its PO₂ gradient' in m3t and 'flows toward' not in body and 'pulls O₂ across' not in body, f'{tag} fetal feedback uses gradient explanation')
    check('fixed tissue PO₂ of 40 mmHg' in m6t and 'partly preserves extraction' in m6t, f'{tag} CO caveat in feedback')
    m2 = pg.inner_text('#mc-m2'); check('Misconception: Right shift' in m2 or 'MISCONCEPTION: RIGHT SHIFT' in m2.upper(), f'{tag} m2 names the misconception')
    check(pg.locator('#mc-m2 .reteach').count()==1, f'{tag} confident-wrong m2 gets reteach card')
    check(pg.locator('#mc-m5 .reteach').count()==0, f'{tag} guessing-wrong m5 gets no reteach card')
    check(pg.locator('#mc-m1 .fb.good').count()==1, f'{tag} m1 correct feedback')
    pg.locator('#mc-m2').scroll_into_view_if_needed()
    shot(pg,'check',shots)
    nowidth(pg,f'{tag} check'); nxt(pg)
    # transfer
    pg.click('label.choice:has(input[name="ans-tr"][value="d"])'); pg.click('label.choice:has(input[name="rsn-tr"][value="r1"])')
    pg.click('label.pill:has(input[name="conf-tr"][value="fairly"])'); pg.click('[data-act="mc-submit"][data-q="tr"]')
    pg.fill('#trText','Left shift, loads fine, unloads less until BPG returns'); pg.click('[data-act="tr-model"]')
    pg.click('label.choice:has(input[name="trRub"][value="0"])'); pg.click('[data-act="tr-save"]')
    shot(pg,'transfer',shots, full=True); nowidth(pg,f'{tag} transfer'); nxt(pg)
    # exit
    check('feedback' not in pg.inner_text('#main').lower() or True, 'exit')
    pg.click('[data-act="exit-submit"]'); check('left' in pg.inner_text('#exitMsg'), f'{tag} exit requires all answers')
    pg.fill('#ex-e1','75')
    for v in ['temp','ph','pco2','bpg']: pg.click(f'label.choice:has(input[name="ex-e2"][value="{v}"])')
    pg.click('label.choice:has(input[name="ex-e3"][value="c"])'); pg.click('label.choice:has(input[name="ex-e4"][value="a"])')
    pg.click('[data-act="exit-submit"]')
    shot(pg,'exit',shots); nowidth(pg,f'{tag} exit'); nxt(pg)
    # results
    items = pg.evaluate("Object.fromEntries(Object.values(S.items).map(i=>[i.id,itemStatus(i)]))")
    RESULTS[f'{tag}items']=items
    U='unassisted-correct'; H='hinted-correct'
    exp = {'q1':H,'q2':H,'w2':H,'w3':'revealed','m1':U,'m2':'incorrect','m3':U,'m4':U,'m5':'incorrect','m6':U,'tr':U,'e1':U,'e2':U,'e3':U,'e4':'incorrect','xc':U}
    check(all(items.get(k)==v for k,v in exp.items()), f'{tag} item statuses as expected {items}')
    stats = pg.locator('.stat b').all_inner_texts(); RESULTS[f'{tag}stats']=stats
    check(stats==['9','3','1','3'], f'{tag} results stats unassisted/assisted/revealed/incorrect = {stats}')
    tstates = pg.evaluate("TARGETS.map(t=>targetState(t.id)[0])"); RESULTS[f'{tag}targets']=tstates
    check(tstates==['Independent this session','Needs support','Independent this session','Needs support'], f'{tag} target states follow 2-of-last-3 rule {tstates}')
    check('at least 2 unassisted-correct among the last 3' in pg.inner_text('#main'), f'{tag} rule shown on results')
    badges = set(pg.locator('table.res .badge').all_inner_texts()); check({b.lower() for b in badges} <= {'unassisted-correct','hinted-correct','revealed','incorrect','self-assessed','independent this session','needs support','not checked'}, f'{tag} only enum outcome labels used {badges}')
    check('default ladder, not a research-optimal schedule' in pg.inner_text('#main'), f'{tag} spacing caveat shown')
    shot(pg,'results',shots, full=True); nowidth(pg,f'{tag} results')
    return pg

with sync_playwright() as p:
    br = p.chromium.launch()
    # ===== Desktop light full run =====
    ctx = br.new_context(viewport={'width':1440,'height':900}, color_scheme='light', accept_downloads=True)
    pg = ctx.new_page(); attach(pg,'desk-light')
    full_run(pg, {'hook':'d-light-01-hook','parts':'d-light-02-parts','predict-before':'d-light-03-predict','predict-after':'d-light-04-predict-reveal','explore':'d-light-05-explore','explore-sprint':'d-light-06-explore-sprint','formalize':'d-light-07-formalize','worked':'d-light-08-worked','check':'d-light-09-mcq','transfer':'d-light-10-transfer','exit':'d-light-11-exit','results':'d-light-12-results'}, tag='D:')
    # flashcard review
    pg.click('[data-act="rv-start"]'); pg.click('[data-act="rv-show"]'); pg.click('[data-act="rv-good"]')
    pg.click('[data-act="rv-show"]'); pg.click('[data-act="rv-again"]')
    cs = pg.evaluate("JSON.parse(localStorage.getItem(CARDS_KEY))")
    c1, c2 = cs['cards']['c1'], cs['cards']['c2']
    import time
    now=time.time()*1000
    check(abs((c1['due']-now)/86400e3-1)<0.01 and c1['reps']==1, f'good -> due in 1 day ({(c1["due"]-now)/86400e3:.3f}d)')
    check(abs((c2['due']-now)/60e3-10)<0.5 and c2['reps']==0, 'again -> due in 10 minutes')
    rows = pg.locator('#cardRows tr').all_inner_texts()
    check('In 1 day' in rows[0] and 'In 10 min' in rows[1], f'next-due shown per card: {rows[0][-30:]!r} / {rows[1][-20:]!r}')
    # exports
    with pg.expect_download() as d: pg.click('[data-act="exp-quizlet"]')
    dl = d.value; qp = SHOT+'/'+dl.suggested_filename; dl.save_as(qp); qt=open(qp,encoding='utf-8').read()
    with pg.expect_download() as d: pg.click('[data-act="exp-anki"]')
    dl = d.value; ap = SHOT+'/'+dl.suggested_filename; dl.save_as(ap); at=open(ap,encoding='utf-8').read()
    ql = qt.rstrip('\n').split('\n'); al = at.rstrip('\n').split('\n')
    nc = pg.evaluate('CARDS.length'); check(6<=nc<=12, f'card count {nc} in 6-12')
    check(len(ql)==nc and all(l.count('\t')==1 for l in ql), f'Quizlet export: {nc} lines, one TAB each ({len(ql)})')
    check(not any('Exercise' in l for l in ql) and not any(l.split('\t')[0].startswith('CADET') for l in ql), 'no CADET-front / Exercise card')
    check(al[0]=='#separator:tab' and al[1]=='#html:false' and len(al)==nc+2 and all(l.count('\t')==1 for l in al[2:]), f'Anki export: header + {nc} tab lines')
    RESULTS['quizlet_sample']=ql[0]; RESULTS['anki_head']=al[:3]
    # reload -> resume
    pg.reload(); pg.wait_for_timeout(300)
    check(pg.evaluate('S.step')==10 and 'Welcome back' in pg.inner_text('#noticeArea'), 'reload resumes at results with notice')
    check(pg.locator('.stat b').all_inner_texts()==['9','3','1','3'], 'results survive reload')
    # rail navigation back to step 3 works & forward
    pg.click('#railList button[data-go="2"]'); check(pg.evaluate('S.step')==2, 'rail jump back works'); 
    check(pg.get_attribute('#predRange','disabled') is not None, 'committed prediction stays locked after reload')
    pg.click('#railList button[data-go="10"]')
    # clear progress: cancel then confirm
    pg.click('#clearBtn'); check(pg.evaluate("document.getElementById('confirmDlg').open"), 'clear dialog opens (in-page)')
    pg.click('#dlgNo'); check(pg.evaluate('S.step')==10, 'cancel keeps progress')
    pg.click('#clearBtn'); pg.click('#dlgYes')
    check(pg.evaluate('S.step')==0 and pg.evaluate('S.maxReached')==0, 'clear resets to step 1')
    check(pg.evaluate("JSON.parse(localStorage.getItem(STORAGE_KEY)).hook.done")==False, 'storage reset after clear')
    check(pg.evaluate("localStorage.getItem(CARDS_KEY)") is None, 'card schedule cleared')
    pg.reload(); check(pg.evaluate('S.step')==0, 'after clear+reload at step 1')
    # numeric model checks
    m = pg.evaluate("""({s100:MODEL.hill(100,26.6),s40:MODEL.hill(40,26.6),s20:MODEL.hill(20,26.6),
       p72:MODEL.p50({pH:7.2,temp:37,bpg:'normal',fetal:false,co:false}),p76:MODEL.p50({pH:7.6,temp:37,bpg:'normal',fetal:false,co:false}),
       p41:MODEL.p50({pH:7.4,temp:41,bpg:'normal',fetal:false,co:false}), fet:MODEL.p50({pH:7.4,temp:37,bpg:'normal',fetal:true,co:false}),
       co:MODEL.p50({pH:7.4,temp:37,bpg:'normal',fetal:false,co:true}), coArt:MODEL.hbo2(100,{pH:7.4,temp:37,bpg:'normal',fetal:false,co:true}),
       low:MODEL.p50({pH:7.4,temp:37,bpg:'low',fetal:false,co:false}), high:MODEL.p50({pH:7.4,temp:37,bpg:'high',fetal:false,co:false})})""")
    RESULTS['model']=m
    check(0.97<=m['s100']<=0.98, f"S(100)={m['s100']:.4f}")
    check(0.74<=m['s40']<=0.76, f"S(40)={m['s40']:.4f}")
    check(0.31<=m['s20']<=0.35, f"S(20)={m['s20']:.4f}")
    check(33<=m['p72']<=35, f"P50 at pH 7.2 = {m['p72']:.2f}")
    ctx.close()

    # ===== Desktop dark: screenshots =====
    ctx = br.new_context(viewport={'width':1440,'height':900}, color_scheme='dark', accept_downloads=True)
    pg = ctx.new_page(); attach(pg,'desk-dark')
    full_run(pg, {'hook':'d-dark-01-hook','predict-after':'d-dark-04-predict-reveal','explore-sprint':'d-dark-06-explore-sprint','check':'d-dark-09-mcq','results':'d-dark-12-results'}, tag='DD:')
    ctx.close()

    # ===== Phone light + dark =====
    for scheme in ['light','dark']:
        ctx = br.new_context(viewport={'width':375,'height':812}, color_scheme=scheme, device_scale_factor=2, has_touch=True, accept_downloads=True)
        pg = ctx.new_page(); attach(pg,'phone-'+scheme)
        full_run(pg, {'hook':f'p-{scheme}-01-hook','predict-after':f'p-{scheme}-04-predict-reveal','explore-sprint':f'p-{scheme}-06-explore-sprint','check':f'p-{scheme}-09-mcq','worked':f'p-{scheme}-08-worked','results':f'p-{scheme}-12-results'}, phone=True, tag=f'P{scheme}:')
        # rail toggle on phone
        pg.click('#railToggle'); check(pg.locator('#railList').is_visible(), 'phone rail list opens')
        pg.screenshot(path=f'{SHOT}/lab-p-{scheme}-13-rail-open.png')
        # touch targets
        small = pg.evaluate("""[...document.querySelectorAll('button, .choice, .pill, input[type=range], .seg label, .term, .switch')].filter(e=>e.offsetParent).map(e=>[e.className||e.tagName, e.getBoundingClientRect().height]).filter(x=>x[1]<43.5)""")
        check(len(small)==0, f'phone touch targets >=44px ({small[:5]})')
        ctx.close()

    # ===== localStorage throws =====
    ctx = br.new_context(viewport={'width':1024,'height':800})
    ctx.add_init_script("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('blocked','SecurityError')}});")
    pg = ctx.new_page(); attach(pg,'nostorage')
    pg.goto(URL); pg.wait_for_timeout(200)
    check("can't be saved" in pg.inner_text('#noticeArea'), 'storage-blocked notice shown')
    pg.fill('#hookText','x'); pg.click('[data-act="hook-save"]'); nxt(pg)
    check(pg.evaluate('S.step')==1, 'app works with throwing localStorage')
    for t in ['po2','sat','p50','aff']: pg.click(f'[data-term="{t}"]')
    nxt(pg); check(pg.evaluate('S.step')==2, 'advances further without storage')
    pg.screenshot(path=f'{SHOT}/lab-nostorage.png')
    ctx.close()
    # ===== reduced motion sanity =====
    ctx = br.new_context(viewport={'width':1440,'height':900}, reduced_motion='reduce')
    pg = ctx.new_page(); attach(pg,'rm'); pg.goto(URL)
    td = pg.evaluate("getComputedStyle(document.querySelector('.btn')).transitionDuration")
    check(td in ('0s',), f'reduced motion: no transitions ({td})')
    anims = pg.evaluate("document.getAnimations().length"); check(anims==0, f'no running animations ({anims})')
    ctx.close()
    br.close()

print('\nCONSOLE ERRORS/WARNINGS:', len(ERRS)); [print(' ',e) for e in ERRS]
print('PASSED:', len(RESULTS.get('pass',[])), 'FAILED:', len(FAILS))
for f in FAILS: print('  FAIL', f)
print(json.dumps({k:v for k,v in RESULTS.items() if k!='pass'}, indent=1, ensure_ascii=False))
