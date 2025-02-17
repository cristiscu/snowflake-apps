# generates 1K rows client-side with fake but realistic test synthetic data
# run from a VSCode Terminal with "python to-csv.py"

from faker import Faker
import pandas as pd
from random import randrange
import matplotlib.pyplot as plt

fake = Faker()
output = [{
        "name": fake.name(),
        "address": fake.address(),
        "city": fake.city(),
        "state": fake.state(),
        "email": fake.email(),
        "age": 10 + randrange(70)
    } for _ in range(1000)]
df = pd.DataFrame(output)
print(df)

# ~ETL/ELT
df.loc[df["age"] < 20, "age"] = 20

df.hist(column="age", bins=10)
plt.show()

df.to_csv('../3-snowflake-extension/customers_fake.csv', index=False)
