Markup+ Installation Guide
==========================

Version: 0.6.0
Last Updated: January 2026

Complete installation instructions for Markup+ on Windows, macOS,
and Linux.

---

Table of Contents
-----------------

1. Requirements
2. Method 1: Windows Installer (Recommended)
3. Method 2: Portable Version
4. Method 3: pip install
5. Method 4: Install from Source
6. Virtual Environment Setup
7. Verify Installation
8. Upgrade
9. Uninstall
10. Troubleshooting
11. Offline Installation
12. Docker (Advanced)

---

1. Requirements
---------------

### Minimum Requirements

    Component           Requirement
    Operating System    Windows 10+, macOS 11+, Linux (any modern distro)
    Architecture        64-bit (x64)
    RAM                 2 GB
    Disk Space          20 MB (installer) or 50 MB (pip with dependencies)
    Browser             Chrome, Firefox, Safari, Edge, or any modern browser

### For Windows Installer

- Windows 10 or later (64-bit)
- No Python installation required
- Administrator rights (optional, for system-wide install)

### For pip Installation

- Python 3.9 or higher
- pip (comes with Python)
- pip install location in PATH

### For Source Installation

- Python 3.9 or higher
- Git
- A code editor
- Development tools (pytest, black, ruff)

---

2. Method 1: Windows Installer (Recommended)
--------------------------------------------

Best for: Windows users who want a simple installation without
Python.

### Step 1: Download the Installer

Open your browser and go to:

    https://github.com/ataee-dev/markup-plus/releases/latest

Look for the file:

    markup-plus-setup-0.6.0.exe

Click to download. File size is approximately 7.5 MB.

### Step 2: Run the Installer

Double-click the downloaded file.

**Windows SmartScreen warning:**

The installer is not code-signed. Windows may show:

    Windows protected your PC

This is normal for open-source software distributed outside the
Microsoft Store.

To proceed:

1. Click "More info"
2. Click "Run anyway"

### Step 3: Welcome Page

You will see a welcome page explaining Markup+. Click **Next**.

### Step 4: License Agreement

Read the license (Markup+ Non-Commercial License). Click **I accept
the agreement** to continue.

### Step 5: Choose Installation Type

Three options:

    Type          Description
    Full          Everything included (recommended)
    Compact       Core files only
    Custom        Choose components manually

For most users, **Full** is best. Click **Next**.

### Step 6: Choose Install Location

Default location:

    C:\Program Files\Markup+\

You can change it by clicking **Browse**. Click **Next**.

### Step 7: Select Components

    Component                          Description
    Markup+ Core                       Required
    Associate .mup files               Recommended
    Documentation and Examples         Optional

Keep the defaults. Click **Next**.

### Step 8: Select Additional Tasks

Two tasks:

    Task                                          Recommended
    Create a desktop shortcut                     Optional
    Add Markup+ to system PATH                    Yes
    Associate .mup files with Markup+             Yes

**Important:** Keep "Add Markup+ to system PATH" checked. This lets
you run `mup` from any folder.

Click **Next**.

### Step 9: Ready to Install

Review your choices. Click **Install**.

### Step 10: Installation Progress

Wait for the installation to complete. It takes about 5-10 seconds.

### Step 11: Finish

After installation, you can:

- Launch Markup+ (opens WELCOME.txt)
- Open the installation folder
- View the documentation

Click **Finish**.

### Step 12: Verify

Open a **new** Command Prompt:

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Type:

    mup --version

Expected output:

    Markup+ v0.6.0

If you see this, installation succeeded.

---

3. Method 2: Portable Version
-----------------------------

Best for: Users who do not want to install anything, or who use
Markup+ on a USB drive.

### Step 1: Download

Go to:

    https://github.com/ataee-dev/markup-plus/releases/latest

Download:

    markup-plus.zip

### Step 2: Extract

Right-click the ZIP file and choose **Extract All**.

Choose a folder. For example:

    C:\Tools\markup-plus\

### Step 3: Run

Open the extracted folder. You should see:

    mup.exe
    _internal\          (folder with dependencies)
    icon-app.ico
    icon-file.ico
    LICENSE.txt
    WELCOME.txt

Double-click `mup.exe` to run. Or from Command Prompt:

    C:\Tools\markup-plus\mup.exe --version

### Step 4: Add to PATH (Optional)

If you want to run `mup` from any folder, add the folder to PATH
manually:

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab
3. Click **Environment Variables**
4. Under **User variables**, select **Path** and click **Edit**
5. Click **New** and add the full path (e.g., `C:\Tools\markup-plus\`)
6. Click **OK** three times
7. Open a new Command Prompt
8. Verify:

    mup --version

### Limitations

- No file association for `.mup`
- No desktop shortcut
- No Start Menu entry
- Must be updated manually

---

4. Method 3: pip install
------------------------

Best for: Python developers, cross-platform users, CI/CD pipelines.

### Step 1: Install Python

If you do not have Python:

1. Go to https://www.python.org/downloads/
2. Download Python 3.9 or higher
3. Run the installer

**Important:** Check **Add Python to PATH** during installation.

Verify:

    python --version

Expected output:

    Python 3.11.x  (or higher)

### Step 2: Install Markup+

    pip install markup-plus

This downloads and installs Markup+ and its dependencies.

### Step 3: Verify

    mup --version

Expected output:

    Markup+ v0.6.0

### Step 4: Optional Dependencies

For development or testing:

    pip install pytest pytest-cov black ruff

### Where Is It Installed?

Markup+ is installed in your Python site-packages:

    C:\Users\<YourName>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages\markup_plus\

The `mup` command is in:

    C:\Users\<YourName>\AppData\Local\Programs\Python\Python3xx\Scripts\mup.exe

### Advantages

- Cross-platform (Windows, macOS, Linux)
- Easy to upgrade
- Works with virtual environments
- Integrates with Python projects

### Limitations

- Requires Python installation
- Not a standalone executable

---

5. Method 4: Install from Source
--------------------------------

Best for: Contributors, users who want the latest development
version.

### Step 1: Install Prerequisites

- Python 3.9 or higher
- Git

### Step 2: Clone the Repository

    git clone https://github.com/ataee-dev/markup-plus.git
    cd markup-plus

### Step 3: Create Virtual Environment

    python -m venv venv

Activate:

    venv\Scripts\activate          (Windows)
    source venv/bin/activate       (macOS/Linux)

### Step 4: Install in Editable Mode

    pip install -e .

This installs Markup+ in development mode. Changes to the source code
take effect immediately.

### Step 5: Install Development Dependencies

    pip install pytest pytest-cov black ruff

### Step 6: Verify

    pytest tests/ -v

All tests should pass.

    mup --version

Expected output:

    Markup+ v0.6.0

### Step 7: Run Examples

    cd examples
    mup hello.mup
    start hello.html

---

6. Virtual Environment Setup
----------------------------

A virtual environment isolates Markup+ from other Python packages.
Recommended for development.

### Windows

    python -m venv venv
    venv\Scripts\activate

You will see `(venv)` in the prompt.

### macOS / Linux

    python3 -m venv venv
    source venv/bin/activate

### Install Markup+

    pip install markup-plus

### Deactivate

    deactivate

### Why Use a Virtual Environment?

- Prevents version conflicts
- Keeps your system Python clean
- Easy to delete and recreate
- Recommended for all Python projects

---

7. Verify Installation
----------------------

### Check Version

    mup --version

Expected output:

    Markup+ v0.6.0

### Check Location

    where mup                (Windows)
    which mup                (macOS/Linux)

Expected output:

    C:\Program Files\Markup+\mup.exe                     (installer)
    C:\Users\...\Python3xx\Scripts\mup.exe               (pip)

### Test Conversion

Create a test file `test.mup`:

    # Hello World

    This is a **test**.

Convert it:

    mup test.mup

You should see:

    Converted: test.mup -> test.html

Open `test.html` in a browser. You should see a formatted page.

### Check Help

    mup --help

Shows all available commands and options.

---

8. Upgrade
----------

### Windows Installer

Download the new installer and run it. It will upgrade in place.

    https://github.com/ataee-dev/markup-plus/releases/latest

Your settings (PATH, associations) are preserved.

### pip

    pip install --upgrade markup-plus

### Verify

    mup --version

Should show the new version.

### Downgrade

If you need an older version:

    pip install markup-plus==0.5.0

---

9. Uninstall
------------

### Windows Installer

**Method 1: Control Panel**

1. Press `Win + R`
2. Type `appwiz.cpl` and press Enter
3. Find **Markup+** in the list
4. Click **Uninstall**
5. Follow the prompts

**Method 2: Settings**

1. Open **Settings**
2. Go to **Apps** then **Apps and features**
3. Find **Markup+**
4. Click **Uninstall**

The uninstaller will:

- Remove files from `C:\Program Files\Markup+\`
- Remove PATH entry
- Remove `.mup` file association
- Remove shortcuts

### pip

    pip uninstall markup-plus

### Clean Up PATH (if needed)

If the uninstaller did not remove PATH:

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab
3. Click **Environment Variables**
4. Under **User variables**, select **Path** and click **Edit**
5. Find any entry with `Markup+`
6. Select it and click **Delete**
7. Click **OK** three times
8. Close and reopen Command Prompt

### Clean Up Registry (advanced)

If `.mup` is still associated with Markup+:

    reg delete "HKCU\Software\Classes\.mup" /f
    reg delete "HKCU\Software\Classes\MarkupPlus.mup" /f

### Restart

Restart your computer to ensure all changes take effect.

---

10. Troubleshooting
-------------------

### mup: command not found

**Cause:** PATH not updated in current session.

**Fix:** Close Command Prompt and open a new one.

If still failing:

    python -m pip install --upgrade markup-plus

Or use full path:

    python -m markup_plus file.mup

### Installer shows SmartScreen warning

**Cause:** Installer is not code-signed.

**Fix:** Click "More info" then "Run anyway". Normal for open-source
software.

### Access denied during installation

**Cause:** Trying to install to a protected folder.

**Fix:** Choose a user folder (like `C:\Users\<You>\Markup+`) or run
the installer as Administrator.

### pip install fails with permission error

**Cause:** Trying to install to system Python.

**Fix:** Use a virtual environment or add `--user`:

    pip install --user markup-plus

### pip install is slow

**Cause:** Network speed or large dependencies.

**Fix:** Use a mirror:

    pip install markup-plus -i https://pypi.org/simple/

### Markup+ installed but mup.exe missing

**Cause:** Antivirus software may have quarantined `mup.exe`.

**Fix:** Check your antivirus quarantine. Add an exception for
Markup+.

### Import error: cannot import name

**Cause:** Circular import or version mismatch.

**Fix:**

    pip uninstall markup-plus
    pip install markup-plus

### Python version not supported

**Cause:** Python is older than 3.9.

**Fix:** Upgrade Python from https://www.python.org/downloads/

Verify:

    python --version

### .mup files open with wrong program

**Cause:** File association not set or overridden.

**Fix:**

1. Right-click any `.mup` file
2. Choose **Open with** then **Choose another app**
3. Select **mup.exe** (in `C:\Program Files\Markup+\`)
4. Check **Always use this app**

### Output HTML is empty

**Cause:** Input file was empty or only contained comments.

**Fix:** Check the input file. Run `mup check file.mup`.

### File is not valid UTF-8

**Cause:** Input file uses a different encoding.

**Fix:** Save the file as UTF-8 in your editor.

### Variables not replaced

**Cause:** Missing `{ }` or typo.

**Fix:** Verify variable names are case-sensitive and wrapped in
braces.

### Chart not rendering

**Cause:** No internet connection (Chart.js loads from CDN).

**Fix:** Connect to the internet, or download Chart.js locally.

### Installation freezes

**Cause:** Antivirus scanning, or slow disk.

**Fix:** Wait. If it takes more than 5 minutes, cancel and try again
with antivirus disabled.

---

11. Offline Installation
------------------------

If you do not have internet access.

### Windows Installer

The installer works offline. However, generated HTML needs internet
for CDN resources.

To make output fully offline, edit the HTML template to use local
copies of:

- Prism.js
- Chart.js
- KaTeX

### pip

Download the wheel on a machine with internet:

    pip download markup-plus -d ./packages

Copy `./packages` to the offline machine. Install:

    pip install --no-index --find-links=./packages markup-plus

### Dependencies

Markup+ has no mandatory external dependencies beyond Python.
Optional testing dependencies can also be downloaded:

    pip download pytest pytest-cov black ruff -d ./packages

---

12. Docker (Advanced)
---------------------

Best for: CI/CD pipelines, isolated environments.

### Create a Dockerfile

    FROM python:3.11-slim

    RUN pip install markup-plus

    WORKDIR /docs

    CMD ["mup", "--help"]

### Build

    docker build -t markup-plus .

### Run

    docker run --rm -v $(pwd):/docs markup-plus mup file.mup

### Advantages

- Fully isolated
- Consistent across environments
- No system modification

### Limitations

- Requires Docker installed
- Slightly slower than native
- Network configuration needed for CDN resources

---

Further Reading
---------------

- README.md -- Project overview
- GUIDE.md -- Full user guide
- TUTORIAL.md -- Step-by-step tutorial
- CUSTOM-CSS.md -- Customization guide
- FAQ.md -- Frequently asked questions
- DEVELOPER.md -- Developer guide
- CHANGELOG.md -- Version history

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