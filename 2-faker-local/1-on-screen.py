# generates 1K rows client-side with fake but realistic test synthetic data
# run from a VSCode Terminal with "python 1-on-screen.py"

from faker import Faker
import pandas as pd
from random import randrange

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