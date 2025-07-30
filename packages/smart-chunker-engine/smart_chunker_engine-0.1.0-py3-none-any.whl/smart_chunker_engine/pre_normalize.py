from typing import Optional, Dict, Any
import unicodedata
import re

class PreNormalizer:
    """Performs text normalization: NFC, control character removal, whitespace cleanup."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize PreNormalizer with optional configuration."""
        self.config = config or {}

    def normalize(self, text: str) -> str:
        """Normalize input text (NFC, remove control chars, collapse spaces).

        Args:
            text (str): Raw input text.
        Returns:
            str: Normalized text.
        """
        # Unicode NFC normalization
        text = unicodedata.normalize("NFC", text)
        # Remove control characters (except \n, \t)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
        # Collapse multiple spaces/tabs/newlines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n+", "\n", text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text 