Markup+ FAQ
===========

Version: 0.6.0
Last Updated: January 2026

Frequently asked questions about Markup+.

---

Table of Contents
-----------------

1. General Questions
2. Installation
3. Syntax and Features
4. Files and Output
5. CLI Usage
6. Themes and Customization
7. RTL and Internationalization
8. Performance
9. Troubleshooting
10. Contributing
11. Commercial Use and Licensing

---

1. General Questions
--------------------

### What is Markup+?

Markup+ is a modern markup language that extends Markdown with
powerful features for building documentation, blogs, reports, and
interactive web pages. It includes variables, conditionals, loops,
components, charts, math, and auto RTL detection.

### What is the difference between Markup+ and Markdown?

Markup+ is a superset of Markdown. Everything valid in Markdown is
valid in Markup+, plus:

- Variables and filters
- Conditionals (@if) and loops (@each)
- Reusable components (@def)
- Charts (bar, line, pie, doughnut)
- Math formulas (KaTeX)
- Tabs and accordions
- Rich alerts (note, warning, tip, danger, success)
- Auto RTL detection for Persian, Arabic, Hebrew, Urdu
- Image galleries with lightbox
- File imports (@import)

### Is Markup+ a programming language?

Not exactly. It is a markup language with logic. You can define
variables, make decisions, and loop -- but it is designed for
documents, not general programming.

### Who is Markup+ for?

- Technical writers who want more than Markdown
- Developers who need charts and math in documentation
- Persian and Arabic writers who need RTL support
- Anyone who wants beautiful output with zero configuration

### Is Markup+ free?

Yes, for non-commercial use. Markup+ is released under the Markup+
Non-Commercial License. Commercial use requires a separate license.
See LICENSE for full terms.

### What is the current version?

Markup+ v0.6.0, released on September 16, 2026.

### What are the system requirements?

- Windows 10 or later (64-bit) for the standalone installer
- Python 3.9 or higher (for pip installation)
- Any modern browser (Chrome, Firefox, Safari, Edge) for viewing output

### Does Markup+ work offline?

Writing works offline. Reading works offline. But the generated HTML
uses CDN resources for:

- Prism.js (syntax highlighting)
- Chart.js (charts)
- KaTeX (math formulas)

For fully offline use, download these libraries locally and update
the HTML template.

---

2. Installation
---------------

### How do I install Markup+?

Three methods:

**Method 1: Standalone Installer (Windows)**

Download `markup-plus-setup-0.6.0.exe` from:

    https://github.com/ataee-dev/markup-plus/releases/latest

Run the installer. No Python required.

**Method 2: Portable Version**

Download `markup-plus.zip`, extract, and run `mup.exe`.

**Method 3: pip install (Developers)**

    pip install markup-plus

### Do I need Python to use Markup+?

No. If you use the standalone installer, you do not need Python.

If you use pip install, you need Python 3.9 or higher.

### How do I verify the installation?

Open a new Command Prompt and run:

    mup --version

Expected output: `Markup+ v0.6.0`

### The installer shows a SmartScreen warning. What do I do?

The installer is not code-signed. Windows SmartScreen may show a
warning. This is normal for open-source software distributed outside
the Microsoft Store.

Click "More info" then "Run anyway" to proceed.

### I get "mup: command not found". What do I do?

Cause: PATH was not updated in the current Command Prompt.

Fix: Close the Command Prompt and open a new one. PATH changes
require a new session.

If still failing, reinstall with PATH option checked. Or use the full
module path:

    python -m markup_plus file.mup

### How do I uninstall Markup+?

**If installed via installer:**

1. Open Control Panel
2. Go to Programs and Features
3. Find Markup+
4. Click Uninstall

**If installed via pip:**

    pip uninstall markup-plus

### How do I upgrade to a newer version?

**If installed via installer:**

Download the new installer and run it. It will upgrade in place.

**If installed via pip:**

    pip install --upgrade markup-plus

### Can I install both installer version and pip version?

Yes, but they are separate. The installer version goes to
`C:\Program Files\Markup+\`. The pip version goes to Python's Scripts
folder. They do not conflict.

However, if both are in PATH, the one with higher priority will run.

---

3. Syntax and Features
----------------------

### What file extension should I use?

Use `.mup` for Markup+ files. `.md` files also work (auto-detected).

### Can I convert my existing Markdown files?

Yes. Just run:

    mup myfile.md

Output is `myfile.html`. Most Markdown features work identically.

### How do I add a comment?

Use `@#` at the start of a line:

    @# This is a comment -- not rendered

    Visible content here.

### How do I create a variable?

    @let name = "Ali"

Then use it with curly braces:

    Hello {name}!

### How do I create a checklist?

Use task-list syntax:

    - [x] Done task
    - [ ] Pending task

Rendered as checkboxes.

### How do I add a table of contents?

Add `@toc` where you want it:

    @toc

With custom title:

    @toc {title="Contents"}

### Can I nest lists?

Indented (nested) lists are not yet supported in v0.6.0. Only flat
lists are supported.

Nested lists are planned for a future version.

### Can I use HTML directly?

Some inline HTML passes through. For safety and consistency, prefer
Markup+ syntax.

### How do I create a chart?

    @chart(type="bar" title="Monthly Sales")
    data: [100, 250, 180, 320]
    labels: ["Jan", "Feb", "Mar", "Apr"]
    @end

Chart types: bar, line, pie, doughnut.

### How do I write math formulas?

Block formula (centered):

    $$ E = mc^2 $$

Inline formula:

    The famous formula $E = mc^2$ changed physics.

### How do I create tabs?

    @tabs
    @tab "Python"
    ```python
    print("Hello")
    ```
    @end

    @tab "JavaScript"
    ```javascript
    console.log("Hello");
    ```
    @end
    @end

### How do I create an accordion?

    @collapse
    @item "Question 1"
    Answer 1.
    @end

    @item "Question 2"
    Answer 2.
    @end
    @end

### How do I create an alert?

    @note
    This is a note.
    @end

Five types: `@note`, `@warning`, `@tip`, `@danger`, `@success`.

### How do I create a component?

Define:

    @def Card(title, body)
    > **{title}**
    >
    > {body}
    @end

Use:

    @Card(title="Hello", body="This is a card.")

### How do I import another file?

    @import "header.mup"

Paths are relative to the importing file.

### How do I embed a YouTube video?

Use the standard embed:

    ![YouTube thumbnail](https://img.youtube.com/vi/VIDEO_ID/0.jpg){link=https://youtube.com/watch?v=VIDEO_ID}

Or paste an iframe in a code block with `previewable` type.

---

4. Files and Output
-------------------

### Where does the HTML output go?

By default, next to the `.mup` file with the same name:

    document.mup  ->  document.html

### How do I specify a custom output path?

Use the `-o` or `--output` flag:

    mup input.mup -o build/index.html

    mup input.mup --output output/custom.html

### Can I convert multiple files at once?

Not in v0.6.0. Convert them one at a time.

Multiple file support is planned for a future version.

### The output HTML is huge. Why?

Cause: Large document or many charts.

Fix: Split with `@import`. Reduce chart data.

The HTML includes all CSS, JavaScript, and CDN links, so even small
documents produce ~50 KB of HTML.

### Does the output HTML require internet?

Yes, for:

- Charts (Chart.js)
- Math (KaTeX)
- Syntax highlighting (Prism.js)

These are loaded from CDN. For fully offline use, download them
locally.

### Can I edit the HTML after conversion?

Yes, but changes will be lost on next conversion.

Better approach: use custom CSS:

    mup document.mup --css my-style.css

### What encoding does Markup+ use?

UTF-8. Always save your `.mup` files as UTF-8.

### Can I convert Markup+ back to Markdown?

Not in v0.6.0. Markdown export is planned for a future version.

### Can I export to PDF?

Not in v0.6.0. PDF export is planned for a future version.

Workaround: Open the HTML in a browser and print to PDF (Ctrl+P).

---

5. CLI Usage
------------

### What commands are available?

    mup <file>           Convert to HTML
    mup new <name>       Create a new .mup file
    mup open <file>      View in terminal
    mup check <file>     Validate
    mup init [name]      Initialize a project
    mup --help           Show help
    mup --version        Show version

### What options are available?

    -d, --dark           Dark theme
    -l, --light          Light theme (default)
    -r, --rtl            Force right-to-left layout
    --ltr                Force left-to-right layout
    -o, --output <file>  Custom output path
    --css <file>         Custom CSS file
    --debug              Show debug info
    -h, --help           Show help
    -v, --version        Show version

### How do I use multiple options?

Combine them:

    mup docs.mup --dark --rtl -o docs/index.html

### What does "mup check" do?

Validates a file for:

- Undefined variables
- Unbalanced blocks (@if without @endif)
- Empty documents

    mup check file.mup

### What does "mup init" do?

Creates a project structure:

    my-blog/
        docs/
        assets/
        index.mup

Usage:

    mup init              # In current directory
    mup init my-blog      # Create my-blog/ folder

### What does "mup --debug" show?

Shows:

- Node counts by type
- Processing time
- Variables defined
- Footnotes

    mup complex.mup --debug

### Can I use Markup+ as a Python module?

Yes:

    from markup_plus import to_html

    html = to_html("# Hello World")

Or:

    from markup_plus.parser import parse_text
    from markup_plus.renderer import to_html

    doc = parse_text(source)
    html = to_html(source)

---

6. Themes and Customization
---------------------------

### What themes are available?

Built-in:

- Light (default)
- Dark

Ready-made CSS themes:

- Ocean Blue
- Midnight Dark
- Forest Green
- Rose Pink
- Solarized Light
- Nord
- Paper (High Contrast)

### How do I use the dark theme?

    mup file.mup --dark

Or:

    mup file.mup -d

### How do I apply a custom theme?

Create a CSS file:

    :root {
        --accent: #ff6b6b;
    }

Apply it:

    mup document.mup --css my-style.css

### Can I switch themes at runtime?

No. Themes are set at conversion time.

Workaround: Generate two files:

    mup article.mup -o article-light.html
    mup article.mup --dark -o article-dark.html

### What CSS variables can I override?

See CUSTOM-CSS.md for the complete list. Common ones:

    --accent        Primary color
    --bg-page       Page background
    --text-main     Text color
    --border        Border color
    --font-size     Base font size
    --max-width     Max content width

### How do I customize fonts?

Add to your CSS file:

    body {
        font-family: "Inter", sans-serif;
        font-size: 18px;
    }

    h1, h2, h3 {
        font-family: "Playfair Display", Georgia, serif;
    }

### How do I add custom colors?

Override the accent variable:

    :root {
        --accent: #ff6b6b;
        --accent-hover: #e94a4a;
        --accent-soft: rgba(255, 107, 107, 0.1);
    }

### Can I share my theme?

Yes. Save the CSS file and share it. Others can use it with:

    mup document.mup --css my-theme.css

---

7. RTL and Internationalization
-------------------------------

### Which RTL languages are supported?

Persian, Arabic, Hebrew, Urdu, and any language that uses
right-to-left script.

### How does auto RTL detection work?

Markup+ scans the text for RTL characters. If more than 30 percent
of letters are RTL, the entire document becomes RTL.

### How do I force RTL?

    mup file.mup --rtl

### How do I force LTR?

    mup file.mup --ltr

Useful when a document has an English title but is mostly Persian.

### Does auto RTL detection work with mixed content?

Yes. Code blocks, URLs, and emails stay LTR even in RTL documents.

Example:

    # راهنمای پایتون

    برای نصب:

    ```bash
    pip install markup-plus
    ```

The Persian text is RTL, but the bash command is LTR.

### Can I use Persian headings in the TOC?

Yes. Heading anchors support Persian and Arabic:

    ## سلام دنیا      -> #سلام-دنیا

---

8. Performance
--------------

### How fast is Markup+?

Benchmarks:

    Document size    Time
    100 lines        <10 ms
    1,000 lines      <50 ms
    10,000 lines     <500 ms
    100,000 lines    <5 s

### Why is my document slow to convert?

Common causes:

- Very large file (over 10,000 lines)
- Many charts (Chart.js loads for each)
- Deeply nested loops

Fix: Split the document with `@import`.

### Can Markup+ handle large files?

Yes, but performance degrades after 10,000 lines.

Streaming parser is planned for a future version.

### Does the output HTML load slowly?

If it contains many charts or math formulas, yes. Chart.js and KaTeX
need time to render.

Fix: Lazy loading is planned for a future version.

### How do I profile performance?

    python -m cProfile -s cumtime -m markup_plus big.mup

---

9. Troubleshooting
------------------

### "mup: command not found"

**Cause:** CLI not installed or PATH not set.

**Fix:**

    python -m pip install --upgrade markup-plus

Or use the full module path:

    python -m markup_plus file.mup

### "File is not valid UTF-8"

**Cause:** File contains non-UTF-8 characters.

**Fix:** Save the file as UTF-8 in your editor.

- VS Code: Bottom-right, click encoding, Save with Encoding, UTF-8
- Notepad: File, Save As, Encoding: UTF-8

### Variables not replacing

**Cause:** Missing `{ }` or typo.

**Wrong:**

    Hello $name!        # Use curly braces, not dollar
    Hello (name)!       # Use curly braces, not parens
    Hello {Name}!       # Case-sensitive

**Correct:**

    Hello {name}!

### Unbalanced blocks

**Cause:** Missing `@end` or `@endif`.

**Fix:** Every block needs to close:

    Opens With              Closes With
    @if                     @endif (or @elif / @else)
    @each                   @end
    @def                    @end
    @tabs                   @end
    @collapse               @end
    @note/@warning/etc.     @end
    @quote                  @end
    @chart                  @end
    @timeline               @end
    @gallery                @end

Check with:

    mup check file.mup

### Chart not rendering

**Cause:** No internet, or invalid data format.

**Fix:** Ensure data is an array of numbers:

    @chart(type="bar")
    data: [10, 20, 30]
    labels: ["A", "B", "C"]
    @end

**Wrong:**

    data: [10, "twenty", 30]   # Mixed types
    data: 10, 20, 30           # Missing brackets

### Math not rendering

**Cause:** Syntax error in LaTeX.

**Fix:** Check KaTeX syntax at https://katex.org/

### RTL layout not activating

**Cause:** Less than 30 percent RTL characters.

**Fix:** Force it:

    mup file.mup --rtl

### Import not working

**Cause:** Wrong path, circular import, or missing file.

**Fix:** Check with absolute paths. Look for `[Import not found: ...]`
in the output HTML.

### Output HTML is huge

**Cause:** Large document or many charts.

**Fix:** Split with `@import`. Reduce chart data.

### Installer shows SmartScreen warning

**Cause:** Installer is not code-signed.

**Fix:** Click "More info" then "Run anyway". This is normal for
open-source software.

### mup command not found after installer

**Cause:** PATH was not updated in the current Command Prompt.

**Fix:** Close Command Prompt and open a new one. PATH changes
require a new session.

### Changes not visible after conversion

**Cause:** Browser cache.

**Fix:** Hard refresh with Ctrl+F5 (Windows) or Cmd+Shift+R (macOS).

### "Permission denied" on Windows

**Cause:** Trying to write to a protected folder.

**Fix:** Run Command Prompt as Administrator, or choose a different
output folder.

---

10. Contributing
----------------

### How do I contribute?

See CONTRIBUTING.md for full guidelines. In short:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

### Do I need to write code to contribute?

No. You can:

- Report bugs
- Suggest features
- Improve documentation
- Translate the project
- Write tests
- Design (CSS, icons)
- Spread the word

### Where do I report bugs?

Open an issue on GitHub:

    https://github.com/ataee-dev/markup-plus/issues

Include:

- The `.mup` file (or minimal reproduction)
- The command you ran
- The error message
- Your Python version (`python --version`)

### Where do I suggest features?

Open a discussion on GitHub:

    https://github.com/ataee-dev/markup-plus/discussions

### How do I translate the project?

See CONTRIBUTING.md section 13. In short:

1. Create a language folder in `docs/`
2. Translate the files
3. Submit a pull request

### How do I keep my fork in sync?

    git fetch upstream
    git rebase upstream/master
    git push --force-with-lease origin your-branch

### How long does a PR take to be reviewed?

Usually 1-3 days. If no response after 2 weeks, leave a comment to
ping the maintainers.

### Where do contributors get credited?

- In release notes
- In CHANGELOG.md
- In GitHub's contributor list
- Featured in README (for significant contributions)

---

11. Commercial Use and Licensing
--------------------------------

### Can I use Markup+ for commercial projects?

Not without a separate commercial license. Markup+ is released under
the Markup+ Non-Commercial License.

### What counts as commercial use?

- Selling Markup+ or any derivative
- Using Markup+ in a commercial product or service
- Using Markup+ to provide paid services
- Using Markup+ in a for-profit organization for business operations
- Integrating Markup+ into a paid product

### What counts as non-commercial use?

- Personal projects
- Educational use
- Academic research
- Non-profit organizations
- Free and open-source projects

### How do I get a commercial license?

Contact the maintainer:

    hosseinataee2009@gmail.com

Commercial license terms, including fees and scope, will be
negotiated separately.

### What is the license for the output HTML?

The output HTML is generated content. You own the output. The license
applies to Markup+ itself, not to documents you create with it.

### Can I redistribute Markup+?

Yes, for non-commercial use. You must:

- Keep the license file
- Keep copyright notices
- Indicate any modifications
- Not sublicense under different terms

### What about third-party libraries?

Markup+ uses these libraries:

    Library      License
    Prism.js     MIT
    Chart.js     MIT
    KaTeX        MIT

These are governed by their own licenses. This license does not apply
to them.

### Can I use Markup+ in a commercial product if I do not charge for it?

If the product itself is commercial (part of a for-profit business),
you need a commercial license.

If you are using Markup+ for personal, non-commercial purposes, you
do not.

### What happens if I violate the license?

Your rights under the license terminate automatically. You must stop
all use and destroy all copies.

The copyright holder may also take legal action.

### Can the license change?

Yes. The copyright holder may update the license at any time.
Continued use after such updates constitutes acceptance of the new
terms.

### Where can I read the full license?

See the LICENSE file in the repository:

    https://github.com/ataee-dev/markup-plus/blob/master/LICENSE

---

Further Reading
---------------

- README.md -- Project overview
- INSTALL.md -- Installation guide
- GUIDE.md -- Full user guide
- TUTORIAL.md -- Step-by-step tutorial
- CUSTOM-CSS.md -- Customization guide
- DEVELOPER.md -- Developer guide
- CHANGELOG.md -- Version history
- ROADMAP.md -- Future plans
- CONTRIBUTING.md -- Contribution guidelines
- SECURITY.md -- Security policy

---

Contact
-------

- Email: hosseinataee2009@gmail.com
- Repository: https://github.com/ataee-dev/markup-plus
- Issues: https://github.com/ataee-dev/markup-plus/issues
- Discussions: https://github.com/ataee-dev/markup-plus/discussions

---

Last updated: January 2026
Version: 0.6.0

Markup+ Non-Commercial License
Copyright 2026 Hossein Ataee