import pandas as pd
import cpi
from cpi.errors import CPIObjectDoesNotExist

def adjust_payment_to_inflation():
    INPUT_FILE = "non_marked_data_2.csv"
    #"non_marked_data_2.csv"
    OUTPUT_FILE =  "non_marked_data_2_adj.csv"
    #"non_marked_data_2_infl_adj.csv"

    # 1. Load the dataset
    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    # 2. Ensure the date column is treated as a datetime object
    df['date_filed'] = pd.to_datetime(df['date_filed'])

    # 3. Update the CPI library to ensure you have the latest data
    # (This is optional, but ensures you have the most recent year's data)
    try:
        cpi.update()
    except Exception:
        print("Could not update CPI data, using local version.")

    # 4. Define a function to calculate the adjusted amount
    def get_adjusted_amount(row):
        original_amount = row['payment_amount']
        date_filed = row['date_filed']
        
        # If amount is 0 or NaN, return 0
        if pd.isna(original_amount) or original_amount == 0:
            return 0.0
        
        # cpi.inflate(amount, from_year_or_date, to_year)
        # If to_year is not specified, it defaults to the most recent year available
        try:
            # We inflate from the year of the 'date_filed'
            adjusted = cpi.inflate(original_amount, date_filed.year)
            return round(adjusted, 2)
        except CPIObjectDoesNotExist:
            # This block now correctly catches the error for dates like 1894
            # or future dates where CPI data is missing.
            # We return the original amount as a fallback.
            # print(f"Warning: No CPI data for {date_filed.year}. Returning original amount.")
            return original_amount
            
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Error processing row {row.name}: {e}")
            return original_amount

    # 5. Apply the function to create a new column
    print("Calculating inflation adjustments...")
    df['payment_amount'] = df.apply(get_adjusted_amount, axis=1)

    # 6. Save the result
    df.to_csv(OUTPUT_FILE, index=False)
    
    # 7. Print a sample comparison
    print(f"Done! Saved to {OUTPUT_FILE}")
    print("\nSample comparison:")
    print(df[['date_filed', 'payment_amount']].head())

if __name__ == "__main__":
    adjust_payment_to_inflation()