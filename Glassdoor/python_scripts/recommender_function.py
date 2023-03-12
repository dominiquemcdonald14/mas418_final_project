import os
import csv
import pandas as pd
import numpy as np
import string

os.getcwd()
os.chdir("./output")

#Cleanup the Salaries column first: 
text = open("output_.csv", "r", encoding="utf8") 

text = ''.join([i for i in text]) 

text = text.replace("Employer est.:", " ") 
text = text.replace("(Glassdoor est.)", " ")

x = open("output_.csv","w", encoding="utf8") 

x.writelines(text)
x.close()

df = pd.read_csv("output_.csv", encoding= 'unicode_escape')
# remove rows with all NaN values
df.dropna(thresh=1, inplace=True)

df['listing_jobDesc'] = df.listing_jobDesc.str.replace('\r\n', '') #remove newline
df['listing_jobDesc'] = df['listing_jobDesc'].str.replace("", "'") #special character: apostrophe

#job roles
df["Role"] = None 
df["Role"][df["company_offeredRole"].str.contains("Data Scientist", case=False)] = "Data Scientist"  
df["Role"][df["company_offeredRole"].str.contains("Data Analytics", case=False)] = "Data Analyst"
df["Role"][df["company_offeredRole"].str.contains("Applied Scientist", case=False)] = "Machine Learning"
df["Role"][df["company_offeredRole"].str.contains("Data Engineer", case=False)] = "Data Engineer" 
df["Role"][df["company_offeredRole"].str.contains("Software Engineer", case=False)] = "Others" 
df["Role"][df["company_offeredRole"].str.contains("Data Integration", case=False)] = "Others" 
df["Role"][df["company_offeredRole"].str.contains("Machine Learning", case=False)] = "Machine Learning" 
df["Role"][df["company_offeredRole"].str.contains("Systems Engineer", case=False)] = "Others" 
df["Role"][df["company_offeredRole"].str.contains("Business Analytics", case=False)] = "Data Analyst" 
df["Role"][df["company_offeredRole"].str.contains("Statistician", case=False)] = "Data Scientist" 
df["Role"][df["company_offeredRole"].str.contains("Data Science", case=False)] = "Data Scientist" 
df["Role"][df["company_offeredRole"].str.contains("Data Analyst", case=False)] = "Data Analyst" 

#education
df["Bachelor_Degree"] = None
df["Bachelor_Degree"][df["listing_jobDesc"].str.contains("Bachelor's Degree", case=False)] = "Bachelor's Degree"

df["Master_Degree"] = None  
df["Master_Degree"][df["listing_jobDesc"].str.contains("Master's Degree", case=False)] = "Master's Degree" 

df["Ph_D"] = None 
df["Ph_D"][df["listing_jobDesc"].str.contains("Ph.D", case=False)] = "Ph.D" 

#skills
df["R"] = None
df["R"][df["listing_jobDesc"].str.contains("R|\\bR programming\\b", case=False)] = "R" 

df["SQL"] = None  
df["SQL"][df["listing_jobDesc"].str.contains("SQL", case=False)] = "SQL" 

df["Python"] = None 
df["Python"][df["listing_jobDesc"].str.contains("Python", case=False)] = "Python"

#location
df["Location"] = None 
df['company_roleLocation'] = df['company_roleLocation'].astype(str)

def get_state_from_address(address):
    """
    Given a US address string, returns the 2-letter state code if it exists, or None otherwise.
    """
    # Mapping of state names to state abbreviations
    states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    
    
    #First, check if the input is just a state name or 'Remote'
    if address in states.values():
        state_code = [k for k, v in states.items() if v == address][0]
        return state_code
    elif address == 'Remote':
        return 'Remote'
    
    #Otherwise, split address into parts, assume state is the last 2 characters of the string
    parts = address.split(',')
    if len(parts) < 2:
        return None
    
    state_code = parts[-1].strip()[:2].upper()
    if state_code in states:
        return state_code
    
    return None

df['Location'] = df['company_roleLocation'].apply(get_state_from_address)

#Salaries
df['company_salary'] = df['company_salary'].astype(str)
df['company_salary'] = df['company_salary'].fillna('0')

df["min_salary"] = None
df["max_salary"] = None
df["average_salary"] = None

df.loc[df['company_salary'] == '0', ['min_salary', 'max_salary']] = 0
 
df['min_salary'] = df['company_salary'].str.extract(r'\$(\d{2,3})K - \$(\d{2,3})K')[0].fillna(0).astype(int)
df['max_salary'] = df['company_salary'].str.extract(r'\$(\d{2,3})K - \$(\d{2,3})K')[1].fillna(0).astype(int)

df['average_salary'] = df[['min_salary', 'max_salary']].mean(axis=1)
df['average_salary']=(df['average_salary'])*1000

df.to_csv('output_.csv')