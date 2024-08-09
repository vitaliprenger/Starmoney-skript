import pandas as pd
import csv  # Import Python's standard csv module
import re

# Custom function to format cells
def format_csv(val, column_name):
   if val == '"None"' or val is None:
      return ''
   if column_name in skip_columns:
        return val  # Skip formatting for specified columns
   if isinstance(val, (int, float)):
      if val.is_integer():  # Check if the number is an integer
         return f'{int(val):,}'.replace(',', '')
      else:
         return f'{val:,.2f}'.replace(',', '').replace('.', ',')
   elif isinstance(val, str) and re.match(pattern, val):
        return val
   else:
      if '.' in val:
        return f'"{str(val).rstrip('0').rstrip('.')}"'
      else:
        return f'"{str(val)}"'

def german_to_float(german_str):
   try:
      if german_str is None:
         return None
      # Replace comma with period
      return float(german_str.replace('.', '').replace(',', '.'))
   except ValueError:
      return None  # Handle cases where conversion fails
     
# Define the regex pattern for the format DD.MM.YYYY
pattern = r'^\d{2}\.\d{2}\.\d{4}$'

# Load the two CSV files
file1 = '1056547415_EUR_20240809_144952.txt'
file2 = 'hibiscus-export-20240809.csv'
output_file = '/mnt/c/Users/prv/Downloads/sm_new.txt'

# Define the list of columns to skip formatting
skip_columns = {'Splittbuchung - Auftraggeber / Name','Splittbuchung - Verwendungszweckzeile 1','Splittbuchung - Kategorie','Splittbuchung - Unterkategorie','Splittbuchung - Kostenstelle','Splittbuchung - SteuersatzWaehr','Splittbuchung - SteuerbetragWaehr','Splittbuchung - Fibu-Nr.'}  # Replace with your actual column names

# Load CSV files
df1 = pd.read_csv(file1, delimiter=';', decimal=',')
df2 = pd.read_csv(file2, delimiter=';', decimal=',')

# Fill NaN values in df1 with empty strings
df1 = df1.fillna('')

# df1 = df1.apply(lambda x: x.fillna('') if x.dtype == 'object' else x)
# df1 = df1.apply(lambda x: x.fillna('') if x.dtype == 'int' else x)

df1["Steuersatz"] = df1["Steuersatz"].apply(german_to_float)
df1["Splittbuchung - Originalbetrag"] = df1["Splittbuchung - Originalbetrag"].apply(german_to_float)
df1["Steuerbetrag"] = df1["Steuerbetrag"].apply(german_to_float)
df1["Splittbuchung - Steuersatz"] = df1["Splittbuchung - Steuersatz"].apply(german_to_float)
df1["Splittbuchung - Steuerbetrag"] = df1["Splittbuchung - Steuerbetrag"].apply(german_to_float)
df1["Primanota"] = df1["Primanota"].astype(str)
# df1["Steuerbetrag"] = df1["Steuerbetrag"].apply(german_to_float)

# Apply the function to all elements in the DataFrame
df1_formatted = df1.apply(lambda col: col.apply(lambda val: format_csv(val, col.name)))
df1_formatted.columns = [f'"{col}"' for col in df1_formatted.columns]

# Export to CSV
df1_formatted.to_csv(output_file, index=False, sep=';', quoting=csv.QUOTE_NONE, escapechar='\\')

print("Done.")
