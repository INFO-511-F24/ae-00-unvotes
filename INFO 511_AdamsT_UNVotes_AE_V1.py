# This will load the appropriate modules #

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# This will load the data from the dataset UNVotes #

import pandas as pd

# Load data from the GitHub repository. I used ChatGPT to adjust the code to reference the correct URL #

un_votes = pd.read_csv('https://raw.githubusercontent.com/INFO-511-F24/ae-00-unvotes/main/data/un_votes.csv')
un_roll_calls = pd.read_csv('https://raw.githubusercontent.com/INFO-511-F24/ae-00-unvotes/main/data/un_roll_calls.csv')
un_roll_call_issues = pd.read_csv('https://raw.githubusercontent.com/INFO-511-F24/ae-00-unvotes/main/data/un_roll_call_issues.csv')

# Merge the datasets on 'rcid'
unvotes = un_votes.merge(un_roll_calls, on='rcid').merge(un_roll_call_issues, on='rcid')

# This next block of python code will create a data visualization of voting records for UK and Turkey #

# Filter the data for the selected countries and prepare for plotting
filtered_unvotes = unvotes[unvotes['country'].isin(['United Kingdom', 'United States', 'Turkey'])]
filtered_unvotes['year'] = pd.to_datetime(filtered_unvotes['date']).dt.year

# Calculate the percentage of 'yes' votes per year, per country, per issue
percent_yes = filtered_unvotes.groupby(['country', 'year', 'issue'])['vote'].apply(lambda x: (x == 'yes').mean()).reset_index()
percent_yes.rename(columns={'vote': 'percent_yes'}, inplace=True)

# Create the faceted plot
g = sns.FacetGrid(percent_yes, col="issue", hue="country", col_wrap=3)
g.map(sns.scatterplot, "year", "percent_yes", alpha=0.4)
g.map(sns.regplot, "year", "percent_yes", lowess=True, scatter=False)

# Adjust the labels and titles 
g.set_axis_labels("Year", "% Yes")
g.set_titles(col_template="{col_name}")
g.add_legend(title="Country")
g.fig.suptitle("Percentage of 'Yes' votes in the UN General Assembly", y=1.02)
plt.subplots_adjust(top=0.9)

plt.show()
