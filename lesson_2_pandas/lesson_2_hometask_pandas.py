# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)

def answer_one():
    energy = pd.read_excel("./Energy Indicators.xls", skiprows=18, skipfooter=38, header=None)
    energy = energy.drop(energy.columns[[0, 1]], axis=1)
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy = energy.replace("...", np.nan)
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    energy['Country'] = energy['Country'].str.replace(r'\d+', '', regex=True)
    energy['Country'] = energy['Country'].str.replace(r'\(.*\)', '' ,regex=True).str.strip()
    energy['Country'] = energy['Country'].replace({
        'Republic of Korea': 'South Korea', 
        'United States of America': 'United States',
        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
        'China, Hong Kong Special Administrative Region': 'Hong Kong'
    })

    GDP = pd.read_csv("./world_bank.csv",skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace({
        'Korea, Rep.': 'South Korea',
        'Iran, Islamic Rep.': 'Iran',
        'Hong Kong SAR, China': 'Hong Kong'
    })

    ScimEn = pd.read_excel("./ScimEn.xlsx")
    ScimEn = ScimEn[ScimEn['Rank'] <= 15]
    
    together = pd.merge(ScimEn, energy, how='inner', on='Country')
    together = pd.merge(together, GDP, how='inner', left_on='Country', right_on='Country Name')
    together = together.set_index('Country')

    together = together[['Rank', 'Documents', 'Citable documents', 'Citations', 
                     'Self-citations', 'Citations per document', 'H index',
                     'Energy Supply', 'Energy Supply per Capita', '% Renewable',
                     '2006', '2007', '2008', '2009', '2010', '2011', '2012', 
                     '2013', '2014', '2015']]
    return together


answer_one()

# %%
def answer_two():
    top15 = answer_one()
    avgGDP = top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1)
    avgGDP = avgGDP.sort_values(ascending=False)
    return avgGDP

answer_two()


# %%
def answer_three():
    top15 = answer_one()
    avgGDP = top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1)
    avgGDP = avgGDP.sort_values(ascending=False)
    sixth_ct = avgGDP.index[5]
    sixth_row = top15.loc[sixth_ct]
    diff = sixth_row['2015']/sixth_row['2006']
    return float(diff)

answer_three()

# %%

def answer_four():
    top15 = answer_one()
    top15['Self to Citation Ratio'] = top15['Self-citations'] / top15['Citations']
    max_country = top15['Self to Citation Ratio'].idxmax()
    max_value = float(top15['Self to Citation Ratio'].max())
    return(max_country, max_value)

answer_four()

# %%

def answer_five():
    top15 = answer_one()
    top15['Population'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    top15 = top15.sort_values('Population', ascending=False)
    country_name = top15.index[2]
    return country_name
answer_five()

# %%

def answer_six():
    top15 = answer_one()
    top15['Population'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    top15['Citable docs per Capita'] = top15['Citable documents'] / top15['Population']
    corr = top15['Citable docs per Capita'].corr(top15['Energy Supply per Capita'])
    return float(corr)
answer_six()

# %%

def answer_seven():
    top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    top15['Population'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    result = top15['Population'].groupby(ContinentDict).agg(['size', 'sum', 'mean', 'std'])
    result.index.name = 'Continent'
    return result

answer_seven()
