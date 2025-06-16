import re

def format_summary(summary: str) -> str:
    """
    Reformat LLM summary into clean Markdown with:
    - Bolded bullet titles
    - Section headers recognized and spaced
    - Graceful fallback for malformed bullets
    """
    lines = summary.strip().split("\n")
    formatted_lines = []
    bullet_symbols = ("-", "•", "*")

    for line in lines:
        stripped = line.strip()

        # Section header (e.g. "Outcome", "Interview Questions", etc.)
        if re.match(r"^[A-Za-z].*:$", stripped):
            formatted_lines.append(f"\n### {stripped[:-1].strip()}")
            continue

        # Bullet point with colon
        if stripped.startswith(bullet_symbols) and ":" in stripped:
            parts = stripped.lstrip("-•* ").split(":", 1)
            title = parts[0].strip().capitalize()
            description = parts[1].strip()
            if title and description:
                formatted_lines.append(f"- **{title}**: {description}")
                continue

        # Regular bullet point without colon
        if stripped.startswith(bullet_symbols):
            cleaned = stripped.lstrip("-•* ").capitalize()
            formatted_lines.append(f"- {cleaned}")
            continue

        # Fallback line
        if stripped:
            formatted_lines.append(stripped)

    return "\n".join(formatted_lines)
