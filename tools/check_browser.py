from playwright.sync_api import sync_playwright
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import tempfile
import shutil
root=Path(__file__).resolve().parents[1]
preview = tempfile.TemporaryDirectory()
shutil.copytree(root / 'public', Path(preview.name), dirs_exist_ok=True)
article = (root / 'tools/blog-post-template.html').read_text()
for key, value in {'TITLE': 'Browser test article', 'DESCRIPTION': 'Template preview only.', 'SLUG': 'test-article', 'DATE_ISO': '2026-10-31', 'DATE_DISPLAY': 'October 31, 2026'}.items():
 article = article.replace('{{' + key + '}}', value)
article = article.replace('<!-- Approved article HTML goes here. Escape code examples with &lt; and &amp;. -->', '<h2>Reading layout</h2><p>Template preview only.</p><pre><code>' + 'x' * 200 + '</code></pre>')
article_path = Path(preview.name) / 'blog/test-article/index.html'
article_path.parent.mkdir()
article_path.write_text(article)
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=preview.name))
Thread(target=server.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:' + str(server.server_port)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for width in [320,375,768,1440]:
   page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(base + '/')
   page.locator('nav a[href="/blog/"]').click()
   assert page.url.endswith('/blog/')
   assert page.get_by_role('heading',name='Blog',exact=True).count()==1
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   for expected in ['gruvbox','dracula','solarized-dark','monokai','phosphor','github-dark']:
    page.get_by_role('button',name='Switch terminal theme',exact=False).click()
    assert page.locator('html').get_attribute('data-theme')==expected
    page.reload()
    assert page.locator('html').get_attribute('data-theme')==expected
   page.locator('nav a[href="/"]').click()
   assert page.url.endswith('/')
   page.go_back();assert page.url.endswith('/blog/')
   page.go_forward();assert page.url==base + '/'
   page.goto(base + '/blog/')
   page.keyboard.press('Tab')
   assert page.locator(':focus').inner_text()=='Skip to content'
   page.keyboard.press('Enter')
   assert page.locator(':focus').get_attribute('id')=='main'
   (root / 'preview').mkdir(exist_ok=True)
   page.screenshot(path=str(root / f'preview/blog-{width}.png'), full_page=True)
   page.goto(base + '/blog/test-article/')
   assert page.get_by_role('heading', name='Browser test article', exact=True).is_visible()
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
   assert page.locator('pre').evaluate('(el) => el.scrollWidth > el.clientWidth')
   page.get_by_role('link', name='← all posts').click()
   assert page.url.endswith('/blog/')
   assert not errors,errors
   page.close()
  page=browser.new_page(java_script_enabled=False,viewport={'width':375,'height':812})
  page.goto(base + '/blog/')
  assert page.get_by_role('heading',name='Blog',exact=True).is_visible()
  assert page.get_by_text('No posts yet.').is_visible()
  assert page.request.get(base + '/blog/feed.xml').ok
  assert page.request.get(base + '/tools/blog-post-template.html').status==404
  browser.close()
 print('PASS: 4 viewports; all 6 themes and reload persistence; home/blog + Back/Forward; keyboard skip link; reduced motion; JS disabled; RSS; template not served; no JS errors')
finally:
 server.shutdown();server.server_close();preview.cleanup()
