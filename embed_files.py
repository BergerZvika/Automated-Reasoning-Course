"""
embed_files.py  —  Pre-embeds lab source/benchmark files into each lab's index.html
                   as window.LAB_FILES so the viewer works with file:// protocol.

Run from the repo root:  python embed_files.py
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
LABS = [d for d in os.listdir(ROOT)
        if os.path.isdir(os.path.join(ROOT, d))
        and os.path.isfile(os.path.join(ROOT, d, 'index.html'))]

for lab in sorted(LABS):
    lab_dir = os.path.join(ROOT, lab)
    html_path = os.path.join(lab_dir, 'index.html')

    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    # Collect all file hrefs that are .py / .cnf / .smt2
    hrefs = re.findall(r'href="([^"]+\.(?:py|cnf|smt2|smt))"', html)
    if not hrefs:
        print(f'  {lab}: no files, skipping')
        continue

    files = {}
    for href in hrefs:
        fpath = os.path.join(lab_dir, href)
        if not os.path.isfile(fpath):
            print(f'  {lab}: missing {href}, skipping')
            continue
        with open(fpath, encoding='utf-8', errors='replace') as f:
            files[href] = f.read()

    if not files:
        print(f'  {lab}: no readable files, skipping')
        continue

    # Build the <script> block
    # Escape </script> inside the JSON so it cannot break the surrounding script tag
    js = 'window.LAB_FILES=' + json.dumps(files, ensure_ascii=False).replace('</script>', '<\\/script>') + ';'
    script_tag = f'<script id="lab-files-data">\n{js}\n</script>\n'

    # Remove existing embedded block if present
    html = re.sub(r'<script id="lab-files-data">.*?</script>\n?', '', html, flags=re.DOTALL)

    # Insert before viewer.js
    html = html.replace('<script src="../viewer.js"></script>',
                        script_tag + '<script src="../viewer.js"></script>')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  {lab}: embedded {len(files)} files')

print('Done.')
