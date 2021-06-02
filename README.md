# Google Cloud Platform YouTube API

## Project Goal

Upload newly created videos to your db periodically using GCP youtube api V3 and django cron job

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

Performance results for 50000 db entries:
1. Silk (for single request)

![Screenshot from 2021-05-25 12-02-16](https://user-images.githubusercontent.com/43541680/119450228-3985c200-bd51-11eb-80e2-452907f02ab6.png)

2. Loadtest (for bulk requests):

![Screenshot from 2021-05-25 12-01-57](https://user-images.githubusercontent.com/43541680/119450232-3b4f8580-bd51-11eb-93cf-11e683626083.png)

![Screenshot from 2021-05-25 12-01-33](https://user-images.githubusercontent.com/43541680/119450242-3c80b280-bd51-11eb-82f8-bc2b53deec39.png)
