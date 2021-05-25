# FAMPAY

## Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.
steps:
1. git clone repo
2. install virtual environment and activate
3. pip install -r requirements.txt
4. add config.ini file in fampay folder (where setting.py belongs)

your config.ini file will look like: 

```
[main]
api_key = GCD project API key
search_key = any search key 
SECRET_KEY = '46&d6uzfd_v1c%zt*=%x*$=g(v%!9(n5cn+^y=bo1mxo*z^6^c'
DEBUG = False

[database]
NAME = db name
HOST = localhost / any db host
USER = user name
PASSWORD = password
```

Reference Link: Please visit http://34.234.94.137/youtube/dashboard (for desigining page) and http://34.234.94.137/youtube/videos/ (for API page)
