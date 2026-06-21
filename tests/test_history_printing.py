from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CHAPTER_FILES = sorted(
    path
    for path in ROOT.glob("s*_*/code.py")
    if path.parent.name[1:3].isdigit()
)
AGENT_FILES = sorted(
    path for path in (ROOT / "agents").glob("*.py") if path.name != "__init__.py"
)
TARGET_FILES = CHAPTER_FILES + AGENT_FILES


def test_interactive_agent_scripts_print_full_history() -> None:
    assert TARGET_FILES, "expected interactive agent scripts"

    missing = []
    for path in TARGET_FILES:
        source = path.read_text()
        has_helpers = (
            "def format_history(history: list)" in source
            and "def print_history(history: list)" in source
            and "json.dumps(history, ensure_ascii=False, indent=2, default=_json_default)"
            in source
        )
        has_call = (
            "print_history(history)" in source
            or "print_history(session_history)" in source
        )
        if not (has_helpers and has_call):
            missing.append(str(path.relative_to(ROOT)))

    assert not missing, "missing full-history printing in:\n" + "\n".join(missing)
