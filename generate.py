#!/usr/bin/env python3
import os, json, jinja2

TEMPLATE = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>红楼梦中英对照</title>
<style>
  body {
    margin: 20px;
    line-height: 1.5;
    font-size: 12pt; /* 小四 */
  }
  .chapter { margin-bottom: 50px; }
  .title { font-size: 14pt; font-weight: bold; margin-bottom: 15px; }
  .pair { display: flex; gap: 20px; }
  .col { flex: 1; min-width: 0; }
  .zh { font-family: SimSun, serif; }
  .en { font-family: "Times New Roman", serif; }
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 6px;
    background: #fafafa;
    margin: 0;
  }
</style>
</head>
<body>
<h1 style="text-align:center;">《红楼梦》 中英对照</h1>
{% for ch in chapters %}
<div class="chapter">
  <div class="title">{{ch.title}}</div>
  <div class="pair">
    <div class="col zh"><h3>原文</h3><pre>{{ch.original}}</pre></div>
    <div class="col en"><h3>译文</h3><pre>{{ch.translation}}</pre></div>
  </div>
</div>
{% endfor %}
</body>
</html>
"""

def main():
    in_dir = "translations"
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)

    chapters = []
    files = sorted([f for f in os.listdir(in_dir) if f.endswith(".json")])
    for fname in files:
        with open(os.path.join(in_dir, fname), "r", encoding="utf-8") as f:
            ch = json.load(f)
        chapters.append({
            "index": ch["index"],
            "title": ch["title"],
            "original": ch.get("text", ch.get("original", "")),
            "translation": ch["translation"]
        })

    html = jinja2.Template(TEMPLATE).render(chapters=chapters)
    outpath = os.path.join(out_dir, "hongloumeng_ZHvsEN.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 已生成", outpath)

if __name__ == "__main__":
    main()
