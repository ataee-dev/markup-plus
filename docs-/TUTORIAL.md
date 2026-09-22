Markup+ Tutorial
================

Version: 0.6.0
Last Updated: January 2026
Audience: Beginners who want to learn Markup+ step by step

A hands-on tutorial that takes you from zero to building a complete
document with Markup+.

---

Table of Contents
-----------------

1. Before You Start
2. Lesson 1: Your First Document
3. Lesson 2: Headings and Text
4. Lesson 3: Lists and Tables
5. Lesson 4: Code Blocks
6. Lesson 5: Links and Images
7. Lesson 6: Variables
8. Lesson 7: Filters
9. Lesson 8: Conditionals
10. Lesson 9: Loops
11. Lesson 10: Components
12. Lesson 11: Alerts and Quotes
13. Lesson 12: Charts and Math
14. Lesson 13: Tabs and Accordions
15. Lesson 14: Front Matter
16. Lesson 15: Table of Contents
17. Lesson 16: Splitting with @import
18. Lesson 17: RTL Support
19. Lesson 18: Custom CSS
20. Final Project: Building a Blog Post
21. Next Steps

---

1. Before You Start
-------------------

### What You Need

- A computer (Windows, macOS, or Linux)
- A text editor (VS Code, Notepad++, or any editor)
- Markup+ installed (see INSTALL.md)

### How to Use This Tutorial

Each lesson has:

- A short explanation
- A code example
- The rendered output
- A practice exercise

Do not just read. Type the examples yourself. Modify them. Break them.
This is how you learn.

### Conventions

- Text in `code font` is Markup+ syntax
- Text in regular font is explanation
- Output is shown after the code

---

2. Lesson 1: Your First Document
--------------------------------

### Step 1: Create a File

Open Command Prompt and run:

    mup new hello

This creates a file called `hello.mup`.

### Step 2: Open the File

Open `hello.mup` in your text editor.

You will see starter content like:

    # Hello World

    This is a Markup+ document.

### Step 3: Convert to HTML

In Command Prompt:

    mup hello.mup

This creates `hello.html`.

### Step 4: Open in Browser

    start hello.html       (Windows)
    open hello.html        (macOS)
    xdg-open hello.html    (Linux)

You should see a nicely formatted page with the heading "Hello World".

### Congratulations

You have created your first Markup+ document.

### Exercise

Change the text to your name. Convert again. See the result.

---

3. Lesson 2: Headings and Text
------------------------------

### Headings

Use `#` symbols for headings. More `#` means smaller heading.

    # Heading 1
    ## Heading 2
    ### Heading 3
    #### Heading 4
    ##### Heading 5
    ###### Heading 6

Output:

- Heading 1 is the largest
- Heading 6 is the smallest

### Text Formatting

    **Bold text**
    *Italic text*
    ***Bold and italic***
    ~~Strikethrough~~
    `Inline code`

Output:

- **Bold text** is bold
- *Italic text* is italic
- ***Bold and italic*** is both
- ~~Strikethrough~~ has a line through it
- `Inline code` is monospace

### Combine Them

    This is **bold** and this is *italic*.

    You can have **bold with *italic* inside**.

### Paragraphs

Separate paragraphs with a blank line:

    First paragraph.

    Second paragraph.

    Third paragraph.

### Exercise

Create a document with:

- An H1 heading with your name
- An H2 heading "About Me"
- A paragraph with bold text
- A paragraph with italic text

---

4. Lesson 3: Lists and Tables
-----------------------------

### Unordered Lists

    - First item
    - Second item
    - Third item

Output:

- First item
- Second item
- Third item

Also works with `*` or `+`.

### Ordered Lists

    1. First step
    2. Second step
    3. Third step

Output:

1. First step
2. Second step
3. Third step

### Task Lists

    - [x] Completed task
    - [ ] Pending task
    - [x] Another done task

Output:

- Checkbox for completed
- Empty checkbox for pending
- Checkbox for completed

### Tables

    | Name | Age | City    |
    |------|-----|---------|
    | Ali  | 30  | Tehran  |
    | Sara | 25  | Isfahan |

Output: A table with three columns.

With alignment:

    | Left | Center | Right |
    |:-----|:------:|------:|
    | A    | B      | C     |

Rules:

- `:---` is left aligned
- `:---:` is center aligned
- `---:` is right aligned

### Exercise

Create a table with your favorite movies:

| Title | Year | Rating |
|-------|-----:|:------:|
| ...   | ...  | ...    |

---

5. Lesson 4: Code Blocks
------------------------

### Inline Code

    Use `print("Hello")` to print text.

Output: Use `print("Hello")` to print text.

### Code Blocks

Wrap code in triple backticks:

    ```python
    def hello(name):
        print(f"Hello, {name}!")

    hello("World")
    ```

Output: A formatted code block with syntax highlighting.

### Code Block Options

With title:

    ```python {title="app.py"}
    print("Hello")
    ```

With line numbers:

    ```python {linenos}
    print("Hello")
    ```

With highlighted lines:

    ```python {hl=[2,4]}
    def add(a, b):
        return a + b

    result = add(2, 3)
    ```

Lines 2 and 4 are highlighted.

### Why Code Blocks Matter

- Syntax highlighting makes code readable
- Copy button lets readers copy with one click
- Download button saves the code as a file
- Live preview for HTML, CSS, JavaScript

### Exercise

Write a code block in your favorite programming language.

---

6. Lesson 5: Links and Images
-----------------------------

### Links

    [Click here](https://example.com)

Output: Click here

With title (shown on hover):

    [Click here](https://example.com "Visit example")

Automatic links:

    <https://example.com>

Output: https://example.com

### Images

Basic image:

    ![Alt text](image.jpg)

With size:

    ![Alt](image.jpg){width=400}

With alignment:

    ![Alt](image.jpg){align=center}
    ![Alt](image.jpg){align=left}
    ![Alt](image.jpg){align=right}

With caption:

    ![Alt](image.jpg){caption="Figure 1: A beautiful sunset"}

### Complete Example

    ![Mountain](mountain.jpg){width=600 align=center caption="Mount Everest" desc="Photo taken at sunrise"}

This creates:

- Image with width 600 pixels
- Centered
- Caption below
- Description in lightbox

### Image Galleries

    @gallery {columns=3}
    ![Sunset](sunset.jpg){caption="Sunset"}
    ![Mountain](mountain.jpg){caption="Mountain"}
    ![Ocean](ocean.jpg){caption="Ocean"}
    @end

Creates a grid of three images.

Click any image to open in lightbox.

### Exercise

Add an image to your document with a caption.

---

7. Lesson 6: Variables
----------------------

### What Are Variables?

Variables store values you can reuse. Change once, change everywhere.

### Define a Variable

    @let name = "Ali"
    @let age = 30
    @let city = "Tehran"

### Use a Variable

    Hello **{name}**! You are {age} years old and live in {city}.

Output:

Hello **Ali**! You are 30 years old and live in **Tehran**.

### Supported Types

    @let text = "Hello"        String
    @let number = 42           Integer
    @let decimal = 3.14        Float
    @let flag = true           Boolean
    @let nothing = null        Null
    @let list = [1, 2, 3]      Array

### Why Variables Are Useful

Imagine writing a document about your project:

Without variables:

    Version 1.0 was released. See version 1.0 changelog.
    Download version 1.0 from version 1.0 page.

With variables:

    @let version = "1.0"

    Version {version} was released. See version {version} changelog.
    Download version {version} from version {version} page.

Now change `@let version = "1.0"` to `"2.0"` and the whole document
updates.

### Exercise

Create three variables:

- Your name
- Your age
- Your city

Use them in a sentence.

---

8. Lesson 7: Filters
--------------------

### What Are Filters?

Filters transform variable output.

### Basic Filters

    @let name = "markup plus"

    {name}                  -> markup plus
    {name|upper}            -> MARKUP PLUS
    {name|lower}            -> markup plus
    {name|capitalize}       -> Markup plus
    {name|title}            -> Markup Plus
    {name|reverse}          -> sulp pukram
    {name|length}           -> 11

### Chain Filters

    {name|upper|reverse}    -> SULP PUKRAM

First `upper`, then `reverse`.

### Filters on Arrays

    @let items = ["a", "b", "c"]

    {items|length}          -> 3
    {items|reverse}         -> ["c", "b", "a"]

### Practical Example

    @let title = "my first blog post"

    # {title|title}

Output:

# My First Blog Post

### Exercise

Create a variable and apply three filters in a chain.

---

9. Lesson 8: Conditionals
-------------------------

### What Are Conditionals?

Show or hide content based on a condition.

### Basic If

    @let version = "1.0"

    @if version == "1.0"
    This is the stable release!
    @endif

Output: "This is the stable release!"

### If Else

    @if is_logged_in
    Welcome back!
    @else
    Please log in.
    @endif

### If Elif Else

    @let score = 85

    @if score >= 90
    Excellent
    @elif score >= 70
    Good
    @elif score >= 50
    Average
    @else
    Needs improvement
    @endif

Output: "Good" (since 85 is between 70 and 90).

### Operators

    Operator    Meaning
    ==          Equal
    !=          Not equal
    >           Greater than
    <           Less than
    >=          Greater or equal
    <=          Less or equal

### Practical Example

    @let environment = "production"

    @if environment == "production"
    ### Production Notes

    Deploy with caution. Test everything first.
    @else
    ### Development Notes

    Experiment freely. Break things.
    @endif

### Exercise

Create a conditional that shows different content for weekday and
weekend.

---

10. Lesson 9: Loops
-------------------

### What Are Loops?

Repeat content for each item in a list.

### Basic Loop

    @let fruits = ["apple", "banana", "cherry"]

    @each fruit in fruits
    - {fruit}
    @end

Output:

- apple
- banana
- cherry

### Loop with Index

    @let items = ["first", "second", "third"]

    @each i, item in items
    {i}. {item}
    @end

Output:

1. first
2. second
3. third

### Nested Loops

    @let matrix = [[1, 2], [3, 4]]

    @each row in matrix
    @each cell in row
    - {cell}
    @end
    @end

Output:

- 1
- 2
- 3
- 4

### Loop with Condition

    @let numbers = [1, 2, 3, 4, 5, 6]

    @each num in numbers
    @if num > 3
    - {num} is greater than 3
    @endif
    @end

Output:

- 4 is greater than 3
- 5 is greater than 3
- 6 is greater than 3

### Inline Array

You can loop over an array defined inline:

    @each lang in ["Python", "JavaScript", "Rust"]
    - **{lang}**
    @end

### Practical Example

    @let team = ["Ali", "Sara", "Reza", "Maryam"]

    ## Team Members

    @each member in team
    - {member}
    @end

### Exercise

Create a loop that prints numbers from 1 to 10, but only even numbers.

---

11. Lesson 10: Components
-------------------------

### What Are Components?

Reusable templates. Define once, use many times.

### Define a Component

    @def Card(title, body)
    > **{title}**
    >
    > {body}
    @end

### Use the Component

    @Card(title="Hello", body="This is a card.")

    @Card(title="News", body="Breaking news here!")

    @Card(title="Info", body="For more details, see the docs.")

Each call creates a new card with different content.

### More Complex Component

    @def User(name, email, role)
    ### {name}

    - **Email:** {email}
    - **Role:** {role}
    @end

    @User(name="Ali", email="ali@example.com", role="Admin")

    @User(name="Sara", email="sara@example.com", role="Editor")

### Why Components Are Useful

Without components, you repeat the same structure:

    > **Hello**
    >
    > This is a card.

    > **News**
    >
    > Breaking news here!

With components:

    @Card(title="Hello", body="This is a card.")
    @Card(title="News", body="Breaking news here!")

Cleaner and easier to maintain.

### Exercise

Create a component called `Product` that takes name, price, and
description.

---

12. Lesson 11: Alerts and Quotes
--------------------------------

### Alert Types

Five alert types for different purposes:

    @note
    This is a note. Use it for additional information.
    @end

    @warning
    This is a warning. Something might go wrong.
    @end

    @tip
    This is a tip. A helpful shortcut or suggestion.
    @end

    @danger
    This is danger. Critical -- could cause damage.
    @end

    @success
    This is success. Operation completed successfully.
    @end

Output:

- Note: blue box with info icon
- Warning: yellow box with warning icon
- Tip: green box with lightbulb icon
- Danger: red box with siren icon
- Success: green box with checkmark icon

### Alerts with Content

Alerts can contain anything:

    @warning
    Careful with this command:

    ```bash
    rm -rf /
    ```

    It will delete everything!
    @end

### Rich Quotes

    @quote(author="Albert Einstein")
    Imagination is more important than knowledge.
    @end

Output: A styled quote with author attribution.

With source:

    @quote(author="Hafez", source="Divan")
    هر که را جامه ز عشقی چاک شد
    او ز عشق مصطفی بی‌باک شد
    @end

### Using Braces

    @quote{author="Douglas Adams", source="Hitchhiker's Guide"}
    Don't panic, and always carry a towel.
    @end

Same result, different syntax.

### Exercise

Create one alert of each type.

---

13. Lesson 12: Charts and Math
------------------------------

### Bar Chart

    @chart(type="bar" title="Monthly Sales")
    data: [100, 250, 180, 320]
    labels: ["Jan", "Feb", "Mar", "Apr"]
    @end

Output: A bar chart with four bars.

### Line Chart

    @chart(type="line" title="User Growth")
    data: [10, 50, 120, 300, 750]
    labels: ["2020", "2021", "2022", "2023", "2024"]
    @end

### Pie Chart

    @chart(type="pie" title="Browser Share")
    data: [55, 20, 15, 10]
    labels: ["Chrome", "Firefox", "Safari", "Others"]
    @end

### Doughnut Chart

    @chart(type="doughnut" title="OS Distribution")
    data: [65, 20, 10, 5]
    labels: ["Windows", "macOS", "Linux", "Other"]
    @end

### Math Formulas

Block formula (centered, on its own line):

    $$ E = mc^2 $$

Inline formula (inside text):

    The famous formula $E = mc^2$ changed physics.

### More Math Examples

Quadratic formula:

    $$ x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} $$

Summation:

    $$ \sum_{i=1}^{n} i = \frac{n(n+1)}{2} $$

Integral:

    $$ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} $$

### Notes

- Charts use Chart.js (loaded from CDN)
- Math uses KaTeX (loaded from CDN)
- Both require internet connection on first render

### Exercise

Create a chart showing your weekly schedule (hours per day).

---

14. Lesson 13: Tabs and Accordions
----------------------------------

### Tabs

Show multiple code samples in tabs:

    @tabs
    @tab "Python"
    ```python
    print("Hello from Python")
    ```
    @end

    @tab "JavaScript"
    ```javascript
    console.log("Hello from JS");
    ```
    @end

    @tab "Bash"
    ```bash
    echo "Hello from Bash"
    ```
    @end
    @end

Output: Three tabs at the top. Click to switch.

### When to Use Tabs

- Show same example in multiple languages
- Show different installation instructions per OS
- Show different configuration options

### Accordions

Collapsible sections (great for FAQs):

    @collapse
    @item "What is Markup+?"
    Markup+ is a modern markup language.
    @end

    @item "How do I install it?"
    Use pip:

    ```bash
    pip install markup-plus
    ```
    @end

    @item "Is it free?"
    Yes! Non-commercial use is free.
    @end
    @end

Output: Three collapsible sections. Click to expand.

### When to Use Accordions

- FAQs
- Long content that should be hidden by default
- Optional details
- Step-by-step guides

### Exercise

Create a FAQ with three questions.

---

15. Lesson 14: Front Matter
---------------------------

### What Is Front Matter?

Metadata at the top of your file, between `---` lines.

### Basic Front Matter

    ---
    title: My Article
    author: Ali Rezaei
    date: 2025-01-15
    ---

    # {title}

    By **{author}** -- {date}

### How It Works

1. Lines between `---` are parsed as metadata
2. Each line is `key: value`
3. All keys become variables
4. Use them anywhere with `{key}`

### Common Fields

    Field       Purpose
    title       Document title
    author      Author name
    date        Publication date
    version     Document version
    tags        Comma-separated tags

You can add any custom field.

### Practical Example

    ---
    title: Getting Started with Python
    author: Ali
    date: 2025-01-15
    version: 1.0
    ---

    # {title}

    **Author:** {author}
    **Date:** {date}
    **Version:** {version}

    ## Introduction

    Welcome to version {version} of this guide.

### Exercise

Add front matter to your document with title, author, and date.

---

16. Lesson 15: Table of Contents
--------------------------------

### Basic TOC

    @toc

Generates a table of contents from all headings in the document.

### With Custom Title

    @toc {title="Contents"}

    @toc {title="On this page"}

    @toc {title="فهرست"}

### How It Works

1. Scans all headings (H1 to H6)
2. Respects hierarchy
3. Creates clickable links
4. Auto-updates when you add headings

### Practical Example

    ---
    title: My Book
    ---

    # {title}

    @toc

    ## Chapter 1

    Content of chapter 1.

    ## Chapter 2

    Content of chapter 2.

    ### Section 2.1

    Nested section.

Output: A TOC with links to Chapter 1, Chapter 2, and Section 2.1.

### Exercise

Add a TOC to a document with at least three headings.

---

17. Lesson 16: Splitting with @import
-------------------------------------

### Why Split Documents?

- Large files are hard to edit
- Reusable sections (header, footer)
- Multiple authors can work on different parts

### Create Separate Files

**header.mup:**

    # My Site

    Welcome to my site!

**footer.mup:**

    ---

    Copyright 2025 My Company

**main.mup:**

    @import "header.mup"

    ## Content Section

    This is the main content.

    @import "footer.mup"

### When You Convert main.mup

    mup main.mup

Markup+ reads the imports and combines everything into one HTML file.

### Rules

- Paths are relative to the importing file
- Can import from subdirectories: `@import "parts/intro.mup"`
- Circular imports are prevented
- Missing files show a warning

### Exercise

Create three files: `header.mup`, `body.mup`, `footer.mup`.
Import them into `main.mup`.

---

18. Lesson 17: RTL Support
--------------------------

### Automatic Detection

Markup+ automatically detects RTL languages:

- Persian (فارسی)
- Arabic (العربية)
- Hebrew (עברית)
- Urdu (اردو)

If more than 30 percent of characters are RTL, the entire document
becomes RTL.

### Example

    # سلام دنیا

    این یک متن **فارسی** است.

Automatically renders:

- Right-to-left direction
- Right-aligned text
- Persian-friendly fonts

### Manual Control

Force RTL:

    mup file.mup --rtl

Force LTR:

    mup file.mup --ltr

### Mixed Content

Code blocks stay LTR even in RTL documents.

    # راهنمای پایتون

    برای نصب:

    ```bash
    pip install markup-plus
    ```

Output: Persian text is RTL, but the bash command is LTR.

### Exercise

Create a Persian document and convert it.

---

19. Lesson 18: Custom CSS
-------------------------

### Create a CSS File

Create `my-style.css` next to your `.mup` file:

    :root {
        --accent: #ff6b6b;
        --bg-page: #1a1a2e;
        --text-main: #eaeaea;
    }

### Convert with CSS

    mup document.mup --css my-style.css

Your document now uses the custom colors.

### CSS Variables

Common variables:

    Variable        Purpose
    --accent        Primary color
    --bg-page       Page background
    --text-main     Text color
    --border        Border color
    --font-size     Base font size
    --max-width     Max content width

### Ready-Made Themes

Copy one of these into a `.css` file:

Ocean Blue:

    :root {
        --accent: #3b82f6;
        --bg-page: #ffffff;
        --text-main: #0f172a;
    }

Midnight Dark:

    :root {
        --accent: #a78bfa;
        --bg-page: #0f0f1a;
        --text-main: #e8e8f0;
    }

Forest Green:

    :root {
        --accent: #10b981;
        --bg-page: #f0fdf4;
        --text-main: #064e3b;
    }

For more, see CUSTOM-CSS.md.

### Exercise

Create a custom theme with your favorite colors.

---

20. Final Project: Building a Blog Post
---------------------------------------

Let us build a complete blog post using everything we learned.

### Step 1: Create the File

    mup new my-blog-post

### Step 2: Write the Front Matter

    ---
    title: Getting Started with Markup+
    author: Ali Rezaei
    date: 2025-01-15
    ---

### Step 3: Add the Title and Intro

    # {title}

    By **{author}** | {date}

    Markup+ is a modern markup language. In this post, we will learn
    how to use it.

### Step 4: Add a Table of Contents

    @toc

### Step 5: Add Sections

    ## Installation

    @note
    You need Python 3.9 or higher.
    @end

    Install with pip:

    ```bash
    pip install markup-plus
    ```

    ## Features

    @each feature in ["Variables", "Loops", "Charts", "Math"]
    ### {feature}

    Details about {feature|lower}...
    @end

    ## Example Chart

    @chart(type="bar" title="Markup+ Features by Category")
    data: [15, 8, 6, 5, 4, 7]
    labels: ["Core", "Logic", "Charts", "Math", "Tabs", "Other"]
    @end

    ## Tips

    @tip
    Use components to avoid repeating yourself.
    @end

    @warning
    Do not use complex nested loops in large documents.
    @end

    ## Conclusion

    @success
    You now know the basics of Markup+!
    @end

### Step 6: Convert

    mup my-blog-post.mup

### Step 7: View

    start my-blog-post.html

You now have a complete blog post with:

- Front matter
- TOC
- Code blocks
- Variables
- Loops
- Alerts
- Charts
- Tips

### Congratulations

You have completed the tutorial. You are now a Markup+ user.

---

21. Next Steps
--------------

### Learn More

- **GUIDE.md** -- Complete reference of all features
- **CUSTOM-CSS.md** -- Customize the appearance
- **FAQ.md** -- Common questions
- **DEVELOPER.md** -- If you want to contribute

### Practice Ideas

1. Convert an existing Markdown document to Markup+
2. Build a documentation site for a project
3. Write a technical blog post
4. Create a personal portfolio page
5. Build a report with charts and tables

### Join the Community

- Repository: https://github.com/ataee-dev/markup-plus
- Issues: https://github.com/ataee-dev/markup-plus/issues
- Discussions: https://github.com/ataee-dev/markup-plus/discussions
- Email: hosseinataee2009@gmail.com

### Contribute

If you found a bug or want a new feature:

1. Open an issue on GitHub
2. Or submit a pull request (see CONTRIBUTING.md)

### Share Your Work

If you build something with Markup+, share it. We would love to see it.

---

Quick Reference
---------------

Everything in one page.

### Basic Syntax

    # Heading 1
    ## Heading 2
    **bold**
    *italic*
    ~~strikethrough~~
    `inline code`
    - list item
    1. ordered item
    > blockquote
    ---
    [link](url)
    ![alt](image.jpg)
    | table | cells |

### Directives

    @let name = "value"           Variable
    {name}                        Use variable
    {name|upper}                  Filter
    @if condition                 Conditional
    @elif condition
    @else
    @endif
    @each item in list            Loop
    @end
    @def Name(param)              Component
    @end
    @Name(param="value")          Use component
    @import "file.mup"            Import
    @toc                          Table of contents
    @note / @warning / @tip       Alert
    @danger / @success
    @end
    @quote(author="...")          Quote
    @end
    @chart(type="bar")            Chart
    data: [1, 2, 3]
    labels: ["A", "B", "C"]
    @end
    @tabs / @tab "Title"          Tabs
    @collapse / @item "Title"     Accordion
    @timeline                     Timeline
    @gallery {columns=3}          Gallery
    @# comment                    Comment
    $$ math $$                    Math (block)
    $math$                        Math (inline)

### CLI

    mup file.mup                  Convert
    mup new name                  Create new
    mup open file.mup             View
    mup check file.mup            Validate
    mup init                      New project
    mup file.mup --dark           Dark theme
    mup file.mup --rtl            Force RTL
    mup file.mup --css style.css  Custom CSS
    mup file.mup -o out.html      Custom output
    mup --version                 Show version

---

Further Reading
---------------

- GUIDE.md -- Complete user guide
- CUSTOM-CSS.md -- Customization
- FAQ.md -- Frequently asked questions
- DEVELOPER.md -- For contributors
- CHANGELOG.md -- Version history
- ROADMAP.md -- Future plans

External Resources:

- Markdown Guide: https://www.markdownguide.org/
- KaTeX: https://katex.org/
- Chart.js: https://www.chartjs.org/

---

Contact
-------

- Email: hosseinataee2009@gmail.com
- Repository: https://github.com/ataee-dev/markup-plus
- Issues: https://github.com/ataee-dev/markup-plus/issues

---

Last updated: January 2026
Version: 0.6.0

Markup+ Non-Commercial License
Copyright 2026 Hossein Ataee