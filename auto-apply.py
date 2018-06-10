import requests
import json_extract
from bs4 import BeautifulSoup

# Create session
s = requests.session()

# Extract data from JSON files
site = json_extract.extract('site.json')[0]
urls = site.urls
widgets = site.widgets
ext = site.app_window_ext
login_data = json_extract.extract('login_data.json')[0]
keywords = json_extract.extract('keywords.json')[0]
resume_config = json_extract.extract('resume-config.json')[0]

# Log-in to website
s.post(urls.get('sign-in'), login_data)

# Scrape data from home page
# home_data = s.get(site.get('home'))

# Filter jobs by keywords
job_list_data = s.post(urls.get('jobs_list'), keywords)
job_list_soup = BeautifulSoup(job_list_data.text, 'html.parser')

# Fetch the titles of all jobs on the page
jobs_list = job_list_soup.findAll('div', {'class': 'list-item-title'})

for job in jobs_list:
    # Get job posting url and html
    job_link = job.find('a')
    job_url = urls.get('default') + job_link['href'] + ext
    job_data = s.get(job_url)
    job_soup = BeautifulSoup(job_data.text, 'html.parser')
    
    # Set job type
    mode = 'default_options'

    # Selecting documents
    resume_option = job_soup.find('div', {'id': widgets.resume})
    resume_option.get('option')['selected'] = 'selected>' + resume_config.get(mode).get('resume_name')

    cover_option = job_soup.find('div', {'id': widgets.cover_letter})
    resume_option.get('option')['selected'] = 'selected>' + resume_config.get(mode).get('cover_letter')

    transcript_option = job_soup.find('div', {'id': widgets.transcript})
    transcript_option.get('option')['selected'] = 'selected>' + resume_config.get(mode).get('transcript')


# Close session
s.close()
