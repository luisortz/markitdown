# packages/markitdown/src/markitdown/summary.py
from __future__ import annotations

def summarize_markdown(md: str, max_lines: int = 25) -> str:
    """
    Return a condensed preview of a Markdown document.

    - Keeps the first `max_lines` non-empty lines.
    - Avoids cutting inside fenced code blocks when possible.
    - Appends an ellipsis if content was truncated.
    """
    if not md:
        return md

    lines = md.splitlines()
    out: list[str] = []
    non_empty = 0
    in_fence = False

    for ln in lines:
        # track fenced code blocks
        if ln.strip().startswith("```"):
            in_fence = not in_fence

        out.append(ln)
        if ln.strip():
            non_empty += 1

        # stop only when not inside a fence
        if non_empty >= max_lines and not in_fence:
            break

    truncated = len(lines) > len(out)
    result = "\n".join(out)
    if truncated:
        if not result.endswith("\n"):
            result += "\n"
        result += "\n…\n"
    return result
