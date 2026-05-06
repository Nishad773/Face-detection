"""create stream sessions and roi records

Revision ID: 0001_create_roi_records
Revises: 
Create Date: 2026-05-06 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_roi_records"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stream_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_stream_sessions_source_id", "stream_sessions", ["source_id"], unique=True)

    op.create_table(
        "roi_records",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["stream_sessions.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_roi_records_session_id", "roi_records", ["session_id"], unique=False)
    op.create_index("ix_roi_records_timestamp", "roi_records", ["timestamp"], unique=False)
    op.create_index("ix_roi_records_session_id_timestamp", "roi_records", ["session_id", "timestamp"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_roi_records_session_id_timestamp", table_name="roi_records")
    op.drop_index("ix_roi_records_timestamp", table_name="roi_records")
    op.drop_index("ix_roi_records_session_id", table_name="roi_records")
    op.drop_table("roi_records")
    op.drop_index("ix_stream_sessions_source_id", table_name="stream_sessions")
    op.drop_table("stream_sessions")
