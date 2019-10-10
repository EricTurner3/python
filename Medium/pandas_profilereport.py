# Found at: https://towardsdatascience.com/exploring-your-data-with-just-1-line-of-python-4b35ce21a82d
import pandas as pd
import pandas_profiling
import sys

#my modification, pass it a CSV as an argument and this app will auto create a profile report
if len(sys.argv) == 1:
    csv = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv' # load a sample file
    print("No CSV passed to program! Loading sample dataset...")
else:
    csv = sys.argv[1]

print('Generating profile report...')
pd.read_csv(csv).profile_report().to_file('profile_report.html')
print('Done! Exported to ./profile_report.html')

