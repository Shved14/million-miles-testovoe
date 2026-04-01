"""create cars

Revision ID: 0001
Revises: 
Create Date: 2026-03-31

"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("brand", sa.String(length=100), nullable=False),
        sa.Column("model", sa.String(length=150), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cars_brand"), "cars", ["brand"], unique=False)
    op.create_index(op.f("ix_cars_created_at"), "cars", ["created_at"], unique=False)
    op.create_index(op.f("ix_cars_id"), "cars", ["id"], unique=False)
    op.create_index(op.f("ix_cars_model"), "cars", ["model"], unique=False)
    op.create_index(op.f("ix_cars_year"), "cars", ["year"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cars_year"), table_name="cars")
    op.drop_index(op.f("ix_cars_model"), table_name="cars")
    op.drop_index(op.f("ix_cars_id"), table_name="cars")
    op.drop_index(op.f("ix_cars_created_at"), table_name="cars")
    op.drop_index(op.f("ix_cars_brand"), table_name="cars")
    op.drop_table("cars")
