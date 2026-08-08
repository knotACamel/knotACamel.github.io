from pathlib import Path
import html
import shutil
import sys

ROOT = Path(__file__).resolve().parent
SUB = ROOT.parent / "ProjectSubmission"
FILES = ROOT / "files"

YOUTUBE_ID = "B7c0iP9zfA4"
YOUTUBE_URL = "https://youtu.be/B7c0iP9zfA4"

AUTHOR = "Dustin Ledbetter"
SITE_TITLE = "CS 499 ePortfolio"

NAV = [
    ("index.html", "Home"),
    ("code-review.html", "Code Review"),
    ("enhancement-1.html", "Software Design"),
    ("enhancement-2.html", "Algorithms"),
    ("enhancement-3.html", "Databases"),
]

LANG = {".java": "java", ".cpp": "cpp", ".h": "cpp", ".py": "python",
        ".md": "markdown", ".example": "ini", ".ipynb": "json"}


CONTENT = {
    "enhancement-1": {
        "number": 1,
        "category": "Software Design and Engineering",
        "title": "Contact Service",
        "course": "CS 320 — Software Testing, Automation, and Quality Assurance",
        "tags": ["Java", "JUnit 5", "HashMap", "Input Validation", "Singleton"],
        "summary": (
            "A contact management service built from two production classes and two JUnit "
            "test classes. The enhancement rebuilt the validation strategy so business "
            "constraints cannot be bypassed, and replaced the backing array with a HashMap "
            "keyed by contact ID."
        ),
        "highlights": [
            ("Validation that cannot be sidestepped",
             "The original validated only in the constructor, so any setter could push an "
             "invalid value straight past the constraints. Validation now lives in dedicated "
             "methods that every mutator is required to route through, which also means a "
             "future setter inherits the rules instead of forgetting them."),
            ("Array to HashMap",
             "Lookup, update, and delete moved from O(n) linear scans to O(1) average access, "
             "and the hard ceiling of 9,999 records disappeared with the fixed-size array."),
            ("Test coverage that grew with the design",
             "The two test classes expanded from 87 lines to 462 as the new validation paths "
             "and collection behavior needed to be pinned down."),
        ],
        "outcomes": [
            ("Outcome 3 — Design and evaluate computing solutions, managing trade-offs",
             "The storage change was treated as a trade rather than a free upgrade. The HashMap "
             "costs more memory per record and gives up insertion order; it wins here only "
             "because this service is lookup heavy."),
            ("Outcome 4 — Well-founded and innovative techniques, skills, and tools",
             "The Java Collections Framework and JUnit 5 were used to redesign the validation "
             "layer around single-responsibility methods."),
        ],
        "files": [
            ("Contact.java", "Enhancement1/Original/Contact.java", "Enhancement1/Enhanced/Contact.java",
             "Validation extracted into reusable methods; all mutators route through them."),
            ("ContactServices.java", "Enhancement1/Original/ContactServices.java", "Enhancement1/Enhanced/ContactServices.java",
             "Backing array replaced with a HashMap keyed by contact ID."),
            ("ContactTest.java", "Enhancement1/Original/ContactTest.java", "Enhancement1/Enhanced/ContactTest.java",
             "Expanded to cover the new mutator validation paths."),
            ("ContactServicesTest.java", "Enhancement1/Original/ContactServicesTest.java", "Enhancement1/Enhanced/ContactServicesTest.java",
             "Expanded to cover collection behavior and edge cases."),
        ],
        "narrative": "Enhancement1/Enhancement1_Narrative.docx",
    },
    "enhancement-2": {
        "number": 2,
        "category": "Algorithms and Data Structures",
        "title": "Course Planner",
        "course": "CS 260 — Data Structures and Algorithms",
        "tags": ["C++", "AVL Tree", "Self-Balancing BST", "Invariant Validation"],
        "summary": (
            "A course catalog application that loads records from CSV, prints the catalog in "
            "alphabetical order, and looks up prerequisites. The enhancement converted the "
            "unbalanced binary search tree into a self-balancing AVL tree and added height "
            "invariant validation."
        ),
        "highlights": [
            ("Why AVL, and why not a hash table",
             "The application has two operations with different structural needs: ordered "
             "listing and keyed lookup. A hash table would win on lookup alone but cannot "
             "produce sorted output without a separate sort on every listing. An AVL tree "
             "serves both, guaranteeing O(log n) lookup while keeping in-order traversal free."),
            ("Rotations and height bookkeeping",
             "rotateLeft and rotateRight rebalance on insert, recalculating stored heights as "
             "pointers are rewired. This is where the original BST degraded: alphabetically "
             "sorted input produced a effectively linked list with O(n) lookup."),
            ("Correctness by invariant, not by eyeballing output",
             "validate() checks every stored height against its computed height and confirms "
             "the balance factor at each node stays within ±1. That catches a broken rotation "
             "immediately, rather than hoping a wrong answer happens to be visible in output."),
        ],
        "outcomes": [
            ("Outcome 3 — Design and evaluate computing solutions, managing trade-offs",
             "The AVL conversion was a deliberate structural decision weighed against the "
             "alternatives, accepting rotation cost on insert to buy a worst-case guarantee "
             "on lookup and to keep ordered traversal."),
            ("Outcome 4 — Well-founded and innovative techniques, skills, and tools",
             "Verification through invariant validation rather than output inspection."),
        ],
        "files": [
            ("ProjectTwo.cpp", "Enhancement2/Original/ProjectTwo.cpp", "Enhancement2/Enhanced/ProjectTwo.cpp",
             "Menu and program flow, rewired to the AVL tree and split away from the structure itself."),
            ("AVLTree.h", None, "Enhancement2/Enhanced/AVLTree.h",
             "New file. Interface for the self-balancing tree."),
            ("AVLTree.cpp", None, "Enhancement2/Enhanced/AVLTree.cpp",
             "New file. Insert, rotations, height maintenance, and validate()."),
        ],
        "narrative": "Enhancement2/Enhancement2_Narrative.docx",
    },
    "enhancement-3": {
        "number": 3,
        "category": "Databases",
        "title": "Animal Shelter Dashboard",
        "course": "CS 340 — Advanced Programming Concepts",
        "tags": ["Python", "MongoDB", "Aggregation Pipeline", "Compound Indexes", "Dash"],
        "summary": (
            "A client/server dashboard over a MongoDB animal shelter database, with a data "
            "access layer cleanly separated from the presentation layer. The enhancement "
            "pushed reporting work down into the database, added index management with "
            "measurement to prove it, and moved credentials out of the source."
        ),
        "highlights": [
            ("Let the database do the counting",
             "get_breed_outcome_report() uses an aggregation pipeline so MongoDB counts "
             "records server-side, instead of pulling the full result set into pandas and "
             "counting in application memory."),
            ("Indexes, with evidence",
             "explain_query() and the timing helpers demonstrate the COLLSCAN-to-IXSCAN "
             "transition rather than asserting the index helped. Compound field order matters: "
             "MongoDB can use a leading subset of an index but not a trailing one, and a range "
             "condition stops the index narrowing anything after it — which is why age had to go last."),
            ("Credentials out of the source",
             "Connection details moved to environment variables loaded from a .env file, which "
             "is excluded from version control. Only env.example is published here."),
            ("Failing loudly beats failing quietly",
             "Dropping the _id column unconditionally crashed on queries that matched nothing, "
             "and positional column access silently pointed at the wrong data whenever the "
             "schema gained or lost a field. Both now fail visibly instead of quietly misreporting."),
        ],
        "outcomes": [
            ("Outcome 3 — Design and evaluate computing solutions, managing trade-offs",
             "Index design was weighed explicitly: each index speeds reads but costs write "
             "throughput and storage, and compound field order determines which queries benefit."),
            ("Outcome 4 — Well-founded and innovative techniques, skills, and tools",
             "Aggregation pipelines, explain plans, and timing instrumentation used to measure "
             "rather than assume."),
            ("Outcome 5 — Develop a security mindset",
             "Hard-coded credentials removed from source and relocated to environment "
             "configuration kept out of version control."),
        ],
        "files": [
            ("CRUD_Python_Module.py", "Enhancement3/Original/CRUD_Python_Module.py", "Enhancement3/Enhanced/CRUD_Python_Module.py",
             "The data access layer. Grew from 85 to 306 lines with aggregation, index management, and timing."),
            ("env.example", None, "Enhancement3/Enhanced/env.example",
             "New file. Template for the credentials that used to be hard-coded; the real .env stays out of version control."),
        ],
        "extra_downloads": [
            ("ProjectTwoDashboard.ipynb", "Enhancement3/Enhanced/ProjectTwoDashboard.ipynb",
             "Enhanced dashboard notebook"),
            ("ProjectTwoDashboard_original.ipynb", "Enhancement3/Original/ProjectTwoDashboard.ipynb",
             "Original dashboard notebook"),
        ],
        "narrative": "Enhancement3/Enhancement3_Narrative.docx",
    },
}

ORDER = ["enhancement-1", "enhancement-2", "enhancement-3"]


def esc(s):
    return html.escape(s, quote=True)


def read_text(rel):
    p = SUB / rel
    if not p.exists():
        warn("missing source file: %s" % rel)
        return None
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="latin-1")


WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("  ! %s" % msg)


def copy_download(rel, dest_name=None):
    src = SUB / rel
    if not src.exists():
        warn("missing download: %s" % rel)
        return None
    dest = FILES / (dest_name or src.name)


    data = src.read_bytes()
    if dest.exists():
        if dest.read_bytes() == data:
            return "files/%s" % dest.name
        try:
            dest.unlink()
        except OSError:
            pass
    try:
        dest.write_bytes(data)
    except OSError:


        alt = dest.with_name("%s-current%s" % (dest.stem, dest.suffix))
        alt.write_bytes(data)
        warn("could not replace %s; published as %s" % (dest.name, alt.name))
        return "files/%s" % alt.name
    return "files/%s" % dest.name


FRONT_MATTER = {
    "professional self-assessment",
    "cs 499 module one assignment template",
}


def is_front_matter(text):
    t = text.strip().lower()
    if t == AUTHOR.lower() or t in FRONT_MATTER:
        return True

    return t.startswith(AUTHOR.lower()) and "|" in t


def para_style(para):
    try:
        if para.style is not None and para.style.name:
            return para.style.name.lower()
    except (AttributeError, KeyError):
        pass
    try:
        pPr = para._p.pPr
        if pPr is not None and pPr.pStyle is not None:
            return (pPr.pStyle.val or "").lower()
    except AttributeError:
        pass
    return ""


def paragraph_segments(para):
    from docx.oxml.ns import qn

    segments, text, bold_flags = [], "", []

    def flush():
        if text.strip():
            segments.append((text.strip(), bool(bold_flags) and all(bold_flags)))

    for run in para.runs:
        is_bold = bool(run.bold)
        for node in run._r:
            if node.tag == qn("w:br"):
                flush()
                text, bold_flags = "", []
            elif node.tag in (qn("w:t"), qn("w:delText")):
                chunk = node.text or ""
                if chunk:
                    text += chunk
                    bold_flags.append(is_bold)
    flush()
    return segments


def looks_like_heading(text, is_bold):
    if not is_bold:
        return False
    t = text.strip()
    return 0 < len(t) <= 80 and not t.endswith((".", "?", "!", ":", ";"))


def docx_to_html(rel):
    p = SUB / rel
    if not p.exists():
        warn("narrative not found: %s" % rel)
        return None
    if p.stat().st_size == 0:
        warn("narrative is an empty file: %s" % rel)
        return None
    try:
        import docx
    except ImportError:
        warn("python-docx not installed; narrative left as placeholder (%s)" % rel)
        return None

    doc = docx.Document(str(p))
    out, bullets = [], []

    def flush():
        if bullets:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % b for b in bullets))
            bullets.clear()

    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        style = para_style(para)

        if "list" in style:
            flush_text = para.text.strip()
            if not is_front_matter(flush_text):
                bullets.append(esc(flush_text))
            continue

        for text, is_bold in paragraph_segments(para):
            if is_front_matter(text):
                continue
            styled_heading = style.replace(" ", "") in ("heading1", "heading2")
            deeper_heading = style.startswith("heading") and not styled_heading
            if styled_heading or looks_like_heading(text, is_bold):
                flush()
                out.append("<h3>%s</h3>" % esc(text))
            elif deeper_heading:
                flush()
                out.append("<h4>%s</h4>" % esc(text))
            else:
                flush()
                out.append("<p>%s</p>" % esc(text))
    flush()
    return "\n".join(out) if out else None


def code_viewer(idx, label, original_rel, enhanced_rel, note):
    ext = Path(label).suffix
    lang = LANG.get(ext, "plaintext")
    vid = "v%d" % idx

    panes = []
    tabs = []
    default = "original" if original_rel else "enhanced"

    for version, rel in (("original", original_rel), ("enhanced", enhanced_rel)):
        selected = "true" if version == default else "false"
        tabs.append(
            '<button class="tab" type="button" role="tab" data-version="%s" '
            'aria-selected="%s" aria-controls="%s-%s">%s</button>'
            % (version, selected, vid, version, version.capitalize())
        )
        hidden = "" if version == default else " hidden"
        if rel is None:
            body = ('<p class="empty-pane">Not present in the original artifact — '
                    'this file was added as part of the enhancement.</p>')
        else:
            src = read_text(rel)
            if src is None:
                body = '<p class="empty-pane">Source file could not be read at build time.</p>'
            else:
                body = ('<pre><code class="language-%s">%s</code></pre>'
                        % (lang, esc(src)))
        panes.append(
            '<div class="pane" id="%s-%s" data-version="%s" role="tabpanel"%s>%s</div>'
            % (vid, version, version, hidden, body)
        )

    return """<div class="viewer">
  <div class="viewer-head">
    <span class="viewer-name">%s</span>
    <span class="viewer-note">%s</span>
    <div class="tabs" role="tablist">%s</div>
    <button class="toggle-code" type="button" aria-expanded="false">Show code</button>
  </div>
  <div class="viewer-body" hidden>%s</div>
</div>""" % (esc(label), esc(note), "".join(tabs), "".join(panes))


def page(filename, title, header_html, body_html):
    nav_links = "".join(
        '<a class="navlink%s" href="%s">%s</a>'
        % (" active" if href == filename else "", href, esc(label))
        for href, label in NAV
    )
    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(author)s — Computer Science capstone ePortfolio, Southern New Hampshire University.">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
</head>
<body>

<nav class="site">
  <div class="inner">
    <a class="brand" href="index.html">%(author)s</a>
    %(nav)s
  </div>
</nav>

%(header)s

<main>
%(body)s
</main>

<footer class="site">
  <p>%(author)s &middot; CS 499 Computer Science Capstone &middot; Southern New Hampshire University</p>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="assets/portfolio.js"></script>
</body>
</html>
""" % {"title": esc(title), "author": esc(AUTHOR), "nav": nav_links,
       "header": header_html, "body": body_html}

    (ROOT / filename).write_text(doc, encoding="utf-8")
    print("  wrote %s (%.1f KB)" % (filename, len(doc) / 1024))


def header(eyebrow, h1, tagline):
    return """<header class="page">
  <p class="eyebrow">%s</p>
  <h1>%s</h1>
  <p class="tagline">%s</p>
</header>""" % (esc(eyebrow), esc(h1), esc(tagline))


def pager(prev, nxt):
    left = ('<a class="btn secondary" href="%s">&larr; %s</a>' % (prev[0], esc(prev[1]))
            if prev else "<span></span>")
    right = ('<a class="btn" href="%s">%s &rarr;</a>' % (nxt[0], esc(nxt[1]))
             if nxt else "<span></span>")
    return '<div class="pager">%s%s</div>' % (left, right)


def build_home():
    sa_rel = "ProfessionalSelfAssessment.docx"
    sa_html = docx_to_html(sa_rel)

    if sa_html:
        copy_download(sa_rel)
        self_assessment = '<div class="narrative">%s</div>' % sa_html
    else:
        self_assessment = """<div class="notice">
  <strong>Professional self-assessment — not yet written.</strong>
  This section is generated automatically from
  <code>ProjectSubmission/ProfessionalSelfAssessment.docx</code>,
  which is currently an empty file. Write that document and re-run <code>build.py</code>
  and this placeholder is replaced by the real content.
</div>
<p class="lede">The self-assessment introduces the portfolio: professional strengths and goals,
then how the three artifacts below fit together as a set. It needs to address collaborating in a
team environment, communicating with stakeholders, data structures and algorithms, software
engineering and databases, and security.</p>"""

    cards = []
    for key in ORDER:
        c = CONTENT[key]
        cards.append("""<div class="card artifact-card">
  <p class="meta">Enhancement %d &middot; %s</p>
  <h3>%s</h3>
  <p>%s</p>
  <a class="btn" href="%s.html">View artifact</a>
</div>""" % (c["number"], esc(c["category"]), esc(c["title"]), esc(c["summary"]), key))

    body = """<section id="self-assessment">
  <h2>Professional Self-Assessment</h2>
  %(sa)s
</section>

<section id="code-review">
  <h2>Code Review</h2>
  <p>Before any enhancement work began, I recorded a walkthrough of the three original artifacts:
  what the existing code does, where it falls short on structure, efficiency, security, testing,
  and documentation, and what I planned to change in each of the three categories.</p>
  <p><a class="btn" href="code-review.html">Watch the code review</a></p>
</section>

<section id="artifacts">
  <h2>Enhanced Artifacts</h2>
  <p>Three artifacts, one for each category. Every artifact page shows the original and the
  enhanced source side by side, the reasoning behind the changes, and the course outcomes the
  work demonstrates.</p>
  <div class="grid">
  %(cards)s
  </div>
</section>""" % {"sa": self_assessment, "cards": "\n".join(cards)}

    page("index.html", "%s | %s" % (AUTHOR, SITE_TITLE),
         header("Computer Science Capstone",
                AUTHOR,
                "B.S. Computer Science — Southern New Hampshire University"),
         body)


def build_code_review():
    body = """<section>
  <h2>Informal Code Review</h2>
  <p class="lede">A walkthrough of the three original artifacts, recorded before any enhancement
  work started.</p>

  <div class="video-wrap">
    <iframe src="https://www.youtube-nocookie.com/embed/%(vid)s"
            title="CS 499 Code Review — %(author)s"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen></iframe>
  </div>
  <p><a href="%(url)s" target="_blank" rel="noopener">Open on YouTube</a></p>
</section>

<section>
  <h2>What the review covers</h2>

  <div class="card">
    <h3>Existing functionality</h3>
    <p>A walkthrough of each artifact as it stood before enhancement: what the code does, how it
    is organized, and what it was originally built to accomplish.</p>
  </div>

  <div class="card">
    <h3>Code analysis</h3>
    <p>Where each artifact fell short — structure, logic, efficiency, functionality, security,
    testing, commenting, and documentation. Notably: validation that could be bypassed through
    setters in the Java contact service, an unbalanced search tree that degrades to a linked list
    on sorted input, and database credentials hard-coded into the Python source.</p>
  </div>

  <div class="card">
    <h3>Planned enhancements</h3>
    <p>What I intended to change in each of the three categories, the specific skills each change
    would demonstrate, and how the planned work maps onto the five course outcomes.</p>
  </div>
</section>

<section>
  <h2>The code as reviewed</h2>
  <p>The original, pre-enhancement source discussed in the video is preserved on each artifact
  page under the <strong>Original</strong> tab, so it can be compared directly against the
  enhanced version.</p>
  <div class="grid">
    <div class="card artifact-card">
      <p class="meta">Enhancement 1</p>
      <h3>Contact Service</h3>
      <p>Java. Validation strategy and backing data structure.</p>
      <a class="btn" href="enhancement-1.html">View artifact</a>
    </div>
    <div class="card artifact-card">
      <p class="meta">Enhancement 2</p>
      <h3>Course Planner</h3>
      <p>C++. Binary search tree converted to a self-balancing AVL tree.</p>
      <a class="btn" href="enhancement-2.html">View artifact</a>
    </div>
    <div class="card artifact-card">
      <p class="meta">Enhancement 3</p>
      <h3>Animal Shelter Dashboard</h3>
      <p>Python and MongoDB. Aggregation, indexing, and credential handling.</p>
      <a class="btn" href="enhancement-3.html">View artifact</a>
    </div>
  </div>
</section>

%(pager)s""" % {"vid": YOUTUBE_ID, "url": YOUTUBE_URL, "author": esc(AUTHOR),
                "pager": pager(("index.html", "Home"), ("enhancement-1.html", "Enhancement 1"))}

    page("code-review.html", "Code Review | %s" % SITE_TITLE,
         header("Milestone One", "Code Review",
                "Existing functionality, code analysis, and the enhancement plan"),
         body)


def build_enhancement(key, counter):
    c = CONTENT[key]
    idx = ORDER.index(key)
    prev = ("code-review.html", "Code Review") if idx == 0 else\
           (ORDER[idx - 1] + ".html", "Enhancement %d" % (idx))
    nxt = (ORDER[idx + 1] + ".html", "Enhancement %d" % (idx + 2)) if idx + 1 < len(ORDER) else None

    tags = "".join("<li>%s</li>" % esc(t) for t in c["tags"])

    highlights = "".join(
        '<div class="card"><h3>%s</h3><p>%s</p></div>' % (esc(h), esc(p))
        for h, p in c["highlights"]
    )

    outcomes = "".join(
        '<div class="outcome"><strong>%s</strong><span>%s</span></div>' % (esc(t), esc(d))
        for t, d in c["outcomes"]
    )

    viewers = []
    for label, orig, enh, note in c["files"]:
        counter[0] += 1
        viewers.append(code_viewer(counter[0], label, orig, enh, note))
        stem = Path(label).stem
        suffix = Path(label).suffix
        if orig:
            copy_download(orig, "e%d_%s_original%s" % (c["number"], stem, suffix))
        if enh:
            copy_download(enh, "e%d_%s_enhanced%s" % (c["number"], stem, suffix))

    for name, rel, desc in c.get("extra_downloads", []):
        copy_download(rel, "e%d_%s" % (c["number"], name))

    narrative_html = docx_to_html(c["narrative"])
    copy_download(c["narrative"])
    if narrative_html:
        narrative_block = '<div class="narrative">%s</div>' % narrative_html
    else:
        narrative_block = ('<div class="notice"><strong>Narrative not available at build '
                           'time.</strong>Generated from <code>%s</code>.</div>' % esc(c["narrative"]))

    body = """<section>
  <ul class="tags">%(tags)s</ul>
  <p class="lede">%(summary)s</p>
  <p><strong>Original course:</strong> %(course)s</p>
</section>

<section>
  <h2>Narrative</h2>
  %(narrative)s
</section>

<section>
  <h2>What changed, and why</h2>
  %(highlights)s
</section>

<section>
  <h2>Original vs. Enhanced</h2>
  <p>Use the <strong>Original</strong> and <strong>Enhanced</strong> tabs to compare each file.
  Code is collapsed by default.</p>
  %(viewers)s
</section>

<section>
  <h2>Course outcome alignment</h2>
  %(outcomes)s
</section>

%(pager)s""" % {"tags": tags, "summary": esc(c["summary"]), "course": esc(c["course"]),
                "narrative": narrative_block, "highlights": highlights,
                "viewers": "\n".join(viewers), "outcomes": outcomes,
                "pager": pager(prev, nxt)}

    page("%s.html" % key, "%s | %s" % (c["title"], SITE_TITLE),
         header("Enhancement %d — %s" % (c["number"], c["category"]),
                c["title"], c["summary"].split(".")[0] + "."),
         body)


def main():
    if not SUB.exists():
        sys.exit("ProjectSubmission not found at %s" % SUB)
    FILES.mkdir(exist_ok=True)
    print("Building ePortfolio from %s" % SUB)
    build_home()
    build_code_review()
    counter = [0]
    for key in ORDER:
        build_enhancement(key, counter)
    print("\nDone. %d warning(s)." % len(WARNINGS))
    for w in WARNINGS:
        print("  - %s" % w)


if __name__ == "__main__":
    main()
