import pandas as pd
from datetime import datetime as dt
def func():
    INPUT_FILE = "Siemens2_c.csv"
    #"results_final_comp_4_cleaned.csv"
    OUTPUT_FILE = "Siemens2_c_d.csv"
    #"results_final_comp_4_cleaned_d.csv"

    data = pd.read_csv(INPUT_FILE)

    data["date_filed"] = pd.to_datetime(data["date_filed"])
    data["year"] = data["date_filed"].dt.year

    print(data.head())
    data.to_csv(OUTPUT_FILE, index=False)

def main():
    func()
   
if __name__ == "__main__":
    main()