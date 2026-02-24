#!/usr/bin/env python3
"""
NIMA Core Database Initialization Script

Initializes SQLite database for NIMA memory storage.
Creates tables, indexes, FTS5 virtual table, and sync triggers.

Usage:
    python scripts/init_db.py [--db-path PATH]

Environment:
    NIMA_DATA_DIR: Override default ~/.nima data directory
    NIMA_HOME: Alias for NIMA_DATA_DIR (for compatibility)
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path
from typing import Optional


def get_db_path(args_path: Optional[str] = None) -> Path:
    """Resolve database path from args, env, or default."""
    if args_path:
        return Path(args_path)
    
    nima_home = os.environ.get('NIMA_HOME') or os.environ.get('NIMA_DATA_DIR', os.path.expanduser('~/.nima'))
    return Path(nima_home) / 'memory' / 'graph.sqlite'


def init_database(db_path: Path, verbose: bool = False) -> None:
    """Initialize the NIMA database with tables, indexes, and FTS."""
    
    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"📂 Initializing database at: {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        
        # Create tables
        conn.executescript("""
        -- Core memory nodes table
        CREATE TABLE IF NOT EXISTS memory_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            layer TEXT NOT NULL,
            text TEXT NOT NULL,
            summary TEXT NOT NULL,
            who TEXT DEFAULT '',
            affect_json TEXT DEFAULT '{}',
            session_key TEXT DEFAULT '',
            conversation_id TEXT DEFAULT '',
            turn_id TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            embedding BLOB DEFAULT NULL,
            fe_score REAL DEFAULT 0.5,
            strength REAL DEFAULT 1.0,
            decay_rate REAL DEFAULT 0.01,
            last_accessed INTEGER DEFAULT 0,
            is_ghost INTEGER DEFAULT 0,
            dismissal_count INTEGER DEFAULT 0
        );

        -- Memory relationships (graph edges)
        CREATE TABLE IF NOT EXISTS memory_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            relation TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (source_id) REFERENCES memory_nodes(id) ON DELETE CASCADE,
            FOREIGN KEY (target_id) REFERENCES memory_nodes(id) ON DELETE CASCADE
        );

        -- Conversation turn structure
        CREATE TABLE IF NOT EXISTS memory_turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turn_id TEXT UNIQUE NOT NULL,
            input_node_id INTEGER,
            contemplation_node_id INTEGER,
            output_node_id INTEGER,
            timestamp INTEGER NOT NULL,
            affect_json TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (input_node_id) REFERENCES memory_nodes(id) ON DELETE SET NULL,
            FOREIGN KEY (contemplation_node_id) REFERENCES memory_nodes(id) ON DELETE SET NULL,
            FOREIGN KEY (output_node_id) REFERENCES memory_nodes(id) ON DELETE SET NULL
        );

        -- Full-text search virtual table
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            text, summary, who, layer,
            content=memory_nodes,
            content_rowid=id
        );
        
        -- FTS5 sync triggers
        CREATE TRIGGER IF NOT EXISTS memory_fts_insert AFTER INSERT ON memory_nodes BEGIN
            INSERT INTO memory_fts(rowid, text, summary, who, layer)
            VALUES (NEW.id, NEW.text, NEW.summary, NEW.who, NEW.layer);
        END;

        CREATE TRIGGER IF NOT EXISTS memory_fts_update AFTER UPDATE OF text, summary, who, layer ON memory_nodes BEGIN
            INSERT INTO memory_fts(memory_fts, rowid, text, summary, who, layer)
            VALUES ('delete', OLD.id, OLD.text, OLD.summary, OLD.who, OLD.layer);
            INSERT INTO memory_fts(rowid, text, summary, who, layer)
            VALUES (NEW.id, NEW.text, NEW.summary, NEW.who, NEW.layer);
        END;

        CREATE TRIGGER IF NOT EXISTS memory_fts_delete AFTER DELETE ON memory_nodes BEGIN
            INSERT INTO memory_fts(memory_fts, rowid, text, summary, who, layer)
            VALUES ('delete', OLD.id, OLD.text, OLD.summary, OLD.who, OLD.layer);
        END;

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_nodes_timestamp ON memory_nodes(timestamp);
        CREATE INDEX IF NOT EXISTS idx_nodes_layer ON memory_nodes(layer);
        CREATE INDEX IF NOT EXISTS idx_nodes_who ON memory_nodes(who);
        CREATE INDEX IF NOT EXISTS idx_nodes_session ON memory_nodes(session_key);
        CREATE INDEX IF NOT EXISTS idx_nodes_conversation ON memory_nodes(conversation_id);
        CREATE INDEX IF NOT EXISTS idx_nodes_fe_score ON memory_nodes(fe_score);
        CREATE INDEX IF NOT EXISTS idx_edges_source ON memory_edges(source_id);
        CREATE INDEX IF NOT EXISTS idx_edges_target ON memory_edges(target_id);
        CREATE INDEX IF NOT EXISTS idx_edges_relation ON memory_edges(relation);
        CREATE INDEX IF NOT EXISTS idx_turns_timestamp ON memory_turns(timestamp);
        CREATE INDEX IF NOT EXISTS idx_turns_turn_id ON memory_turns(turn_id);
    """)
    
        conn.commit()
        
        # Verify tables created
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()
    
    if verbose:
        print("✅ Database initialized successfully")
        print(f"   Tables created: {len(tables)}")
        for table in tables:
            print(f"   - {table}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize NIMA Core database"
    )
    parser.add_argument(
        '--db-path',
        type=str,
        help='Path to database file (default: ~/.nima/memory/graph.sqlite)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        db_path = get_db_path(args.db_path)
        init_database(db_path, verbose=args.verbose)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
