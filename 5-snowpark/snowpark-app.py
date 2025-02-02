# after "pip install snowflake-snowpark-python"

import os
from snowflake.snowpark import Session
import matplotlib.pyplot as plt

pars = {
    "account": os.environ['SNOWFLAKE_ACCOUNT'],
    "user": os.environ['SNOWFLAKE_USER'],
    "password": os.environ['SNOWFLAKE_PASSWORD']
}
session = Session.builder.configs(pars).create()

# with Row collection
query = 'select current_warehouse(), current_role()'
rows = session.sql(query).collect()
for row in rows: print(row)

# with Pandas DataFrame
query = 'select * from test.public.customers_fake limit 100'
df = session.sql(query).to_pandas()
print(df)

df.hist(column="age", bins=10)
plt.show()
