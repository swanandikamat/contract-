import re

def clean_text(text: str) -> str:
    """
    Sanitizes and normalizes extracted contract text.
    Removes zero-width characters, normalizes line endings and redundant whitespace.
    """
    if not text:
        return ""
    
    # Replace non-breaking spaces and zero-width spaces
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    
    # Normalize Windows line endings to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Strip split hyphens at line endings (e.g. "li- \n ability" -> "liability")
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Replace 3 or more consecutive newlines with a double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Collapse horizontal whitespace
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    
    return '\n'.join(lines)

def extract_headings(text: str) -> list[str]:
    """
    Extracts potential section/heading lines from contract text.
    Identifies patterns like 'SECTION 1.', 'Article II', '1.1 Limitation of Liability', 'SECTION 10 - GOVERNING LAW'.
    """
    heading_pattern = re.compile(
        r'^(?:SECTION|ARTICLE|CLAUSE|\d+(\.\d+)*)\b.*$',
        re.IGNORECASE | re.MULTILINE
    )
    return heading_pattern.findall(text)
