"""empty message

Revision ID: d0d9bdf0ffca
Revises: a4c1ff15b4da
Create Date: 2021-06-15 21:25:12.165802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0d9bdf0ffca'
down_revision = 'a4c1ff15b4da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.String(length=64), nullable=True),
    sa.Column('assigned_to', sa.String(length=120), nullable=True),
    sa.Column('eta', sa.String(length=120), nullable=True),
    sa.Column('progress_bar', sa.String(length=120), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_task_name'), 'task', ['task_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_name'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
