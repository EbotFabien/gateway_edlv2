import requests

token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4MzI0MjM2LCJpYXQiOjE2OTc0NjAyMzYsImp0aSI6ImI2ZTg5OGE5NzYwNzQxNjFhMzJiOGJlY2NiMzMxMTQ1IiwidXNlcl9pZCI6MjYwfQ.Zd2IHuhfuuU5btQd-zDEK0fR2pOXDSswADQ2bk9W064"
headers={"Authorization":"Bearer "+token}

URL2="http://195.15.218.172/rdv_app/rdv/"+str(29030)
r2 = requests.put(URL2,headers=headers,json={'edl': "1"})
print(r2)