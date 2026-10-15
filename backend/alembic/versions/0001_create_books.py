"""create books table

Revision ID: 0001_create_books
Revises: 
Create Date: 2026-10-16 01:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_books"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="AVAILABLE"),
        sa.Column("borrower_name", sa.String(length=255), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_books_title", "books", ["title"])
    op.create_index("ix_books_category", "books", ["category"])
    op.create_index("ix_books_status", "books", ["status"])

def downgrade():
    op.drop_index("ix_books_status", table_name="books")
    op.drop_index("ix_books_category", table_name="books")
    op.drop_index("ix_books_title", table_name="books")
    op.drop_table("books")
