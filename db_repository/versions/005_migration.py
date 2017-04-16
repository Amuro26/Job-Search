from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
companies = Table('companies', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('company_name', VARCHAR(length=40)),
    Column('username', VARCHAR(length=40)),
    Column('password', VARCHAR(length=40)),
    Column('address', VARCHAR(length=40)),
    Column('contact', VARCHAR(length=20)),
    Column('telephone', VARCHAR(length=20)),
    Column('email', VARCHAR(length=120)),
    Column('industry', VARCHAR(length=20)),
    Column('introduction', TEXT),
    Column('last_seen', DATETIME),
    Column('logo', VARCHAR(length=40)),
    Column('found_year', VARCHAR(length=20)),
    Column('type', VARCHAR(length=20)),
)

companies = Table('companies', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('company_name', String(length=40)),
    Column('username', String(length=40)),
    Column('password_hash', String(length=40)),
    Column('address', String(length=40)),
    Column('contact', String(length=20)),
    Column('telephone', String(length=20)),
    Column('email', String(length=120)),
    Column('industry', String(length=20)),
    Column('type', String(length=20)),
    Column('found_year', String(length=20)),
    Column('introduction', Text),
    Column('last_seen', DateTime),
    Column('logo', String(length=40), default=ColumnDefault('/static/avatar/default.jpg')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['companies'].columns['password'].drop()
    post_meta.tables['companies'].columns['password_hash'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['companies'].columns['password'].create()
    post_meta.tables['companies'].columns['password_hash'].drop()
