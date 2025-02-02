# after "pip install snowflake-connector-python"

import os
import snowflake.connector

conn = snowflake.connector.connect(
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'])
cur = conn.cursor()

# fetch row by row
query = 'select current_warehouse(), current_role()'
cur.execute(query)
for row in cur: print(row)

# pass in a Pandas DataFrame
query = 'select * from test.public.customers_fake2 limit 100'
cur.execute(query)
df = cur.fetch_pandas_all()
print(df)
