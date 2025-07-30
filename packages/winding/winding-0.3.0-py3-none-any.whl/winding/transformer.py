from .parser import Transformer, Token, v_args
from .ast import Image, Markdown, Winding

@v_args(inline=True)
class WindingTransformer(Transformer):
    def IDENTIFIER(self, tk):
        return tk.value

    def CAPTION(self, tk):
        return tk.value

    def TEXT(self, tk):
        return tk.value

    def attributes(self, *ids):
        return list(ids)

    def image(self, caption="", url=Token("URI", "")):
        if isinstance(caption, Token):
            url, caption = caption, ""        
        return Image(caption=caption, url=url.value)

    def markdown(self, *items):
        nodes = []
        for it in items:
            if isinstance(it, Image):
                nodes.append(Markdown(content=it))
            else:
                nodes.append(Markdown(content=it))
        return nodes if len(nodes) > 1 else nodes[0]

    def inline_winding(self, at, attrs, *children):
        body = []
        for c in children:
            if isinstance(c, list):
                body.extend(c)
            else:
                body.append(c)
        return Winding(at=at, attributes=attrs, content=body)

    def meta_winding(self, at, attrs, *children):
        return self.inline_winding(at, attrs, *children)

    def space_winding(self, at, attrs, *children):
        return self.inline_winding(at, attrs, *children)

    def header_winding(self, at, attrs, *children):
        return Winding(at=at, attributes=attrs, content=[])


    def content(self, *items):
        # flatten lists
        flat = []
        for i in items:
            if isinstance(i, list):
                flat.extend(i)
            else:
                flat.append(i)
        return flat

    def start(self, *items):
        # top-level wrapper
        return Winding(at="this", attributes=[], content=list(items))

    def __default__(self, data, children, meta):
        # catch-all: flatten nested lists or return sole child
        flat = []
        for c in children:
            if isinstance(c, list):
                flat.extend(c)
            else:
                flat.append(c)
        if len(flat) == 1:
            return flat[0]
        return flat