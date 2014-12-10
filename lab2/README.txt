# get token
https://d.isaev.ru/oauth2/auth?client_id=11&redirect_uri=http://google.ru&response_type=code
curl -kgvv "https://d.isaev.ru/oauth2/token" --data "grant_type=authorization_code&redirect_uri=http://google.ru&client_id=11&client_secret=e3ea25aebad6439ca2883ebf16c010fa&code=58bec70c230b40868f5aa6c7e8342d88"

# refresh token
curl -gkvv "https://d.isaev.ru/oauth2/token" --data "grant_type=refresh_token&redirect_uri=http://google.ru&client_id=11&client_secret=e3ea25aebad6439ca2883ebf16c010fa&refresh_token=931a6b60f7794d7bac1afd65427fc1e8"

# API
curl -kgvv "https://d.isaev.ru/api/images" -H "Authorization: Bearer 4f33e06dbf4048f58f45678eefb274f0" --data '{"name":"some image", "description": "some description", "url": "http://some.url.com", "tags": [23, 24]}'

curl -kgvv "https://d.isaev.ru/api/tags" -H "Authorization: Bearer 4f33e06dbf4048f58f45678eefb274f0" --data '{"name":"some tag", "description": "some description of tag"}'
