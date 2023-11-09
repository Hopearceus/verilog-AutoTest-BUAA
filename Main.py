import sys

from Run import run

if __name__ == "__main__":
    run(template_used=sys.argv[1:] if len(sys.argv) > 1 else None)
