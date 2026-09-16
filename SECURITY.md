# 🔒 Security Policy

> **Version:** 0.6.0
> **Last Updated:** January 2025

We take the security of **Markup+** seriously. Thank you for helping us keep
this project safe.

---

## 📑 Table of Contents

1. [Supported Versions](#1-supported-versions)
2. [Reporting a Vulnerability](#2-reporting-a-vulnerability)
3. [What We Expect From You](#3-what-we-expect-from-you)
4. [What You Can Expect From Us](#4-what-you-can-expect-from-us)
5. [Security Considerations](#5-security-considerations)
6. [Best Practices](#6-best-practices)
7. [Acknowledgments](#7-acknowledgments)

---

## 1. Supported Versions

We provide security updates for the following versions:

| Version | Supported | Notes |
|---------|:---------:|-------|
| `0.6.x` | ✅ | Current stable release |
| `0.5.x` | ⚠️ | Security fixes only |
| `0.4.x` and older | ❌ | No longer supported |

**Recommendation:** Always use the latest stable version.

```bash
pip install --upgrade markup-plus
```

---

## 2. Reporting a Vulnerability

### 🔐 Private Report (Recommended)

If you discover a security vulnerability, **please do not report it
publicly**. Instead, choose one of the following methods:

**Method 1 — GitHub Security Advisories:**

1. Go to the repository: https://github.com/USERNAME/markup-plus
2. Click the **Security** tab
3. Click **Report a vulnerability**
4. Fill out the form

**Method 2 — Email:**

Send an email to:

```
security@markupplus.dev
```

**Method 3 — Private Message:**

Send a private message to one of the project maintainers on GitHub.

### 📝 What Information to Send

To help us respond quickly, please include the following:

```markdown
**Vulnerability Type:**
e.g., XSS, Code Injection, Path Traversal

**Markup+ Version:**
Output of `mup --version`

**Operating System:**
e.g., Windows 10, Ubuntu 22.04, macOS 14

**Python Version:**
Output of `python --version`

**Description:**
Clear and complete description of the vulnerability

**Steps to Reproduce:**
1. Create file `test.mup` with content: ...
2. Run command `mup test.mup`
3. Observe that ...

**Impact:**
What attack is possible? What is at risk?

**Suggested Fix (Optional):**
If you have a fix in mind, please describe it

**Additional Info:**
Links, screenshots, outputs
```

### ⚠️ What NOT to Report

- ❌ Third-party dependency vulnerabilities (report to the original project)
- ❌ Attacks requiring physical access
- ❌ Theoretical issues not practically exploitable
- ❌ Public information already in the documentation

---

## 3. What We Expect From You

When you report a vulnerability, please:

- ✅ **Stay confidential** — don't disclose publicly until we've fixed it
- ✅ **Be honest** — provide accurate and complete information
- ✅ **Be patient** — fixing takes time
- ✅ **Cooperate** — respond to our questions
- ✅ **Coordinate** — agree with us before public disclosure

**Please do NOT:**
- ❌ Exploit the vulnerability
- ❌ Expose user data
- ❌ Damage systems
- ❌ Attempt extortion

---

## 4. What You Can Expect From Us

### ⏱️ Timeline

| Stage | Time |
|-------|------|
| **Acknowledgment** | Within 48 hours |
| **Initial review** | Within 7 days |
| **Full assessment** | Within 14 days |
| **Fix** | Depends on severity |
| **Release of fix** | Within 30 days |

### 🎖️ Credit

- 📝 Your name in `CHANGELOG.md` (if you wish)
- 🏆 Mention in GitHub release
- ⭐ In README (for significant vulnerabilities)
- 🎁 Swag (if available)

### 📢 Public Disclosure

- We **always** coordinate with you before public disclosure
- If you wish to stay anonymous, we respect that
- The public disclosure date is agreed upon by both parties

---

## 5. Security Considerations

### 5.1 Threat Model

**What Markup+ is designed for:**

- ✅ Generating HTML from valid `.mup` files
- ✅ Running in a local or trusted server environment
- ✅ Converting trusted files to HTML

**What Markup+ is NOT designed for:**

- ❌ Executing invalid or malicious `.mup` files
- ❌ Running arbitrary code
- ❌ Serving untrusted users
- ❌ Real-time processing of user input

### 5.2 Important Security Points

#### 🔸 XSS (Cross-Site Scripting)

Markup+ **generates HTML output**. If `.mup` files come from untrusted
sources, JavaScript code may be embedded in the output HTML.

**Recommendation:** Only process `.mup` files from trusted sources.

#### 🔸 Code Injection

Markup+ **does not execute code** — it only converts text to HTML.
However, the `@run` directive (in future versions) will execute HTML/JS code.

**Recommendation:** Use `@run` only with trusted content.

#### 🔸 Path Traversal

The `@import` directive loads external files. If the path comes from user
input, it could access sensitive files.

**Dangerous example:**

```mup
@import "../../../etc/passwd"
```

**Recommendation:** Use `@import` only with fixed and trusted paths.

#### 🔸 Denial of Service

Large files or deeply nested structures can consume CPU and RAM.

**Recommendation:**
- Split large `.mup` files into smaller parts
- Limit the nesting depth of loops

### 5.3 Dependencies

Markup+ is written in **pure Python** and has no mandatory external
dependencies.

Optional dependencies (for testing):

| Package | Purpose | Security |
|---------|---------|----------|
| `pytest` | Testing | ✅ Trusted |
| `pytest-cov` | Test coverage | ✅ Trusted |
| `black` | Code formatter | ✅ Trusted |
| `ruff` | Linter | ✅ Trusted |

**Note:** The HTML output uses trusted CDNs:

- **Prism.js** (syntax highlighting) — `cdn.jsdelivr.net`
- **Chart.js** (charts) — `cdn.jsdelivr.net`
- **KaTeX** (math formulas) — `cdn.jsdelivr.net`

If CDN security matters to you, you can load the libraries locally.

---

## 6. Best Practices

### 👤 For Users

- ✅ **Trusted sources only:** Don't process `.mup` files from unknown sources
- ✅ **Isolated environment:** Use containers or sandboxes on servers
- ✅ **Stay updated:** Always install the latest version
- ✅ **Limit access:** Store `.mup` files with restricted permissions
- ✅ **Validate input:** Check user input before processing
- ✅ **Enable logging:** Log suspicious activity

### 👨‍💻 For Developers

- ✅ **Validate input:** Check all inputs
- ✅ **Escape output:** Escape generated HTML
- ✅ **File restrictions:** Limit access to external files
- ✅ **Dependency checks:** Keep dependencies up to date
- ✅ **Security tests:** Write security tests
- ✅ **Responsible disclosure:** Report vulnerabilities responsibly

### 🏢 For Organizations

- ✅ **Isolated environment:** Run Markup+ in a separate environment
- ✅ **Content policy:** Define a safe content policy
- ✅ **Training:** Train your team
- ✅ **Monitoring:** Monitor systems
- ✅ **Periodic review:** Regularly review security

---

## 7. Acknowledgments

We thank everyone who helps keep Markup+ secure.

### 🏆 Hall of Fame

Those who have responsibly reported security vulnerabilities:

<!-- This section is updated with each valid report -->

*No reports yet — you could be the first!*

---

## 📚 Further Reading

### Related Documents

- [README.md](README.md) — Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) — Contribution guidelines
- [GUIDE.md](GUIDE.md) — User guide
- [DEVELOPER.md](DEVELOPER.md) — Developer guide
- [ROADMAP.md](ROADMAP.md) — Roadmap

### Useful Links

- **GitHub Security:** https://github.com/USERNAME/markup-plus/security
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **CWE:** https://cwe.mitre.org/
- **CVE:** https://cve.mitre.org/

### Standards

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📞 Contact

For security matters:

- 🔒 **Security Email:** security@markupplus.dev
- 🐛 **GitHub Issues:** https://github.com/USERNAME/markup-plus/issues (non-sensitive only)
- 💬 **GitHub Discussions:** https://github.com/USERNAME/markup-plus/discussions

---

## 📜 License

This document is released under the MIT License.

Copyright © 2025 Ataee

---

**Version:** 0.6.0
**Last Updated:** January 2025

**Thank you for your cooperation! 💜**