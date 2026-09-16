"""
Markup+ Parser

Converts tokens into an Abstract Syntax Tree (AST).

Phase 1:  Headings, Paragraphs
Phase 2:  Lists, Blockquotes, HR, Code blocks, Images, Galleries
Phase 3:  Links, Tables, Task Lists, Front Matter, TOC, Footnotes
Phase 4:  Variables, Logic (if/elif/else), Loops (each), Comments
Phase 5:  Components, Charts, Math, Tabs, Collapse, Alerts, Quotes, Timeline
"""

import re
from typing import List, Any

from .ast import (
    AlertBlock,
    BlockQuote,
    ChartBlock,
    CodeBlock,
    CollapseBlock,
    ComponentCall,
    ComponentDef,
    Document,
    EachBlock,
    GalleryBlock,
    Heading,
    HorizontalRule,
    IfBlock,
    ImageBlock,
    ImportBlock,
    ListBlock,
    MathBlock,
    Paragraph,
    QuoteBlock,
    TableBlock,
    TabsBlock,
    TimelineBlock,
    TOCBlock,
    VariableDef,
)
from .lexer import Lexer, Token


# ============================================================
# Regex patterns
# ============================================================

RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RE_UL_ITEM = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
RE_TASK_ITEM = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(.+?)\s*$")
RE_OL_ITEM = re.compile(r"^\s*\d+\.\s+(.+?)\s*$")
RE_HR = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
RE_BLOCKQUOTE = re.compile(r"^\s*>\s?(.*)$")
RE_CODE_FENCE = re.compile(r"^\s*```\s*(\w*)\s*(?:\{(.+?)\})?\s*$")
RE_IMAGE = re.compile(
    r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'
    r'(?:\{([^}]*)\})?\s*$'
)
RE_GALLERY_START = re.compile(r"^@gallery(?:\s*\{([^}]*)\})?\s*$")
RE_TABLE_LINE = re.compile(r"^\s*\|.*\|\s*$")
RE_TABLE_SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
RE_FRONT_MATTER_START = re.compile(r"^---\s*$")
RE_FRONT_MATTER_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.+?)\s*$")
RE_TOC = re.compile(r"^@toc(?:\s*\{([^}]*)\})?\s*$")
RE_FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:\s*(.+?)\s*$")

# Phase 4: Logic directives
RE_LET = re.compile(r"^@let\s+([A-Za-z_][\w]*)\s*=\s*(.+?)\s*$")
RE_IF = re.compile(r"^@if\s+(.+?)\s*$")
RE_ELIF = re.compile(r"^@elif\s+(.+?)\s*$")
RE_ELSE = re.compile(r"^@else\s*$")
RE_ENDIF = re.compile(r"^@endif\s*$")
RE_EACH = re.compile(r"^@each\s+(?:(\w+)\s*,\s*)?(\w+)\s+in\s+(.+?)\s*$")
RE_END = re.compile(r"^@end\s*$")
RE_COMMENT = re.compile(r"^@#(.*)$")

# Phase 5: Rich features
# Accept both `(...)` and `{...}` for options
RE_COMPONENT_DEF = re.compile(r"^@def\s+(\w+)\s*(?:[\(\{]([^\)\}]*)[\)\}])?\s*$")
RE_COMPONENT_CALL = re.compile(r"^@([A-Z]\w+)\s*[\(\{]([^\)\}]*)[\)\}]\s*$")
RE_CHART = re.compile(r"^@chart\s*(?:[\(\{]([^\)\}]*)[\)\}])?\s*$")
RE_MATH_BLOCK = re.compile(r"^\$\$\s*(.+?)\s*\$\$\s*$")
RE_TABS = re.compile(r"^@tabs\s*$")
RE_TAB = re.compile(r'^@tab\s+"([^"]+)"\s*$')
RE_COLLAPSE = re.compile(r"^@collapse\s*$")
RE_ITEM = re.compile(r'^@item\s+"([^"]+)"\s*$')
RE_ALERT = re.compile(r"^@(note|warning|tip|danger|success)\s*$")

# @quote has 3 forms:
#   1. @quote(author="...", source="...")   - parenthesized
#   2. @quote{author="...", source="..."}   - braced
#   3. @quote                                - plain
RE_QUOTE_PAREN = re.compile(r"^@quote\s*\((.*)\)\s*$")
RE_QUOTE_BRACE = re.compile(r"^@quote\s*\{(.*)\}\s*$")
RE_QUOTE_PLAIN = re.compile(r"^@quote\s*$")

RE_TIMELINE = re.compile(r"^@timeline\s*$")
RE_TIMELINE_EVENT = re.compile(r"^(\d{4}(?:-\d{2})?(?:-\d{2})?)\s*:\s*(.+?)\s*$")
RE_IMPORT = re.compile(r'^@import\s+"([^"]+)"\s*$')

class Parser:
    """Parse a list of tokens into a Document AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self._variables: dict = {}

    # --------------------------------------------------------
    # Main entry
    # --------------------------------------------------------

    def parse(self) -> Document:
        doc = Document()

        # 1. Parse front matter
        self._parse_front_matter(doc)

        # 2. Collect footnotes
        self._collect_footnotes(doc)

        # 3. Parse main content
        self.pos = getattr(doc, "_content_start", 0)
        doc.children = self._parse_blocks(stop_at=set())

        # 4. Save collected variables
        doc.variables = dict(self._variables)

        # 5. Assign heading slugs
        self._assign_heading_slugs(doc)

        return doc

    # --------------------------------------------------------
    # Block parsing (recursive)
    # --------------------------------------------------------

    def _parse_blocks(self, stop_at: set) -> List:
        """Parse blocks until one of the stop_at keywords is found."""
        children = []

        while not self._is_at_end():
            token = self._peek()
            line = token.value
            stripped = line.strip()

            # Check stop keywords
            if stop_at:
                if "@elif" in stop_at and RE_ELIF.match(stripped):
                    return children
                if "@else" in stop_at and RE_ELSE.match(stripped):
                    return children
                if "@endif" in stop_at and RE_ENDIF.match(stripped):
                    return children
                if "@end" in stop_at and RE_END.match(stripped):
                    return children

            # EOF
            if token.type == "EOF":
                return children

            # Blank line
            if stripped == "":
                self._advance()
                continue

            # Comment
            if RE_COMMENT.match(stripped):
                self._advance()
                continue

            # Footnote def (skip)
            if RE_FOOTNOTE_DEF.match(stripped):
                self._advance()
                continue

            # @let — variable definition
            m = RE_LET.match(stripped)
            if m:
                var_name = m.group(1)
                raw_value = m.group(2)
                value = self._parse_value(raw_value)
                self._variables[var_name] = value
                children.append(VariableDef(
                    name=var_name,
                    value=value,
                    raw_value=raw_value,
                    line=token.line,
                ))
                self._advance()
                continue

            # @def (component definition)
            m = RE_COMPONENT_DEF.match(stripped)
            if m:
                children.append(self._parse_component_def(
                    m.group(1), m.group(2) or "", token.line
                ))
                continue

            # @import
            m = RE_IMPORT.match(stripped)
            if m:
                children.append(ImportBlock(path=m.group(1), line=token.line))
                self._advance()
                continue

            # @if
            m = RE_IF.match(stripped)
            if m:
                children.append(self._parse_if(m.group(1), token.line))
                continue

            # @each
            m = RE_EACH.match(stripped)
            if m:
                children.append(self._parse_each(
                    m.group(1), m.group(2), m.group(3), token.line
                ))
                continue

            # @chart
            m = RE_CHART.match(stripped)
            if m:
                children.append(self._parse_chart(m.group(1), token.line))
                continue

            # Math block $$ ... $$
            m = RE_MATH_BLOCK.match(stripped)
            if m:
                children.append(MathBlock(
                    latex=m.group(1), display=True, line=token.line
                ))
                self._advance()
                continue

            # @tabs
            if RE_TABS.match(stripped):
                children.append(self._parse_tabs(token.line))
                continue

            # @collapse
            if RE_COLLAPSE.match(stripped):
                children.append(self._parse_collapse(token.line))
                continue

            # @note / @warning / @tip / @danger / @success
            m = RE_ALERT.match(stripped)
            if m:
                children.append(self._parse_alert(m.group(1), token.line))
                continue

            # @quote — three forms: (), {}, or plain
            m_paren = RE_QUOTE_PAREN.match(stripped)
            m_brace = RE_QUOTE_BRACE.match(stripped)
            
            if m_paren or m_brace or RE_QUOTE_PLAIN.match(stripped):
                options_str = ""
                if m_paren:
                    options_str = m_paren.group(1)
                elif m_brace:
                    options_str = m_brace.group(1)
                
                children.append(self._parse_quote(options_str, token.line))
                continue

            # @timeline
            if RE_TIMELINE.match(stripped):
                children.append(self._parse_timeline(token.line))
                continue

            # Code fence
            m = RE_CODE_FENCE.match(line)
            if m:
                children.append(
                    self._parse_code_block(m.group(1), m.group(2), token.line)
                )
                continue

            # Gallery
            m = RE_GALLERY_START.match(stripped)
            if m:
                children.append(self._parse_gallery(m.group(1), token.line))
                continue

            # TOC
            m = RE_TOC.match(stripped)
            if m:
                options = self._parse_inline_options(m.group(1) or "")
                children.append(TOCBlock(
                    title=options.get("title", ""),
                    line=token.line,
                ))
                self._advance()
                continue

            # Table
            if self._is_table_start():
                children.append(self._parse_table())
                continue

            # Image
            m = RE_IMAGE.match(stripped)
            if m:
                children.append(self._parse_image(m, token.line))
                self._advance()
                continue

            # HR
            if RE_HR.match(line):
                children.append(HorizontalRule(line=token.line))
                self._advance()
                continue

            # Heading
            m = RE_HEADING.match(line)
            if m:
                children.append(Heading(
                    level=len(m.group(1)),
                    text=m.group(2),
                    line=token.line,
                ))
                self._advance()
                continue

            # Blockquote
            if RE_BLOCKQUOTE.match(line):
                children.append(self._parse_blockquote())
                continue

            # Task list
            if RE_TASK_ITEM.match(line):
                children.append(self._parse_task_list())
                continue

            # UL
            if RE_UL_ITEM.match(line):
                children.append(self._parse_ul())
                continue

            # OL
            if RE_OL_ITEM.match(line):
                children.append(self._parse_ol())
                continue

            # @ComponentCall(...) — after all lowercase @ directives
            m = RE_COMPONENT_CALL.match(stripped)
            if m:
                children.append(self._parse_component_call(
                    m.group(1), m.group(2), token.line
                ))
                self._advance()
                continue

            # Paragraph
            children.append(Paragraph(text=line, line=token.line))
            self._advance()

        return children

    # --------------------------------------------------------
    # Phase 5: Rich feature parsers
    # --------------------------------------------------------

    def _parse_component_def(self, name: str, params_str: str, start_line: int) -> ComponentDef:
        """Parse @def Name(param1, param2) ... @end"""
        self._advance()
        params = []
        if params_str.strip():
            params = [p.strip() for p in params_str.split(",") if p.strip()]

        children = self._parse_blocks(stop_at={"@end"})
        if not self._is_at_end() and RE_END.match(self._peek().value.strip()):
            self._advance()

        return ComponentDef(name=name, params=params, children=children, line=start_line)

    def _parse_component_call(self, name: str, args_str: str, start_line: int) -> ComponentCall:
        """Parse @Name(key=value, ...)"""
        args = {}
        if args_str.strip():
            pattern = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^,\s]+))')
            for m in pattern.finditer(args_str):
                key = m.group(1)
                value = m.group(2) or m.group(3) or m.group(4) or ""
                args[key] = value
        return ComponentCall(name=name, args=args, line=start_line)

    def _parse_chart(self, options_str: str, start_line: int) -> ChartBlock:
        """Parse @chart(...) or @chart{...} with data/labels."""
        self._advance()
        options = self._parse_inline_options(options_str or "")
        chart_type = options.get("type", "bar")
        title = options.get("title", "")
        color = options.get("color", "")

        data = []
        labels = []

        while not self._is_at_end():
            line = self._peek().value.strip()
            if RE_END.match(line):
                self._advance()
                break

            m = re.match(r"^data\s*:\s*\[(.+?)\]\s*$", line)
            if m:
                data_str = m.group(1)
                data = [
                    self._parse_value(v.strip())
                    for v in self._split_top_level(data_str, ",")
                    if v.strip()
                ]
                self._advance()
                continue

            m = re.match(r"^labels\s*:\s*\[(.+?)\]\s*$", line)
            if m:
                labels_str = m.group(1)
                labels = [
                    str(self._parse_value(v.strip()))
                    for v in self._split_top_level(labels_str, ",")
                    if v.strip()
                ]
                self._advance()
                continue

            self._advance()

        return ChartBlock(
            chart_type=chart_type,
            data=data,
            labels=labels,
            title=title,
            color=color,
            line=start_line,
        )

    def _parse_tabs(self, start_line: int) -> TabsBlock:
        """Parse @tabs @tab "Title" ... @end @end"""
        self._advance()
        tabs = []
        while not self._is_at_end():
            line = self._peek().value.strip()
            if RE_END.match(line):
                self._advance()
                break

            m = RE_TAB.match(line)
            if m:
                title = m.group(1)
                self._advance()
                children = self._parse_blocks(stop_at={"@end"})
                if not self._is_at_end() and RE_END.match(self._peek().value.strip()):
                    self._advance()
                tabs.append((title, children))
                continue

            self._advance()

        return TabsBlock(tabs=tabs, line=start_line)

    def _parse_collapse(self, start_line: int) -> CollapseBlock:
        """Parse @collapse @item "Title" ... @end @end"""
        self._advance()
        items = []
        while not self._is_at_end():
            line = self._peek().value.strip()
            if RE_END.match(line):
                self._advance()
                break

            m = RE_ITEM.match(line)
            if m:
                title = m.group(1)
                self._advance()
                children = self._parse_blocks(stop_at={"@end"})
                if not self._is_at_end() and RE_END.match(self._peek().value.strip()):
                    self._advance()
                items.append((title, children))
                continue

            self._advance()

        return CollapseBlock(items=items, line=start_line)

    def _parse_alert(self, alert_type: str, start_line: int) -> AlertBlock:
        """Parse @note / @warning / @tip / @danger / @success ... @end"""
        self._advance()
        children = self._parse_blocks(stop_at={"@end"})
        if not self._is_at_end() and RE_END.match(self._peek().value.strip()):
            self._advance()
        return AlertBlock(alert_type=alert_type, children=children, line=start_line)

    def _parse_quote(self, options_str: str, start_line: int) -> QuoteBlock:
        """Parse @quote(author="...", source="...") Text... @end"""
        self._advance()
        options = self._parse_inline_options(options_str)
        author = options.get("author", "")
        source = options.get("source", "")

        text_lines = []
        while not self._is_at_end():
            line = self._peek().value
            if RE_END.match(line.strip()):
                self._advance()
                break
            text_lines.append(line)
            self._advance()

        text = "\n".join(text_lines).strip()
        return QuoteBlock(author=author, source=source, text=text, line=start_line)

    def _parse_timeline(self, start_line: int) -> TimelineBlock:
        """Parse @timeline date: text @end"""
        self._advance()
        events = []
        while not self._is_at_end():
            line = self._peek().value.strip()
            if RE_END.match(line):
                self._advance()
                break

            m = RE_TIMELINE_EVENT.match(line)
            if m:
                events.append((m.group(1), m.group(2)))
                self._advance()
                continue

            self._advance()

        return TimelineBlock(events=events, line=start_line)

    # --------------------------------------------------------
    # @if parser
    # --------------------------------------------------------

    def _parse_if(self, first_condition: str, start_line: int) -> IfBlock:
        """Parse @if ... @elif ... @else ... @endif"""
        block = IfBlock(branches=[], line=start_line)
        self._advance()

        first_children = self._parse_blocks(stop_at={"@elif", "@else", "@endif"})
        block.branches.append((first_condition, first_children))

        while not self._is_at_end():
            stripped = self._peek().value.strip()

            m = RE_ELIF.match(stripped)
            if m:
                self._advance()
                children = self._parse_blocks(stop_at={"@elif", "@else", "@endif"})
                block.branches.append((m.group(1), children))
                continue

            if RE_ELSE.match(stripped):
                self._advance()
                children = self._parse_blocks(stop_at={"@endif"})
                block.branches.append((None, children))
                if not self._is_at_end() and RE_ENDIF.match(self._peek().value.strip()):
                    self._advance()
                break

            if RE_ENDIF.match(stripped):
                self._advance()
                break

            break

        return block

    # --------------------------------------------------------
    # @each parser
    # --------------------------------------------------------

    def _parse_each(
        self,
        index_name: str,
        item_name: str,
        iterable_expr: str,
        start_line: int,
    ) -> EachBlock:
        """Parse @each item in items ... @end"""
        self._advance()
        children = self._parse_blocks(stop_at={"@end"})
        if not self._is_at_end() and RE_END.match(self._peek().value.strip()):
            self._advance()

        return EachBlock(
            index_name=index_name or "",
            item_name=item_name,
            iterable_expr=iterable_expr,
            children=children,
            line=start_line,
        )

    # --------------------------------------------------------
    # Front matter
    # --------------------------------------------------------

    def _parse_front_matter(self, doc: Document) -> None:
        if self._is_at_end():
            doc._content_start = 0
            return

        first = self._peek().value
        if not RE_FRONT_MATTER_START.match(first):
            doc._content_start = 0
            return

        saved_pos = self.pos
        self._advance()

        meta = {}
        found_closing = False

        while not self._is_at_end():
            line = self._peek().value

            if RE_FRONT_MATTER_START.match(line):
                self._advance()
                found_closing = True
                break

            if line.strip() == "":
                self._advance()
                continue

            m = RE_FRONT_MATTER_KEY.match(line)
            if m:
                key = m.group(1)
                value = m.group(2).strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                meta[key] = value
                self._advance()
            else:
                self.pos = saved_pos
                doc._content_start = 0
                return

        if not found_closing:
            self.pos = saved_pos
            doc._content_start = 0
            return

        doc.meta = meta
        doc._content_start = self.pos

    # --------------------------------------------------------
    # Footnotes
    # --------------------------------------------------------

    def _collect_footnotes(self, doc: Document) -> None:
        for token in self.tokens:
            m = RE_FOOTNOTE_DEF.match(token.value.strip())
            if m:
                doc.footnotes[m.group(1)] = m.group(2)

    # --------------------------------------------------------
    # Value parsing
    # --------------------------------------------------------

    def _parse_value(self, raw: str) -> Any:
        """Parse raw value into Python type."""
        raw = raw.strip()

        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            if not inner:
                return []
            items = self._split_top_level(inner, ",")
            return [self._parse_value(item) for item in items]

        if (raw.startswith('"') and raw.endswith('"')) or \
           (raw.startswith("'") and raw.endswith("'")):
            return raw[1:-1]

        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False

        if raw.lower() in ("null", "none"):
            return None

        try:
            return int(raw)
        except ValueError:
            pass

        try:
            return float(raw)
        except ValueError:
            pass

        return raw

    def _split_top_level(self, s: str, sep: str) -> List[str]:
        """Split by sep, ignoring separators inside quotes/brackets."""
        result = []
        current = []
        depth = 0
        in_quote = None

        for ch in s:
            if in_quote:
                if ch == in_quote:
                    in_quote = None
                current.append(ch)
            elif ch in ('"', "'"):
                in_quote = ch
                current.append(ch)
            elif ch in "[{(":
                depth += 1
                current.append(ch)
            elif ch in "]})":
                depth -= 1
                current.append(ch)
            elif ch == sep and depth == 0:
                result.append("".join(current).strip())
                current = []
            else:
                current.append(ch)

        if current:
            result.append("".join(current).strip())

        return result

    # --------------------------------------------------------
    # Heading slugs
    # --------------------------------------------------------

    def _assign_heading_slugs(self, doc: Document) -> None:
        seen = {}

        def visit(children):
            for child in children:
                if isinstance(child, Heading):
                    slug = self._slugify(child.text)
                    if slug in seen:
                        seen[slug] += 1
                        slug = f"{slug}-{seen[slug]}"
                    else:
                        seen[slug] = 0
                    child.slug = slug
                elif isinstance(child, IfBlock):
                    for _, branch_children in child.branches:
                        visit(branch_children)
                elif isinstance(child, EachBlock):
                    visit(child.children)

        visit(doc.children)

    @staticmethod
    def _slugify(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\u0600-\u06FF\u0750-\u077F\s-]", "", text)
        text = re.sub(r"[\s_]+", "-", text)
        text = re.sub(r"-+", "-", text)
        return text.strip("-") or "section"

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    def _is_table_start(self) -> bool:
        if self._is_at_end():
            return False
        line1 = self._peek().value
        if not RE_TABLE_LINE.match(line1):
            return False
        if self.pos + 1 >= len(self.tokens):
            return False
        line2 = self.tokens[self.pos + 1].value
        if not RE_TABLE_SEP.match(line2):
            return False
        if "-" not in line2:
            return False
        return True

    def _parse_table(self) -> TableBlock:
        start_line = self._peek().line
        header_line = self._peek().value
        headers = self._split_table_row(header_line)
        self._advance()

        sep_line = self._peek().value
        alignments = self._parse_alignments(sep_line)
        self._advance()

        while len(alignments) < len(headers):
            alignments.append("none")
        alignments = alignments[:len(headers)]

        rows = []
        while not self._is_at_end():
            line = self._peek().value
            if not RE_TABLE_LINE.match(line):
                break
            if RE_TABLE_SEP.match(line):
                self._advance()
                continue
            cells = self._split_table_row(line)
            while len(cells) < len(headers):
                cells.append("")
            cells = cells[:len(headers)]
            rows.append(cells)
            self._advance()

        return TableBlock(
            headers=headers,
            rows=rows,
            alignments=alignments,
            line=start_line,
        )

    def _split_table_row(self, line: str) -> List[str]:
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]

    def _parse_alignments(self, line: str) -> List[str]:
        cells = self._split_table_row(line)
        alignments = []
        for cell in cells:
            cell = cell.strip()
            left = cell.startswith(":")
            right = cell.endswith(":")
            if left and right:
                alignments.append("center")
            elif right:
                alignments.append("right")
            elif left:
                alignments.append("left")
            else:
                alignments.append("none")
        return alignments

    # --------------------------------------------------------
    # Gallery
    # --------------------------------------------------------

    def _parse_gallery(self, options_str: str, start_line: int) -> GalleryBlock:
        self._advance()
        options = self._parse_inline_options(options_str or "")

        try:
            columns = int(options.get("columns", 3))
        except (ValueError, TypeError):
            columns = 3

        columns = max(1, min(columns, 6))
        caption = options.get("caption", "")

        images = []
        while not self._is_at_end():
            line = self._peek().value.strip()
            if RE_END.match(line):
                self._advance()
                break
            if line == "":
                self._advance()
                continue
            m = RE_IMAGE.match(line)
            if m:
                images.append(self._parse_image(m, self._peek().line))
                self._advance()
                continue
            self._advance()

        return GalleryBlock(
            columns=columns,
            images=images,
            caption=caption,
            line=start_line,
        )

    def _parse_inline_options(self, options_str: str) -> dict:
        """Parse 'key="value" key2=value2' or 'key=value'."""
        if not options_str:
            return {}
        options = {}
        # Match: key="value" OR key='value' OR key=value OR key
        pattern = re.compile(r'(\w+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s,]+)))?')
        for match in pattern.finditer(options_str):
            key = match.group(1)
            value = match.group(2) or match.group(3) or match.group(4)
            options[key] = value if value is not None else True
        return options

    # --------------------------------------------------------
    # Image
    # --------------------------------------------------------

    def _parse_image(self, match: re.Match, line_num: int) -> ImageBlock:
        alt = match.group(1)
        url = match.group(2)
        title = match.group(3) or ""
        options_str = match.group(4) or ""
        options = self._parse_image_options(options_str)

        zoomable = options.get("zoomable", True)
        if isinstance(zoomable, str):
            zoomable = zoomable.lower() != "false"

        return ImageBlock(
            alt=alt,
            url=url,
            title=title,
            width=options.get("width", ""),
            height=options.get("height", ""),
            align=options.get("align", ""),
            link=options.get("link", ""),
            caption=options.get("caption", ""),
            description=options.get("desc", ""),
            zoomable=zoomable,
            line=line_num,
        )

    def _parse_image_options(self, options_str: str) -> dict:
        if not options_str:
            return {}
        options = {}
        pattern = re.compile(r'(\w+)(?:=(?:"([^"]*)"|(\S+)))?')
        for match in pattern.finditer(options_str):
            key = match.group(1)
            value = match.group(2) or match.group(3)
            options[key] = value if value else True
        return options

    # --------------------------------------------------------
    # Code block
    # --------------------------------------------------------

    def _parse_code_block(self, language: str, options_str: str, start_line: int) -> CodeBlock:
        self._advance()
        code_lines = []
        while not self._is_at_end():
            line = self._peek().value
            if RE_CODE_FENCE.match(line):
                self._advance()
                break
            code_lines.append(line)
            self._advance()

        options = self._parse_code_options(options_str or "")
        return CodeBlock(
            language=language,
            code="\n".join(code_lines),
            title=options.get("title", ""),
            copy=options.get("copy", True),
            download=options.get("download", True),
            run=options.get("run", False),
            share=options.get("share", False),
            linenos=options.get("linenos", False),
            highlight=options.get("hl", []),
            wrap=options.get("wrap", False),
            line=start_line,
        )

    def _parse_code_options(self, options_str: str) -> dict:
        if not options_str:
            return {}
        options = {}
        pattern = re.compile(r'(\w+)(?:=(?:"([^"]*)"|\[([^\]]*)\]|(\w+)))?')
        for match in pattern.finditer(options_str):
            key = match.group(1)
            str_val = match.group(2)
            list_val = match.group(3)
            word_val = match.group(4)
            if str_val is not None:
                options[key] = str_val
            elif list_val is not None:
                options[key] = [int(x.strip()) for x in list_val.split(",") if x.strip()]
            elif word_val is not None:
                if word_val == "true":
                    options[key] = True
                elif word_val == "false":
                    options[key] = False
                else:
                    options[key] = word_val
            else:
                options[key] = True
        return options

    # --------------------------------------------------------
    # Blockquote / List
    # --------------------------------------------------------

    def _parse_blockquote(self) -> BlockQuote:
        start_line = self._peek().line
        lines = []
        while not self._is_at_end():
            line = self._peek().value
            m = RE_BLOCKQUOTE.match(line)
            if not m:
                break
            lines.append(m.group(1))
            self._advance()
        return BlockQuote(text="\n".join(lines), line=start_line)

    def _parse_task_list(self) -> ListBlock:
        start_line = self._peek().line
        items, checked = [], []
        while not self._is_at_end():
            line = self._peek().value
            m = RE_TASK_ITEM.match(line)
            if not m:
                break
            items.append(m.group(2))
            checked.append(m.group(1).lower() == "x")
            self._advance()
        return ListBlock(ordered=False, items=items, checked=checked, line=start_line)

    def _parse_ul(self) -> ListBlock:
        start_line = self._peek().line
        items = []
        while not self._is_at_end():
            line = self._peek().value
            m = RE_UL_ITEM.match(line)
            if not m:
                break
            items.append(m.group(1))
            self._advance()
        return ListBlock(ordered=False, items=items, line=start_line)

    def _parse_ol(self) -> ListBlock:
        start_line = self._peek().line
        items = []
        while not self._is_at_end():
            line = self._peek().value
            m = RE_OL_ITEM.match(line)
            if not m:
                break
            items.append(m.group(1))
            self._advance()
        return ListBlock(ordered=True, items=items, line=start_line)

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if not self._is_at_end():
            self.pos += 1
        return token

    def _is_at_end(self) -> bool:
        return self.tokens[self.pos].type == "EOF"


def parse_text(text: str) -> Document:
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()