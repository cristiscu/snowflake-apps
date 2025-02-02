-- ====================================================
-- generate fake random data

-- see https://docs.snowflake.com/en/sql-reference/functions/generator
select 1
from table(generator(rowcount => 1000));

-- see https://docs.snowflake.com/en/sql-reference/functions-data-generation
select randstr(10, random()) || ' ' || randstr(15, random()) as name
from table(generator(rowcount => 1000));

select randstr(10, random()) || ' ' || randstr(15, random()) as name,
    floor(abs(normal(40, 10, random()))) as age
from table(generator(rowcount => 1000));

create or replace table test.public.customers_fake(name string, age integer)
as select randstr(10, random()) || ' ' || randstr(15, random()) as name,
    floor(abs(normal(40, 10, random()))) as age
    from table(generator(rowcount => 1000));
select * from test.public.customers_fake;

-- ====================================================
-- get sample data from existing tables

select *
from snowflake_sample_data.tpch_sf1.customer
limit 1000;

-- see https://docs.snowflake.com/en/sql-reference/constructs/sample
select c_name, c_address, c_phone
from snowflake_sample_data.tpch_sf1.customer
sample (1000 rows);

create or replace table test.public.customers_fake(
    name string, address string, phone string)
as select c_name, c_address, c_phone
    from snowflake_sample_data.tpch_sf1.customer
    sample (1000 rows);
select * from test.public.customers_fake;

-- ====================================================
-- get look-alike data from existing tables

-- see https://docs.snowflake.com/en/sql-reference/stored-procedures/generate_synthetic_data
call SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
    'datasets': [{
        'input_table': 'snowflake_sample_data.tpch_sf1.customer',
        'output_table': 'test.public.customers_fake',
        'columns': { 'c_name': { 'join_key': FALSE } }
    }],
    'replace_output_tables': TRUE
});
select * from test.public.customers_fake;
