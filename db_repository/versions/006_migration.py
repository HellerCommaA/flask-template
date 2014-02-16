from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
service_call = Table('service_call', post_meta,
    Column('ticket', Integer, primary_key=True, nullable=False),
    Column('location', String(length=120)),
    Column('who', String(length=120)),
    Column('phone', String(length=120)),
    Column('email', String(length=120)),
    Column('org', String(length=120)),
    Column('serial', String(length=120)),
    Column('env', String(length=120)),
    Column('product', String(length=120)),
    Column('ptype', String(length=120)),
    Column('date', String(length=120)),
    Column('time', String(length=120)),
    Column('problem', String(length=120)),
    Column('filename', String(length=120), default=ColumnDefault('')),
    Column('solution', String(length=120), default=ColumnDefault('')),
    Column('status', String(length=120), default=ColumnDefault('1')),
    Column('statusdate', String(length=120)),
    Column('postauthor', String(length=120), default=ColumnDefault(',')),
    Column('posttime', String(length=120), default=ColumnDefault(',')),
    Column('postdate', String(length=120), default=ColumnDefault(',')),
    Column('postmessage', String(length=120), default=ColumnDefault(',')),
    Column('totalmessages', Integer, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['service_call'].columns['statusdate'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['service_call'].columns['statusdate'].drop()
