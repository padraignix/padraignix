import feedparser
import httpx
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)
  
def fetch_blog_entries():
    d = feedparser.parse("https://blog.quantumlyconfused.com/feed.xml")
    return [
        {
            "title": d.entries[i].title,
            "url": d.entries[i].link,
            "published": d.entries[i].published.split("T")[0],
        }
        for i in range(len(d.entries))
    ]

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    
    entries = fetch_blog_entries()
    entries_md = "| Post | Date |\n| --------------------------------------- | -------------- |\n"
    entries_md += "\n".join(
        ["| [{title}]({url}) | {published} |".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)
  
