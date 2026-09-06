import csv
import pandas as pd

def load_csv(choice, csv_type):
    with open(f"question_bank/{choice}_{csv_type}.csv", "r") as file:
        return pd.read_csv(file)

    