
import json


def parse(filename: str) -> dict[str, list[str]]:
    with open(filename, "r") as f:
        file_json = json.load(f)
        return {
            k.replace("web:", "", 1): [s.get('selector', None) for s in json.loads(v)]
            for (k, v)
            in file_json.items()
            if k.startswith("web:")
        }

def for_url(url: str, filename: str | None = None) -> list[str]:
    if filename:
        all_selectors = parse(filename)
        return next((v for (k, v) in all_selectors.items() if k in url), [])
    else:
        return []
