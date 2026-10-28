"""PanelProof release smoke tests. Run: python verify_release.py"""
from pathlib import Path
from tempfile import TemporaryDirectory
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright

root=Path(__file__).parent
server=ThreadingHTTPServer(('127.0.0.1',0), partial(SimpleHTTPRequestHandler,directory=str(root/'public_site')))
Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    with TemporaryDirectory() as tmp:
        context=browser.new_context(accept_downloads=True, viewport={'width':1440,'height':1000})
        page=context.new_page()
        errors=[]
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
        assert page.get_by_text('Stop rebuilding FAT/SAT paperwork').count()==1
        page.get_by_role('link', name='Try the interactive demo').click()
        assert page.url.endswith('app.html'),page.url
        assert page.locator('#total').inner_text()=='20'
        page.locator('#project').fill('Acceptance Demo')
        page.locator('#client').fill('Example Client')
        page.locator('#panelid').fill('CP-01')
        page.locator('#tech').fill('Inspector Example')
        page.locator('[data-status="1"]').select_option('Fail')
        page.locator('[data-evidence="1"]').fill('Example discrepancy')
        assert page.locator('#issues').inner_text()=='1'
        assert 'NOT READY' in page.locator('#readiness').inner_text()
        with page.expect_download() as d: page.locator('#issuesCsv').click()
        issue=d.value
        assert issue.suggested_filename.endswith('.csv')
        with page.expect_download() as d: page.locator('#export').click()
        exported=d.value
        exported.save_as(Path(tmp)/'project.json')
        page.once('dialog',lambda dialog:dialog.accept())
        page.locator('#newProject').click()
        # Import the saved project after a reset
        with page.expect_file_chooser() as chooser: page.locator('#import').click()
        page.once('dialog',lambda dialog:dialog.accept())
        chooser.value.set_files(str(Path(tmp)/'project.json'))
        assert page.locator('#project').input_value()=='Acceptance Demo'
        page.reload()
        assert page.locator('#project').input_value()=='Acceptance Demo'
        page.locator('#demo').click()
        assert 'Demonstration data' in page.locator('#readiness').inner_text()
        page.screenshot(path=str(root/'product_screenshot.png'),full_page=True)
        assert not errors,errors
        print('PASS: landing navigation, 20 checks, status, evidence, readiness, CSV, JSON, import, persistence, demo warning, JS errors')
        context.close()
    browser.close()
