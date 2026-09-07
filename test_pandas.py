import pandas as pd
from time import sleep

resources = pd.read_csv("question_bank/infra_resources.csv")

for i in resources[resources['question_id'] == 1].loc[:, 'resource_url']:
    print(i)

sleep(10)
