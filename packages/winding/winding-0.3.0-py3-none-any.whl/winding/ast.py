from dataclasses import dataclass, field
from typing import List, Union

@dataclass
class Image:
    caption: str = field(metadata={"description": "Image caption."})
    url:     str = field(metadata={"description": "Image URL."})

@dataclass
class Markdown:
    content: Union[str, 'Markdown', Image] = field(
        metadata={"description": "Plain text, nested Markdown, or Image node."}
    )

@dataclass
class Winding:
    at:         str                 = field(
        default="this",
        metadata={"description": "The @at recipient, a valid identifier."}
    )
    attributes: List[str]           = field(
        default_factory=list,
        metadata={"description": "Modifiers (e.g., size, orientation, !negation)."}
    )
    content:    List[Union[Markdown, 'Winding']] = field(
        default_factory=list,
        metadata={"description": "Child nodes: text (Markdown), or nested directives (Winding)."}
    )
