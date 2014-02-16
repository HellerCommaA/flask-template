from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
survey = Table('survey', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('key', String),
    Column('date', String),
    Column('event', String),
    Column('mission', String),
    Column('terrain', String),
    Column('los', String),
    Column('mesh', String),
    Column('manip', String),
    Column('timeofday', String),
    Column('priort', String),
    Column('typeofs', String),
    Column('q1', String),
    Column('q2', String),
    Column('q3', String),
    Column('q4', String),
    Column('q5', String),
    Column('q6', String),
    Column('q7', String),
    Column('q8', String),
    Column('q9', String),
    Column('q10', String),
    Column('q11', String),
    Column('q12', String),
    Column('q13', String),
    Column('q14', String),
    Column('q15', String),
    Column('q16', String),
)

survey_master = Table('survey_master', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('key', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['survey'].create()
    post_meta.tables['survey_master'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['survey'].drop()
    post_meta.tables['survey_master'].drop()
