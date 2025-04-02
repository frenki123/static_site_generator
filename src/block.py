from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERD_LIST = "unorderd list"
    ORDERD_LIST = "orderd list"

def text_to_blocktype(text:str) -> BlockType:
    if (text.startswith("# ") or 
        text.startswith("## ") or 
        text.startswith("### ") or 
        text.startswith("#### ") or 
        text.startswith("##### ") or 
        text.startswith("###### ")):
        return BlockType.HEADING
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    if _is_quote(text):
        return BlockType.QUOTE
    if _is_unorderd_list(text):
        return BlockType.UNORDERD_LIST
    if _is_orderd_list(text):
        return BlockType.ORDERD_LIST

    return BlockType.PARAGRAPH

def _is_quote(text:str) ->bool:
    lines = text.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def _is_unorderd_list(text:str) -> bool:
    lines = text.split("\n")
    for line in lines:
        if not line.startswith("- "):
            return False
    return True

def _is_orderd_list(text:str) -> bool:
    lines = text.split("\n")
    next = 1
    pattern = r"^(\d+)\.\s.*"
    for line in lines:
        m = re.search(pattern,line)
        if m is None:
            return False
        num = m.group(1)
        if isinstance(num, str):
            if num.isdigit():
                x = int(num)
                if x == next:
                    next += 1
                else:
                    return False
            else:
                return False
        else:
            return False
    return True
