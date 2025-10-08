"""Entry point for running eleventh.decks.cluster as a module.

Usage
-----
    poetry run python -m eleventh.decks.cluster start --addresses http://127.0.0.1:8001 http://127.0.0.1:8002
"""

from eleventh.decks.cluster import main

if __name__ == "__main__":
    main()
