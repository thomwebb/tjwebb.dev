# Writing a post

The blog is ordinary static HTML: no build step, package manager, or runtime dependency. `/blog/` is the index; `/blog/feed.xml` is RSS. The homepage and blog pages keep their CSS and theme scripts inline. When changing shared palettes or navigation, update the homepage, blog index, article template, and any published articles together.

## Draft safely

1. Copy `tools/blog-post-template.html` to a **local, gitignored** `drafts/<slug>.html`. Never put unapproved writing in `public/` or commit it to this public repository (even on a draft PR).
2. Replace `{{TITLE}}`, `{{DESCRIPTION}}`, `{{SLUG}}`, `{{DATE_ISO}}` (`YYYY-MM-DD`), and `{{DATE_DISPLAY}}` (e.g. a human-readable publication date) with approved values. HTML-escape text and attribute values. Write semantic HTML inside `.prose`; use headings, descriptive links, image alt text, and escaped code examples.
3. Leave `noindex` in drafts. It is only a search-engine hint, **not privacy protection**. Only `public/` is served by the configured Cloudflare static-assets deployment. For a private local preview, copy `public/` into a disposable directory under `/tmp`, then copy the draft to that directory’s `blog/<slug>/index.html`. Serve only that disposable directory with `python3 -m http.server 8000 --bind 127.0.0.1 --directory /tmp/<preview-directory>`. This preserves root-relative fonts and navigation. Delete the disposable preview afterward; never deploy it or serve the repository root.

## Publish only after approval

1. Copy the finished article to `public/blog/<slug>/index.html`, remove the draft comment and `noindex`, and check its title, description, canonical/OG URL and publication date. Optionally add `BlogPosting` JSON-LD with matching approved metadata. No article is included in this change.
2. Replace the index's empty-state paragraph with `<ul class="post-list">`. Add one `<li>` per published article, newest first, using `<h3><a href="/blog/<slug>/">Title</a></h3>`, `<time class="post-date mono" datetime="YYYY-MM-DD">Date</time>` and a short summary. Do not list drafts or future-dated posts.
3. Add an RSS `<item>` with escaped `<title>`, absolute `<link>`, identical `<guid isPermaLink="true">`, escaped plain-text `<description>`, and an RFC 2822 `<pubDate>` with timezone. Keep newest items first. The feed can stay empty until the first approved post.
4. Run `python3 -m unittest discover -s tests -v`. Serve `public/` locally (`python3 -m http.server 8000 --bind 127.0.0.1 --directory public`) and verify home → blog → article → blog, keyboard focus, a narrow viewport, all six themes, reload persistence, and reduced motion. Article code blocks should scroll without widening the page.
5. Open a PR. **Merging/pushing to `main` automatically deploys to the public domains** via the existing Cloudflare workflow. Do not use it as a private preview. Review and check CI on the final head before merging.
