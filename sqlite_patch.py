# SQLite Version Patch for ChromaDB
# This file should be imported before importing chromadb

import sys

try:
    # Try to use pysqlite3 if available (newer SQLite)
    import pysqlite3.dbapi2 as sqlite3
    # Replace the built-in sqlite3 module
    sys.modules['sqlite3'] = sqlite3
    print("Using pysqlite3-binary for SQLite compatibility")
except ImportError:
    # Fall back to built-in sqlite3
    import sqlite3
    print(f"Using built-in SQLite version: {sqlite3.sqlite_version}")
