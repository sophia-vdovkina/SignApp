"""added more tables

Revision ID: 791c37df40e9
Revises: 7bfbd98ecc34
Create Date: 2021-12-21 00:16:04.091744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '791c37df40e9'
down_revision = '7bfbd98ecc34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('has_pressure', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('info',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('organization', sa.String(length=255), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reference_parameters',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('min_value', sa.Float(), nullable=True),
    sa.Column('max_value', sa.Float(), nullable=True),
    sa.Column('mean_value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('security_settings',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('threshold', sa.Float(), nullable=True),
    sa.Column('attempts_num', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('identification_attempts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('signature_id', postgresql.UUID(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('confidence_value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['signature_id'], ['signature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('login_attempts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('signature_id', postgresql.UUID(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['signature_id'], ['signature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('feature', sa.Column('name', sa.String(length=32), nullable=True))
    op.drop_column('feature', 'value_name')
    op.alter_column('person', 'name',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('person', 'surname',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    op.alter_column('person', 'passport',
               existing_type=sa.VARCHAR(length=11),
               nullable=False)
    op.create_unique_constraint(None, 'person', ['passport'])
    op.add_column('signature', sa.Column('set_id', postgresql.UUID(), nullable=True))
    op.add_column('signature', sa.Column('device_id', postgresql.UUID(), nullable=True))
    op.add_column('signature', sa.Column('num_in_file', sa.Integer(), nullable=True))
    op.alter_column('signature', 'file_path',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.create_foreign_key(None, 'signature', 'device', ['device_id'], ['id'])
    op.create_foreign_key(None, 'signature', 'signature_set', ['set_id'], ['id'])
    op.drop_column('signature', 'device_name')
    op.add_column('signature_set', sa.Column('isActive', sa.Boolean(), nullable=False))
    op.drop_constraint('signature_set_signature_id_fkey', 'signature_set', type_='foreignkey')
    op.drop_column('signature_set', 'signature_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('signature_set', sa.Column('signature_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('signature_set_signature_id_fkey', 'signature_set', 'signature', ['signature_id'], ['id'])
    op.drop_column('signature_set', 'isActive')
    op.add_column('signature', sa.Column('device_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'signature', type_='foreignkey')
    op.drop_constraint(None, 'signature', type_='foreignkey')
    op.alter_column('signature', 'file_path',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.drop_column('signature', 'num_in_file')
    op.drop_column('signature', 'device_id')
    op.drop_column('signature', 'set_id')
    op.drop_constraint(None, 'person', type_='unique')
    op.alter_column('person', 'passport',
               existing_type=sa.VARCHAR(length=11),
               nullable=True)
    op.alter_column('person', 'surname',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('person', 'name',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.add_column('feature', sa.Column('value_name', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_column('feature', 'name')
    op.drop_table('login_attempts')
    op.drop_table('identification_attempts')
    op.drop_table('security_settings')
    op.drop_table('reference_parameters')
    op.drop_table('info')
    op.drop_table('device')
    # ### end Alembic commands ###
