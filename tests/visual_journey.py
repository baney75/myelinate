#!/usr/bin/env python3
"""Open the authored visual template and check its learning gates and small-screen layout."""
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / 'templates' / 'visual-stepper.html').as_uri()

def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print('PASS:', message)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for width, scheme, motion in [(1280, 'light', 'no-preference'), (360, 'dark', 'reduce')]:
        page = browser.new_page(viewport={'width': width, 'height': 800}, color_scheme=scheme, reduced_motion=motion)
        errors = []
        page.on('pageerror', lambda error, errors=errors: errors.append(str(error)))
        page.goto(URL)
        check(page.locator('#frames .frame').count() == 1, f'{width}px starts on first step')
        check('evaporates' not in page.locator('#frames').inner_text().lower(), f'{width}px future step hidden')
        check(page.locator('#reveal').is_disabled(), f'{width}px reveal disabled before commitment')
        page.locator('#commit').click()
        check('Enter a prediction' in page.locator('#path-status').inner_text(), f'{width}px blank prediction refused')
        page.locator('#prediction').fill('Some water rises into the air')
        page.locator('#prediction').press('Tab')
        check(page.evaluate('document.activeElement.id') == 'commit', f'{width}px keyboard reaches commit')
        page.keyboard.press('Enter')
        check(page.locator('#reveal').is_enabled(), f'{width}px commitment unlocks reveal')
        check(page.locator('#frames .frame').count() == 1, f'{width}px commitment alone does not reveal')
        check(page.evaluate('document.activeElement.id') == 'reveal', f'{width}px keyboard focus moves to reveal')
        page.keyboard.press('Enter')
        check(page.locator('#frames .frame').count() == 2, f'{width}px reveal adds one step')
        check('You predicted: Some water rises into the air' in page.locator('#frames .frame').nth(1).inner_text(), f'{width}px first prediction stays beside revealed step')
        check('evaporates' in page.locator('#frames').inner_text().lower(), f'{width}px step text appears after reveal')
        check(page.locator('#reveal').is_disabled(), f'{width}px next reveal needs another prediction')
        check('condenses' not in page.locator('#frames').inner_text().lower(), f'{width}px third step hidden')
        page.locator('#prediction').fill('It cools and gathers')
        page.locator('#commit').click()
        page.locator('#reveal').click()
        check(page.locator('#frames .frame').count() == 3, f'{width}px second reveal works')
        check('You predicted: It cools and gathers' in page.locator('#frames .frame').nth(2).inner_text(), f'{width}px second prediction stays beside revealed step')
        scroll, inner = page.evaluate('[document.documentElement.scrollWidth, window.innerWidth]')
        check(scroll <= inner, f'{width}px expanded path has no horizontal overflow ({scroll} <= {inner})')
        if width == 360:
            page.screenshot(path='/tmp/myelinate-visual-360-dark-revealed.png', full_page=True)
        page.locator('#recall').click()
        check(page.locator('#frames').is_hidden() and page.locator('#path-figure').is_hidden(), f'{width}px recall hides the answer')
        check('feeds rivers' not in page.locator('#map-status').inner_text().lower(), f'{width}px map key hidden')
        page.locator('#check-map').click()
        check('Fill both blanks' in page.locator('#map-status').inner_text(), f'{width}px blank map refused')
        page.locator('#verb').fill('feeds')
        page.locator('#concept').fill('rivers')
        page.locator('#concept').press('Tab')
        check(page.evaluate('document.activeElement.id') == 'check-map', f'{width}px keyboard reaches map check')
        page.keyboard.press('Enter')
        check('feeds rivers' in page.locator('#map-status').inner_text().lower(), f'{width}px committed map receives key')
        scroll, inner = page.evaluate('[document.documentElement.scrollWidth, window.innerWidth]')
        check(scroll <= inner, f'{width}px map feedback has no horizontal overflow ({scroll} <= {inner})')
        page.locator('#reset-map').click()
        check('feeds rivers' not in page.locator('#map-status').inner_text().lower(), f'{width}px map reset hides key')
        page.locator('#reset').click()
        check(page.locator('#frames .frame').count() == 1 and page.locator('#reveal').is_disabled() and page.locator('#frames').is_visible(), f'{width}px step reset restores gate')
        check('You predicted:' not in page.locator('#frames').inner_text(), f'{width}px reset clears prior predictions')
        scroll, inner = page.evaluate('[document.documentElement.scrollWidth, window.innerWidth]')
        check(scroll <= inner, f'{width}px no horizontal overflow ({scroll} <= {inner})')
        check(not errors, f'{width}px no script errors')
        if width == 360:
            page.screenshot(path='/tmp/myelinate-visual-360-dark.png', full_page=True)
        else:
            page.screenshot(path='/tmp/myelinate-visual-desktop-light.png', full_page=True)
        page.close()
    browser.close()
