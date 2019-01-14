
Signup

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

Requirements:

● Token authentication (JWT is prefered)

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

Response:
```{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5ld2FkbWluIiwidXNlcl9pZCI6MjcsImV4cCI6MTU0Njc5MzIzMiwiZW1haWwiOiJrYWx1emh5bm92YUBnbWFpbC5jb20ifQ.BBhR-CsTi63yO9mKKPidFlOfh-RA90FXM_WxiFk44XQ"}```

For User and Post objects, candidate is free to define attributes as they see fit.

Example Post Request create post. 

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

GET request

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


Like.
Request example (method POST)
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
Request example (method GET)
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


Automated bot

```http://127.0.0.1:8000/bot/```

Bot read the configuration and create this activity:
● signup users (number provided in config)
● each user creates random number of posts with any content (up to max_posts_per_user)
After creating the signup and posting activity, posts should be liked using following rules:
● next user to perform a like is the user who has most posts and has not reached max likes
● user performs “like” activity until he reaches max likes
● user can only like random posts from users who have at least one post with 0 likes
● if there is no posts with 0 likes, bot stops
● users cannot like their own posts
● posts can be liked multiple times, but one user can like a certain post only once

we have now
```NUMBER_OF_USERS = 3
MAX_POSTS_PER_USER = 5
MAX_LIKES_PER_USER = 4
```