from ensure_json import ensure_json, JsonFixError

if __name__ == "__main__":
    # Example of "almost-JSON" input (extra comma, unquoted keys, code block)
    input_str = '```json { name: "Alice", age: 42, }'
    try:
        result = ensure_json(input_str)
        print(result)
    except JsonFixError as e:
        print(f"JsonFixError: {e}")
    except Exception as e:
        print(f"Error: {e}")
