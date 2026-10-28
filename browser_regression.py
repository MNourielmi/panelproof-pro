"""Run with: python browser_regression.py (requires playwright and Chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
HTML=Path(__file__).with_name('index.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(HTML)
    assert page.locator('[data-status]').count()==20
    assert '20 not tested' in page.locator('#readiness').inner_text()
    page.locator('#project').fill('Regression test')
    page.locator('[data-status]').first.select_option('Fail')
    assert page.locator('#issues').inner_text()=='1'
    assert '1 failed or blocked' in page.locator('#readiness').inner_text()
    page.locator('#search').fill('Emergency stop')
    assert page.locator('[data-status]').count()==1
    page.locator('#search').fill('')
    page.locator('#customTitle').fill('Test custom item')
    page.locator('#add').click()
    assert page.locator('#total').inner_text()=='21'
    with page.expect_download() as d:page.locator('#issuesCsv').click()
    assert d.value.suggested_filename=='PanelProof_issues.csv'
    with page.expect_download() as d:page.locator('#allCsv').click()
    assert d.value.suggested_filename=='PanelProof_register.csv'
    with page.expect_download() as d:page.locator('#export').click()
    assert d.value.suggested_filename.endswith('.json')
    page.on('dialog',lambda dialog:dialog.accept())
    page.locator('#demo').click()
    assert 'Demonstration data' in page.locator('#readiness').inner_text()
    page.evaluate('window.print=()=>{}')
    page.locator('#print').click()
    assert 'SAMPLE DATA' in page.locator('#report').inner_text()
    page.locator('#newProject').click()
    assert page.locator('#total').inner_text()=='20'
    assert not errors,errors
    browser.close()
print('PASS: 12 browser checks; no uncaught JavaScript exceptions')
