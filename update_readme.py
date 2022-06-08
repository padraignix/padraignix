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
    entries = feedparser.parse("https://blog.quantumlyconfused.com/feed.xml")
    return [
        {
            "title": entry["title"],
            "url": entry["link"],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]

if __name__ == "__main__":
    readme = root / "README.md"
    
    entries = fetch_blog_entries()
    entries_md = "| Post | Date |\n| --------------------------------------- | -------------- |".join(
        ["| [{title}]({url}) | {published} |".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(rewritten, "blog", entries_md)

    readme.open("w").write(rewritten)
  
