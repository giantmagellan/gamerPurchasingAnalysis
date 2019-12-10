#!/usr/bin/env python
# coding: utf-8

# In[1]:


# HEROES OF PYMOLI script for analysing the game's purchasing data


# In[3]:


# Dependencies and setup
import os 
import csv
import pandas as pd

# File to load
HEROES_PATH = os.path.join('c:/Users/User/Documents/Homework Data/purchase_data.csv')

# Function to read csv data
def load_pymoli_data(heroes_path=HEROES_PATH):
    pymoli_path = os.path.join(heroes_path)
    return pd.read_csv(pymoli_path)

# print data
pymoli_df = load_pymoli_data()
copy_pymoli = pymoli_df # for later use
pymoli_df.head()


# In[4]:


# Prints info about the data set
pymoli_df.info()


# In[5]:


pymoli_df.describe()


# In[6]:


# PLAYER COUNT
# Count the number of players in Heroes of Pymoli
total_players = len(pymoli_df["SN"].unique().tolist())

# Summary dataframe for total players
player_dict = [{'Total Players': total_players}]
player_df = pd.DataFrame(player_dict)
player_df


# In[8]:


# PURCHASING ANALYSIS
# Counts the number of unique values 
unique_items = len(pymoli_df["Item ID"].unique())

# Average purchase price
avg_price = pymoli_df['Price'].mean()

# Total number of purchases
total_purchases = pymoli_df["Price"].count()

# Total Revenue
revenue = pymoli_df["Price"].sum()


# In[9]:


# Summary dataframe for Purchasing Analysis
purchase_dict = [{'Number of Unique': unique_items, 'Average Price':avg_price, 
                  'Total Purchases':total_purchases,'Total Revenue':revenue}]
purchase_df = pd.DataFrame(purchase_dict)
purchase_df


# In[10]:


# GENDER DEMOGRAPHICS
# count of players by gender
# male
male_df = pymoli_df.loc[pymoli_df["Gender"] == "Male", :]
male_count = len(male_df["SN"].unique())
# female
female_df = pymoli_df.loc[pymoli_df["Gender"] == "Female", :]
female_count = len(female_df["SN"].unique())
#other
other_df = pymoli_df.loc[pymoli_df["Gender"] == "Other / Non-Disclosed", :]
other_count = len(other_df["SN"].unique())

# percentage of players by gender
male_perc = male_count / total_players * 100
# male_perc_fin = male_perc.map("{:,.2f}%".format)
female_perc = female_count / total_players * 100
# fem_perc_fin = female_perc.map("{:,.2f}%".format)
other_perc = other_count / total_players * 100
# other_perc_fin = [other_perc.map("{:,.2f}%".format)]


# In[12]:


# Summary dataframe for Gender Demographics
gender_df = pd.DataFrame({
    'Gender': ["Male","Female","Other / Non-Disclosed"],
    'Total Count': [male_count, female_count, other_count],
    'Percentage of Players': [male_perc,female_perc, other_perc],
               })
gender_df.set_index(['Gender','Total Count','Percentage of Players'])


# In[13]:


# GENDER PURCHASING ANALYSIS
# purchase counts by gender
male_count_total = pymoli_df['Gender'].value_counts()['Male']
fem_count_total = pymoli_df['Gender'].value_counts()['Female']
other_count_total = pymoli_df['Gender'].value_counts()['Other / Non-Disclosed']


# In[14]:


# total and average amount spent by gender
# male
male_price_df = pymoli_df.loc[pymoli_df["Gender"] == "Male", :]
male_avg = male_price_df['Price'].mean()
male_sum = male_price_df['Price'].sum()
male_tot_avg = male_sum / male_count

# female
female_price_df = pymoli_df.loc[pymoli_df['Gender'] == "Female", :]
fem_avg = female_price_df['Price'].mean()
fem_sum = female_price_df['Price'].sum()
fem_tot_avg = fem_sum / female_count

# other/non-disclosed
other_price_df = pymoli_df.loc[pymoli_df['Gender'] == "Other / Non-Disclosed", :]
other_avg = other_price_df['Price'].mean()
other_sum = other_price_df['Price'].sum()
other_tot_avg = other_sum / other_count


# In[15]:


# Summary dataframe for Gender Purchasing Analysis
gen_purch = pd.DataFrame({
    'Gender': ["Female", "Male", "Other / Non-Disclosed"],
    'Purchase Count': [fem_count_total, male_count_total, other_count_total],
    'Average Purchase Price': [fem_avg, male_avg, other_avg],
    'Total Purchase Value': [fem_sum, male_sum, other_sum],
    'Avg Total Purchase Per Person': [fem_tot_avg, male_tot_avg, other_tot_avg],
               })
gen_purch.set_index(['Gender', 'Purchase Count', 'Average Purchase Price', 
                     'Total Purchase Value', 'Avg Total Purchase Per Person'])


# In[16]:


# AGE DEMOGRAPHICS
ages = [0, 9, 14, 19, 24, 29, 34, 39, 49]
labels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-40", "40+"]
pymoli_df["Age Group"] = pd.cut(pymoli_df["Age"], ages, labels=labels)
pymoli_df.head()


# In[69]:


# groupby object base on Age Group
ages_group = pymoli_df.drop_duplicates(subset="SN", keep='first') # drops duplicate SN values
age_group = ages_group.groupby("Age Group")
age_count = pd.DataFrame(age_group["Age"].count()) # number of rows in each bin
age_total = age_count["Age"].sum() # total count of ages
perc_play = age_count["Age"] / age_total * 100
perc_age = [perc_play.map("{:,.2f}%".format)]
age_count_final = age_count["Age"]


# In[70]:


# Summary dataframe for Age Demographics
gen_purch = pd.DataFrame({
    'Total Count': age_count_final,
    'Percentage of Players': perc_play.map("{:,.2f}%".format),
               })
gen_purch


# In[71]:


# # Groups copy_pymoli by age and price
# for age, price in copy_pymoli.groupby('Age Group'):
#     print(age)
#     print(price)


# In[77]:


# PURCHASING ANALYSIS BY AGE
new_age_group = pymoli_df.groupby('Age Group')
ages_purchase_count = new_age_group['SN'].count()
ages_purchase_avg = new_age_group['Price'].mean()
ages_purchase_total = new_age_group['Price'].sum()
ages_purchase_per_person = ages_purchase_total / ages_purchase_count

# Summary dataframe for Age Purchasing Analysis
age_analysis = pd.DataFrame({
    'Purchase Count': ages_purchase_count,
    'Avg Purchase Price': ages_purchase_avg.map("${:,.2f}".format),
    'Total Purchase Value': ages_purchase_total.map("${:,.2f}".format),
    'Avg Total Purchase per Person': ages_purchase_per_person.map("${:,.2f}".format),
               })
age_analysis


# In[73]:


# TOP SPENDERS
spend_group = pymoli_df.groupby('SN')
spend_count = spend_group['SN'].count()
spend_avg = spend_group['Price'].mean()
spend_total = spend_group['Price'].sum()

spenders = pd.DataFrame({
    'Purchase Count': spend_count,
    'Average Purchase Price': spend_avg.map("${:,.2f}".format),
    'Total Purchase Value': spend_total.map("${:,.2f}".format),
})
spenders.sort_values(by='Purchase Count',ascending=False).head()


# In[74]:


# MOST PROFITABLE
profit_group = pymoli_df.groupby(['Item ID','Item Name'])
profit_count = profit_group['SN'].count()
profit_avg = profit_group['Price'].mean()
profit_total = profit_group['Price'].sum()

profits = pd.DataFrame({
    'Purchase Count': profit_count,
    'Average Purchase Price': profit_avg.map("${:,.2f}".format),
    'Total Purchase Value': profit_total.map("${:,.2f}".format),
})
profits.sort_values(by='Purchase Count',ascending=False).head()


# In[ ]:




