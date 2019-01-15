#### Run project
##### Requirements
`$ virtualenv myvenv`

`$ source myvenv/bin/activate`

`$ pip install -r requirements.txt`

##### Database migrate
`$ python manage.py makemigrations`

`$ python manage.py migrate`

##### Database settings

`'NAME': 'django_test',`

`'USER': 'root',`

`'PASSWORD': '12345',`
##### Run server
`$ python manage.py runserver
`

##### Signup

```http://127.0.0.1:8000/api/v1/registration/```
```Content-Type: application-json```

 Body:
```
{
  "username": "username",
  "email": "email@test.ua",
  "password": "yourpassword",
  "password": "yourpassword"
}
```

##### Token authentication (JWT is prefered)

```$ curl -X POST -d "username=newadmin&password=password123" http://localhost:8000/api-token-auth/```

or, using Rest Client

```http://localhost:8000/api-token-auth/```
Headers:

```Content-Type: application-json```

Body:
```
{
  "username": "username",
  "password": "yourpassword"
}
```

Response example:
```{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5ld2FkbWluIiwidXNlcl9pZCI6MjcsImV4cCI6MTU0Njc5MzIzMiwiZW1haWwiOiJrYWx1emh5bm92YUBnbWFpbC5jb20ifQ.BBhR-CsTi63yO9mKKPidFlOfh-RA90FXM_WxiFk44XQ"}```

For User and Post objects, candidate is free to define attributes as they see fit.

##### Example Post Request to create a post. 

POST request:

`http://127.0.0.1:8000/api/v1/posts/`

Headers:

```Content-Type: application-json```

```Authorization: JWT token ```

Body:
```
{
  "title": "Title",
  "text": "This is test text"
}
```
Response example:
```
{
"title": "Title",
"text": "This is test text"
}
```

##### GET request to view posts

`http://127.0.0.1:8000/api/v1/posts/`

Headers:

```Content-Type: application-json```

Response example:
```
{
"title": "Title",
"author": 22,
"text": "This is test text"
},
{
"title": "Title2",
"author": 15,
"text": "This is test text 2"
},

```


#### Like.
##### Request example (method POST)
```
http://127.0.0.1:8000/api/v1/posts/like/
```
Headers:

```Content-Type: application-json```

```Authorization: JWT token ```
Body:
```
{
  "post": 3,
  "like": 0
}
```
Response:
```
{
"post": 3,
"like": false
}
```
##### Request example (method GET)
```
http://127.0.0.1:8000/api/v1/posts/like/
```
Response:
```  
{
"user": 27,
"post": 1,
"like": true
},
  {
"user": 27,
"post": 1,
"like": true
},
  {
"user": 27,
"post": 3,
"like": false
}
```

##### Request example (method GET) post detail
```
http://127.0.0.1:8000/api/v1/posts/581
```
Response:
```  

{
    "title": "It is great",
    "text": "Hello ladies and gentlemen!\nThank you so much ..."
}
```


##### Automated bot

```http://127.0.0.1:8000/bot/```

we have now
```
NUMBER_OF_USERS = 3
MAX_POSTS_PER_USER = 5
MAX_LIKES_PER_USER = 4
```