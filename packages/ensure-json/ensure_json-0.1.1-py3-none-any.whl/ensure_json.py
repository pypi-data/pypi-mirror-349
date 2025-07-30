import json
import re

class JsonFixError(Exception):
    """Raised when JSON repair fails."""
    def __init__(self, message, raw):
        super().__init__(message)
        self.raw = raw

def ensure_json(raw: str, schema=None):
    """
    Repairs and parses 'almost-JSON' text from LLMs.
    Optionally validates with a schema (e.g., pydantic model).
    """
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = _try_repair(raw)
    if schema:
        try:
            return schema.parse_obj(parsed)
        except Exception:
            raise JsonFixError("Schema validation failed", raw)
    return parsed

async def ensure_json_async(raw: str, schema=None):
    return ensure_json(raw, schema)

def _try_repair(raw: str):
    text = raw

    # 1. Remove markdown fences
    text = re.sub(r"^\s*```(?:json)?|```\s*$", "", text, flags=re.MULTILINE)

    # 2. Slice from first { or [
    brace_pos = min([i for i in [text.find("{"), text.find("[")] if i != -1] or [0])
    text = text[brace_pos:]

    # 3. Remove trailing commas
    text = re.sub(r",\s*([}\]])", r"\1", text)

    # 4. Single ➜ double quotes for keys
    text = re.sub(r"'([^']+)':", r'"\1":', text)

    # 5. Quote bare keys
    text = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', text)

    # 6. Balance braces/brackets
    if text.count("{") == text.count("}") + 1:
        text += "}"
    if text.count("[") == text.count("]") + 1:
        text += "]"

    # 7. Try parsing again
    try:
        return json.loads(text)
    except Exception:
        raise JsonFixError("Failed to repair and parse JSON", raw)
