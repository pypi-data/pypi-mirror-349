import sys
from ensure_json import ensure_json, JsonFixError

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python -m ensure-py.cli [--help]\nReads JSON from stdin, repairs it, and writes valid JSON to stdout.\nExits 0 on success, 1 on failure.")
        sys.exit(0)
    try:
        raw = sys.stdin.read()
        result = ensure_json(raw)
        import json
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except JsonFixError as e:
        print(f"JsonFixError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
