import os
from pathlib import Path
from typing import Optional

from tesslate_chainlit.logger import logger

from ._utils import is_path_inside

# Default tesslate.md file created if none exists
DEFAULT_MARKDOWN_STR = """# Welcome to Tesslate tesslate_chainlit! 🚀🤖
"""


def init_markdown(root: str):
    """Initialize the tesslate_chainlit.md file if it doesn't exist."""
    chainlit_md_file = os.path.join(root, "tesslate_chainlit.md")

    if not os.path.exists(chainlit_md_file):
        with open(chainlit_md_file, "w", encoding="utf-8") as f:
            f.write(DEFAULT_MARKDOWN_STR)
            logger.info(f"Created default tesslate markdown file at {chainlit_md_file}")


def get_markdown_str(root: str, language: str) -> Optional[str]:
    """Get the tesslate_chainlit.md file as a string."""
    root_path = Path(root)
    translated_tesslate_md_path = root_path / f"tesslate_chainlit_{language}.md"
    default_tesslate_md_path = root_path / "tesslate_chainlit.md"

    if (
        is_path_inside(translated_tesslate_md_path, root_path)
        and translated_tesslate_md_path.is_file()
    ):
        tesslate_md_path = translated_tesslate_md_path
    else:
        tesslate_md_path = default_tesslate_md_path
        logger.warning(
            f"Translated markdown file for {language} not found. Defaulting to tesslate_chainlit.md."
        )

    if tesslate_md_path.is_file():
        return tesslate_md_path.read_text(encoding="utf-8")
    else:
        return None
