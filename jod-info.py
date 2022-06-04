import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'}
    url = f'https://in.indeed.com/jobs?q=flutter+developer&l=india&start={page}'

    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('a').text
        company = item.find('span', class_ = 'companyName').text.strip()
        try:
            salary = item.find('div', class_ = 'salary-snippet-container').text.strip()
        except:
            salary =''
        summary = item.find('div', {'class' : 'job-snippet'}).text.strip().replace('\n','')
        
        job = {
            'title' : title,
            'company' : company,
            'salary' : salary,
            'summary' : summary
        }
        
        joblist.append(job)
    return   
        
joblist = []
for i in range(0,40,10):
    print(f'getting page,{i}')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')