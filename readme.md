This project was performed as a test task for the position of python developer.


The project used:<br>
* base User model;
* additionally created models for posts and likes

Also in the project were used:<br>

* The [JWT token technique](https://pypi.org/project/djangorestframework-simplejwt/) was used to authenticate users and access the api
* To display statistics on likes using a date range, [django filters](https://pypi.org/project/django-filter/) were used
* To log user activity, the [drf api tracking](https://pypi.org/project/drf-api-tracking/) module was used

For a simple check of the project's functionality, curl was used with typical requests. Examples of requests:

http://127.0.0.1:8000 - loacalhost

* New User Registration<br>
```
curl -d "username=<username>&password=<password>" http://127.0.0.1:8000/api/signup
```
* Obtaining a token for a user registered by an administrator
```
curl -d "username=<username>&password=<password>" http://127.0.0.1:8000/api/token/
```
* Getting a list of posts
```
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/posts
```
* Create new post
```
curl -X POST -d "title=<title>&content=<text>&poster_id=<id>" http://127.0.0.1:8000/api/posts -H "Authorization: Bearer <token>"
```
* Delete post
```
curl -X DELETE http://127.0.0.1:8000/api/posts/<post_id> -H "Authorization: Bearer <token>"
```
* Like the post
```
curl -X POST http://127.0.0.1:8000/api/posts/<post_id>/like -H "Authorization: Bearer <token>"
```
* Unlike the post
```
curl -X DELETE http://127.0.0.1:8000/api/posts/<post_id>/like -H "Authorization: Bearer <token>"
```
* Analytics about how many likes was made. API returns analytics
aggregated by day
```
curl -X GET http://127.0.0.1:8000/api/analytics/?date_from=<YYYY>-<MM>-<DD>&date_to=<YYYY>-<MM>-<DD> -H "Authorization: Bearer <token>"
```
* User activity endpoint that shows when the user was last logged in and when
makes the last request to the service
```
curl -X GET http://127.0.0.1:8000/api/useractivity/<id> -H "Authorization: Bearer <token>"
```

_If suddenly someone does something like this, please do not copy my project thoughtlessly, I could make a mistake :-) Better write, if you suddenly have questions or problems, I will help._