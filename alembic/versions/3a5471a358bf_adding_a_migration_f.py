"""Adding a migration for the exploitability report.

Revision ID: 3a5471a358bf
Revises: 191d0453cc07
Create Date: 2013-10-25 07:07:33.968691

"""

# revision identifiers, used by Alembic.
revision = '3a5471a358bf'
down_revision = '4aacaea3eb48'

from alembic import op
from socorro.lib import citexttype, jsontype
from socorro.lib.migrations import load_stored_proc

import sqlalchemy as sa
from sqlalchemy import types
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column




def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('TRUNCATE exploitability_reports CASCADE');
    op.add_column(u'exploitability_reports', sa.Column(u'version_string', sa.TEXT(), nullable=True))
    op.add_column(u'exploitability_reports', sa.Column(u'product_name', sa.TEXT(), nullable=True))
    op.add_column(u'exploitability_reports', sa.Column(u'product_version_id', sa.INTEGER(), nullable=False))
    ### end Alembic commands ###
    load_stored_proc(op, ['update_exploitability.sql'])
        
    for i in range(15, 30):
        backfill_date = '2013-11-%s' % i
        op.execute("""
            SELECT backfill_exploitability('%s')
        """ % backfill_date)
    op.execute(""" COMMIT """)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'exploitability_reports', u'product_version_id')
    op.drop_column(u'exploitability_reports', u'product_name')
    op.drop_column(u'exploitability_reports', u'version_string')
    load_stored_proc(op, ['update_exploitability.sql'])
    ### end Alembic commands ###