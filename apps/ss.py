from pathlib import Path

p = Path("/home/fulvio/loko/projects")

for el in p.glob("**/services.py"):
    with el.open() as o:
        txt = o.read()
        if "Sanic" in txt and "extract_value" in txt and "file" in txt:
            print(el, txt)
