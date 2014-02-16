from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
service_call = Table('service_call', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ticket', Integer),
    Column('who', String),
    Column('location', String),
    Column('date', String),
    Column('problem', String),
    Column('sysnum', String),
    Column('rocunum', String),
    Column('botnum', String),
    Column('solution', String, default=ColumnDefault('')),
    Column('status', String),
    Column('history', String, default=ColumnDefault('')),
    Column('filename', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['service_call'].columns['filename'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['service_call'].columns['filename'].drop()
