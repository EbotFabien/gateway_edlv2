import requests

def checkRole(token):

    try:
        user = requests.get("http://195.15.218.172/security/manager_app/viewset/role/?token="+token,headers={"Authorization":"Bearer "+token}).json()[0]
    except KeyError:
        return -1
    return user

token='eyJ0eXAiOiJKV1QiLCJhbGciOhJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4MzI0MjM2LCJpYXQiOjE2OTc0NjAyMzYsImp0aSI6ImI2ZTg5OGE5NzYwNzQxNjFhMzJiOGJlY2NiMzMxMTQ1IiwidXNlcl9pZCI6MjYwfQ.Zd2IHuhfuuU5btQd-zDEK0fR2pOXDSswADQ2bk9W064'

five=checkRole(token)
print(five)
