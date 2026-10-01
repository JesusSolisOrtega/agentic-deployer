"""
SQLite repository for DeploymentRecord.
"""
from __future__ import annotations

import sqlite3

from app.domain.models import DeploymentIntent, DeploymentRecord, DeploymentStatus
from app.domain.ports import DeploymentRepositoryPort


class SQLiteDeploymentRepository(DeploymentRepositoryPort):
    def __init__(self, db_path: str = "agentic_deployer.db"):
        self.db_path = db_path
        self._memory_conn = sqlite3.connect(":memory:", check_same_thread=False) if db_path == ":memory:" else None
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._memory_conn:
            return self._memory_conn
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS deployments (
                    id TEXT PRIMARY KEY,
                    intent_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result_url TEXT
                )
            ''')

    def save(self, record: DeploymentRecord) -> None:
        with self._get_conn() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO deployments (id, intent_json, status, result_url)
                VALUES (?, ?, ?, ?)
            ''', (
                record.id,
                record.intent.model_dump_json(),
                record.status.value,
                record.result_url
            ))

    def get(self, id: str) -> DeploymentRecord | None:
        with self._get_conn() as conn:
            cursor = conn.execute(
                'SELECT intent_json, status, result_url FROM deployments WHERE id = ?',
                (id,)
            )
            row = cursor.fetchone()
            if not row:
                return None

            intent = DeploymentIntent.model_validate_json(row[0])
            status = DeploymentStatus(row[1])
            result_url = row[2]
            return DeploymentRecord(id=id, intent=intent, status=status, result_url=result_url)

    def get_all(self) -> list[DeploymentRecord]:
        with self._get_conn() as conn:
            cursor = conn.execute(
                'SELECT id, intent_json, status, result_url FROM deployments'
            )
            records = []
            for row in cursor.fetchall():
                intent = DeploymentIntent.model_validate_json(row[1])
                status = DeploymentStatus(row[2])
                result_url = row[3]
                records.append(DeploymentRecord(id=row[0], intent=intent, status=status, result_url=result_url))
            return records
