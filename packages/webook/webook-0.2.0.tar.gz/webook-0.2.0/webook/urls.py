from dataclasses import dataclass
from mistletoe import Document
from mistletoe.token import Token
from mistletoe.span_token import Link

@dataclass
class URL:
    url: str
    title: str

def get_links(token: Token) -> list[Link]:
    if isinstance(token, Link):
        return [token]
    if "children" in vars(token) or "_children" in vars(token):
        links = []
        for child in token.children:
            links.extend(get_links(child))
        return links
    return []

def parse(filename: str) -> list[URL]:
    with open(filename, 'r') as f:
        md = Document(f)
        return [
            URL(link.target, link.children[0].content)
            for link in get_links(md)
        ]