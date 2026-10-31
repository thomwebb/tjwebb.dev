"""Dependency-free checks for the deployed static assets: python3 -m unittest discover -s tests."""
from pathlib import Path
from html.parser import HTMLParser
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.h1 = 0
        self.ids = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])

class SiteTests(unittest.TestCase):
    def test_public_pages(self):
        for path in PUBLIC.rglob('*.html'):
            with self.subTest(path=path):
                text = path.read_text()
                page = Page(text)
                self.assertEqual(page.h1, 1)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertNotIn('{{', text)
                self.assertNotIn('content="noindex"', text)
                for link in page.links:
                    url = urlsplit(link)
                    if url.scheme or url.netloc:
                        continue
                    if not url.path:
                        if url.fragment:
                            self.assertIn(url.fragment, page.ids)
                        continue
                    target = PUBLIC / url.path.lstrip('/') if url.path.startswith('/') else path.parent / url.path
                    self.assertTrue(target.is_file() or (target / 'index.html').is_file(), link)

    def test_blog_discovery(self):
        self.assertIn('href="/blog/"', (PUBLIC / 'index.html').read_text())
        for path in (PUBLIC / 'index.html', PUBLIC / 'blog/index.html'):
            self.assertIn('type="application/rss+xml"', path.read_text())
        blog = (PUBLIC / 'blog/index.html').read_text()
        self.assertIn('aria-current="page"', blog)

    def test_feed_and_unpublished_template(self):
        channel = ET.parse(PUBLIC / 'blog/feed.xml').getroot().find('channel')
        self.assertEqual(channel.findtext('link'), 'https://tjwebb.dev/blog/')
        for item in channel.findall('item'):
            link = item.findtext('link')
            self.assertTrue(link.startswith('https://tjwebb.dev/blog/'))
            self.assertEqual(item.findtext('guid'), link)
            self.assertTrue(item.findtext('title'))
            self.assertTrue(item.findtext('pubDate'))
            self.assertTrue((PUBLIC / urlsplit(link).path.lstrip('/') / 'index.html').is_file())
        self.assertFalse((PUBLIC / 'blog-post-template.html').exists())
        template = (ROOT / 'tools/blog-post-template.html').read_text()
        self.assertIn('content="noindex"', template)
        self.assertIn('<time datetime="{{DATE_ISO}}">', template)

if __name__ == '__main__':
    unittest.main()
