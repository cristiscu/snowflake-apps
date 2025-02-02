-- run from (paid) producer account

create or replace secure function test.public.get_fake_row(num integer)
    returns table (name string, address string, city string, state string, email string)
    language python
    runtime_version = 3.9
    packages = ('faker')
    handler = 'FakeGen'
as $$
from faker import Faker

class FakeGen:
    def process(self, num):
        f = Faker()
        for _ in range(num):
            yield (f.name(), f.address(), f.city(), f.state(), f.email())
$$;

select * from table(test.public.get_fake_row(100));

-- ==============================================================
-- create share for the UDF + share w/ another paid account from the same org
create share fake_share;

grant usage on database test to share fake_share;
grant usage on schema test.public to share fake_share;
grant usage on function test.public.get_fake_row(integer) to share fake_share;

alter share fake_share add accounts = YICTMGU.RXB41860;
show shares;

-- ==============================================================
-- run from (paid) consumer account, w/ ACCOUNTADMIN
-- after Data > Private Sharing > FAKE_SHARE in Direct Shares --> Get as DB_FAKE_SHARE database
select * from table(db_fake_share.public.get_fake_row(50));
