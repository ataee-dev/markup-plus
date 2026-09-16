
---

## 📋 Summary of Sections

| Section | Topic | Simple Explanation |
|---------|-------|-------------------|
| **1** | Code of Conduct | Behavioral rules — how we treat each other to keep the community friendly |
| **2** | Ways to Contribute | How to help — you don't have to write code! |
| **3** | Before You Start | Before starting — check if someone already did it |
| **4** | Setting Up Environment | Install and set up the dev environment on your machine |
| **5** | Development Workflow | Daily Git workflow (branching, committing, pushing) |
| **6** | Coding Standards | How to write clean code |
| **7** | Writing Tests | How to write tests to make sure code works |
| **8** | Writing Documentation | How to write good docs |
| **9** | Commit Message Guidelines | How to format commit messages |
| **10** | Pull Request Process | How to submit a PR |
| **11** | Reporting Bugs | How to report bugs properly |
| **12** | Suggesting Features | How to propose new features |
| **13** | Translation Guide | How to translate the project |
| **14** | Recognition | How contributors get credited |

---

## 🎯 Who Is This File For?

This file is written for **three groups**:

### 1️⃣ First-time Contributors
If you've never contributed to a project before, this file walks you through it step by step.

### 2️⃣ Developers
If you want to write code, the standards and workflow are described here.

### 3️⃣ Translators and Designers
Even if you can't code, you can translate docs or improve the design.

---

## 🛠️ What This File Asks You to Do (Short Version)

### If you want to write code:

1. **Fork** — make a copy of the project in your own GitHub account
2. **Clone** — bring the copy to your computer
3. **Create a virtual environment** — `python -m venv venv`
4. **Install** — `pip install -e .`
5. **Create a branch** — `git checkout -b feature/my-feature`
6. **Write code**
7. **Write tests** — `pytest tests/ -v`
8. **Format** — `black src/ tests/`
9. **Commit** — `git commit -m "feat: add my feature"`
10. **Push and open a PR**

### Important rules:

- **Comments must be in English** (not Persian)
- **Follow PEP 8** (max 100 characters per line)
- **Write tests for every new feature**
- **Update the documentation**
- **For big changes, open an issue first and get approval**

---

## 📝 Commit Message Format (Very Important)

Commits should look like this:

```
<type>(<scope>): <subject>
```

**Examples:**
```
feat: add @run directive for code blocks
fix: correct RTL detection for mixed text
docs: add examples to GUIDE.md
test: add parser tests for nested lists
```

**Types:**
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Tests |
| `refactor` | Code refactoring |
| `perf` | Performance improvement |
| `style` | Formatting |
| `chore` | Maintenance |

---

## 🐛 If You Find a Bug, What Should You Do?

**Bug report template:**

```markdown
**Describe the bug**
Clear description of the problem.

**To Reproduce**
1. Create file `test.mup` with content...
2. Run `mup test.mup`
3. Open `test.html`
4. See the error

**Expected behavior**
Should display `Hello Ali!`

**Actual behavior**
Displays `Hello {name}!` — variable not substituted.

**Environment**
- OS: Windows 10
- Python: 3.11.5
- Markup+: 0.6.0

**Additional context**
Screenshot attached.
```

**Key points:**
- ✅ Send the smallest possible reproduction file
- ✅ Write exact commands you ran
- ✅ Copy-paste the error text (not a screenshot)
- ❌ Don't write "it doesn't work" — be specific
- ❌ Don't send a huge file

---

## ✅ Checklist Before Submitting a PR

Before opening a PR, make sure:

- [ ] My code follows the style guide
- [ ] I ran `black src/ tests/`
- [ ] I ran `ruff check src/ tests/`
- [ ] I ran `pytest tests/ -v` and all tests pass
- [ ] I added tests for new functionality
- [ ] I updated the documentation
- [ ] I updated `CHANGELOG.md`
- [ ] My commits follow the commit guidelines
- [ ] My branch is up to date with `upstream/master`

---

## 🎁 What You Get (Recognition)

If you contribute:
- 🏆 Your name appears in release notes
- ⭐ You get featured in the README
- 🎁 You may receive swag (t-shirt, stickers, etc.)
- 📜 You get thanked in `CHANGELOG.md` by name

---

## 💡 One-Line Summary

> This file is the **contribution guide for the Markup+ project**. It tells you how to set up your dev environment, how to write code, how to write tests, how to commit, how to open a PR, and how to report bugs.

---

## ❓ FAQ

**Q: Do I have to write code to contribute?**
A: No! You can improve docs, translate, report bugs, or suggest features.

**Q: What if I'm a beginner?**
A: Look for issues labeled `good first issue`, `documentation`, or `help wanted`.

**Q: What if I want to make a big change?**
A: Open an issue first, explain your plan, wait for approval, then start coding.

**Q: Why do comments have to be in English?**
A: Because the project is international — everyone should be able to read them.

**Q: What if my PR gets no response for a while?**
A: After 2 weeks, leave a comment to ping the maintainers.

**Q: How do I keep my fork in sync?**
A: Run:
```bash
git fetch upstream
git rebase upstream/master
git push --force-with-lease origin your-branch
```

---

---

## 📚 Full Guide

For the complete contribution guide (all workflows, all standards),
see **[CONTRIBUTING-FOR-AI.md](CONTRIBUTING-FOR-AI.md)**.