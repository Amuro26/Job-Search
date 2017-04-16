from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
companies = Table('companies', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('company_name', String(length=40)),
    Column('username', String(length=40)),
    Column('password', String(length=40)),
    Column('address', String(length=40)),
    Column('contact', String(length=20)),
    Column('telephone', String(length=20)),
    Column('email', String(length=120)),
    Column('industry', String(length=20)),
    Column('found_year', String(length=20)),
    Column('introduction', Text),
    Column('last_seen', DateTime),
    Column('logo', String(length=40)),
)

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
    Column('timestamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['companies'].columns['found_year'].create()
    post_meta.tables['jobs'].columns['welfare'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['companies'].columns['found_year'].drop()
    post_meta.tables['jobs'].columns['welfare'].drop()
