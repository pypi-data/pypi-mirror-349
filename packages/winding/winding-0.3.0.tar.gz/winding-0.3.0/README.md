# Winding Markdown Extension

Winding is a grammar, AST and parser for the Winding Markdown extension. This extension enhances Markdown, allowing to specify scenes, layout and agentic behaviours.

## Features

- Defines a clear and concise EBNF grammar for the Winding Markdown extension.
- Defines a pure Python parser, based on the Lark standalone parser.
- Defines AST and WindingTransformer, to facilitate the parsing.
- No external dependencies required.

## Installation

You can install the Winding module from PyPI using pip:

```bash
pip install winding
```

## Usage

You can find runnable examples in the `samples/` directory.

Here is a simple example of printing the grammar:

```python
>>> from winding import grammar
>>> print(grammar)

start: (winding | markdown)+

winding: meta_winding | space_winding | inline_winding
meta_winding: "---\n" IDENTIFIER ":" attributes header_winding* "\n---\n" content? 
space_winding: "--\n" IDENTIFIER ":" attributes header_winding* "\n--\n" content?
header_winding: "\n" IDENTIFIER ":" attributes
inline_winding: "@" IDENTIFIER ":" attributes "\n" content?

content: (winding | markdown)+

markdown: (image | TEXT)+

attributes: (IDENTIFIER ("," IDENTIFIER)*)?

image: "![" CAPTION? "]" "(" URI? ")"

IDENTIFIER: /!?[A-Za-z][A-Za-z0-9_.-]*/
URI: /[^\)\n]+/
TEXT: /(?:(?!@\w+:|--|!\[).)*\n+/ 
CAPTION: /[^\]]+/
    
%ignore /[ \t]+/
%ignore "\r" 
```

## Example of parsing a Winding Markdown file

See `samples/dragon.py` for a complete example.

```python
from winding.parser import Lark_StandAlone
from winding.transformer import WindingTransformer
from winding.ast import Winding
from pprint import pprint

parser = Lark_StandAlone()
sample = """---
dragons: portrait-oriented
---
A book about dragons

--
front-cover: portrait-oriented
--
Dragons

@center: large, landscape-oriented
![Flying Wind Dragon](dragon.png)
"""

tree = parser.parse(sample)
ast = WindingTransformer().transform(tree)
pprint(ast, indent=2)
```

This will output the following AST:
```
Winding(at='this',
    attributes=[],
    content=[ 
        Winding(at='dragons',
            attributes=['portrait-oriented'],
            content=[ 
                Markdown(content='A book about dragons\n\n'),
                Winding(at='front-cover', attributes=['portrait-oriented'],
                    content=[ 
                        Markdown(content='Dragons\n\n'),
                        Winding(at='center', attributes=['large', 'landscape-oriented'],
                            content=[Markdown(content=Image(caption='Flying Wind Dragon',
                                               url='dragon.png')),
                                     Markdown(content='\n')]
                                )])])])
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.