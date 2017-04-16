from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
jobs = Table('jobs', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('company_id', Integer),
    Column('user_id', Integer),
    Column('company_name', String(length=20)),
    Column('job_name', String(length=20)),
    Column('email', String(length=40)),
    Column('industry', String(length=20)),
    Column('salary', String(length=10)),
    Column('welfare', Text),
    Column('work_place', String(length=20)),
    Column('requirement', Text),
    Column('job_detail', Text),
    Column('PS', Text),
    Column('avatar', String(length=20)),
    Column('timestamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['jobs'].columns['avatar'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['jobs'].columns['avatar'].drop()
