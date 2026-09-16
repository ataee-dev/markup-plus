import sys
sys.path.insert(0, "src")

from markup_plus.renderer import to_html

src = "Text[^1].\n\n[^1]: Note text."
html = to_html(src)

print("Footnotes in HTML:", 'class="footnotes"' in html)
print("Length:", len(html))
print("Has task-list in CSS:", "task-list" in html)