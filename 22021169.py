#Importing the Libraries I am going to be used for this project
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec

def read_climate_change(filename):
    # Read the World Bank data into a dataframe
    df_wrld_bank = pd.read_csv('worldbankdata.csv', skiprows=4)
    df_years = df_wrld_bank.drop(['Country Code', 'Indicator Code'], axis=1)
    return df_years
df_years = read_climate_change('worldbankdata.csv')
df_years

"""
For further analysis to be carried out on the world bank data on climate change
we will be selcting some few indicators and select G7 countries

"""
indicators = df_years[df_years['Indicator Name'].isin(["Urban population", \
                                                       "Electricity production from coal sources (% of total)",\
                                                           "Total greenhouse gas emissions (kt of CO2 equivalent)", "CO2 emissions (kt)"])]
countries = ['United States', 'Germany', 'Italy', 'United Kingdom', 'France', 'Canada', 'Japan']
selected_countries = indicators[indicators['Country Name'].isin(countries)]
selected_countries = selected_countries.dropna(axis=1)
selected_countries = selected_countries.reset_index(drop=True)
print(selected_countries)

#Creating a dataFrame for Total greenhouse gas emissions for further analysis and plotting.
Tot_green  = selected_countries[selected_countries["Indicator Name"] == \
                                        "Total greenhouse gas emissions (kt of CO2 equivalent)"]

Tot_green = Tot_green.set_index('Country Name', drop=True)
Tot_green = Tot_green .transpose().drop('Indicator Name')
Tot_green[countries] = Tot_green[countries].apply(pd.to_numeric, errors='coerce', axis=1)
print(Tot_green)

# create a new column with the decade for each year
Tot_green['Decade'] = Tot_green.index.map(lambda x: str(x)[:3] + '0s')

# group by decade and sum the CO2 emissions for each country
Tot_green = Tot_green.groupby('Decade').sum()


#Creating a dataFrame for Electricity production from coal sources emissions for further analysis and plotting.
Elect_prod_coal = selected_countries[selected_countries["Indicator Name"] == \
                                        "Electricity production from coal sources (% of total)"]

Elect_prod_coal = Elect_prod_coal.set_index('Country Name', drop=True)
Elect_prod_coal =Elect_prod_coal.transpose().drop('Indicator Name')

Elect_prod_coal[countries] = Elect_prod_coal[countries].apply(pd.to_numeric, errors='coerce', axis=1)
Elect_prod_coal = Elect_prod_coal.rename(columns={'Country Name': 'Years'})
data_2015 = Elect_prod_coal.loc['2015', countries]


"""
For further analysis to be carried out on the world bank data on climate change
we will be Total greenhouse gas emissions indicator and regions

"""
indicators = df_years[df_years['Indicator Name'].isin(["Total greenhouse gas emissions (kt of CO2 equivalent)"])]


regions = ['Europe & Central Asia', 'Middle East & North Africa', 'North America', 'South Asia', 'Latin America & Caribbean']
selected_regions = indicators[indicators['Country Name'].isin(regions)]
selected_regions = selected_regions.dropna(axis=1)
selected_regions = selected_regions.rename(columns={'Country Name': 'Years'})
selected_regions = selected_regions.reset_index(drop=True).T.drop('Indicator Name')

#Set the first row as the new header and remove the original 'Years' row
selected_regions.columns = selected_regions.iloc[0]
selected_regions = selected_regions.drop(selected_regions.index[0])
selected_regions.index = pd.to_datetime(selected_regions.index)

print(selected_regions)

"""
For further analysis to be carried out on the world bank data on climate change
we will be Urban population indicator and regions

"""
Urban_indicators = df_years[df_years['Indicator Name'].isin(["Urban population (% of total population)"])]


Urban_regions = ['Europe & Central Asia', 'Middle East & North Africa', 'North America', 'Sub-Saharan Africa', 'Latin America & Caribbean']
Urban_selected = Urban_indicators[Urban_indicators['Country Name'].isin(Urban_regions)]
Urban_selected = Urban_selected.rename(columns={'Country Name': 'Years'})
Urban_selected = Urban_selected.reset_index(drop=True).T.drop('Indicator Name')


#Set the first row as the new header and remove the original 'Years' row
Urban_selected.columns = Urban_selected.iloc[0]
Urban_selected = Urban_selected.drop(Urban_selected.index[0])

Urban_selected
aggregated_regions = Urban_selected.sum(axis=0)

# Create the dashboard-infographics visualization
fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor('mistyrose')  # Set the figure background color

# Define the grid layout
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.7, hspace=1)


# Creating a dashboard

# Define the explode values
explode = [0.1] * len(aggregated_regions)

# Plot 1: Trend of Region Total greenhouse gas emissions 1990-2020
ax1 = fig.add_subplot(gs[0, 0])
for column in selected_regions.columns:
    ax1.plot(selected_regions.index, selected_regions[column], label=column, linestyle='dashed')
ax1.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
ax1.set_title('Trend of Region Total Greenhouse Gas Emissions 1990-2020')
ax1.set_xlabel('Year')
ax1.set_ylabel('Emissions (kt)')


# Plot 2: Total greenhouse gas emissions by World Power (G7)
ax2 = fig.add_subplot(gs[0, 1])
Tot_green.plot(kind='bar', stacked=False, ax=ax2)
ax2.set_title('Total Greenhouse Gas Emissions by World Power (G7)')
ax2.set_ylabel('Emissions (kt)')
ax2.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))


# Plot 3: Electricity production from coal sources by G7 countries (2015)
ax3 = fig.add_subplot(gs[1, 0])
ax3.barh(data_2015.index, data_2015.values)
ax3.set_title('Electricity Production from Coal Sources by G7 Countries (2015)')
ax3.set_xlabel('Electricity Production from Coal Sources (% of total)')
ax3.set_ylabel('Country')


# Plot 4: Region Urban Population Growth (%)
ax4 = fig.add_subplot(gs[1, 1])
# Define the explode values

ax4.pie(aggregated_regions, labels=aggregated_regions.index, autopct='%1.1f%%', startangle=90, explode=explode)
ax4.set_title('Region Urban Population Growth (%)')


# Overall Title and Explanation
fig.suptitle('Global Impact on Climate Change', fontsize=20)

# Add author's name and student ID below the subtitle
author_info = "Presented by\nOnyedikachi Onwuachuke Student ID: 22021169"
fig.text(0.5, 0.91, author_info, ha='center', va='bottom', fontsize=12)

#Add a textbox with an explanation of your overall visualisation and individual plots
report_summary = """

An Explanation Of The Overall Visualisation And Individual Plots
This climate change dashboard, based on World Bank data, includes four plots:
Regional greenhouse gas emissions trends (1990-2020) for comparison and identification of high-emission areas.
G7 countries' greenhouse gas emissions, highlighting their contributions and allowing comparison.
G7 countries' electricity production from coal sources in 2015, emphasizing reliance on coal and potential for reduction.
Urban population growth distribution across regions, illustrating urbanization's impact on climate change.
This visualization offers a comprehensive perspective on climate change-related aspects and underscores the need for action to mitigate the adverse effects of climate change.
"""

# Add a text box at the bottom of the plots
fig.text(0.5, 0.1, report_summary, ha='center', fontsize=14, va='top', bbox=dict(facecolor='none', edgecolor='none', alpha=0.5))


# Adjust spacing between subplots
fig.tight_layout(pad=3)

#saving the infographics project in .png format
plt.savefig('22021169.png', dpi=300)

# Display the dashboard-infographics visualization
plt.show()