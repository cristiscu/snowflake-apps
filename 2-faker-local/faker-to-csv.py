# run from a VSCode Terminal with "python 2-faker-to-csv.py"

from faker import Faker
import pandas as pd

fake = Faker()
output = [{
        "name": fake.name(),
        "address": fake.address(),
        "city": fake.city(),
        "state": fake.state(),
        "email": fake.email()
    } for _ in range(1000)]
df = pd.DataFrame(output)
#print(df)
df.to_csv('customers_fake.csv', index=False)  