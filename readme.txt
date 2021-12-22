>>>
>>>
>>> from blog import User, Post
>>>
>>> user1 = User(username='nicolas', email='nicolas@gmail.com', password='password')
>>> user2 = User(username='joe', email='joe@gmail.com', password='password')
>>>
>>> db.session.add(user1)
>>> db.session.add(user2)
>>> db.session.commit()
>>>
>>> User.query.all()
[User('nicolas','nicolas@gmail.com', 'default.jpg'), User('joe','joe@gmail.com', 'default.jpg')]
>>>
>>>
>>> user = User.query.filter_by(username='nicolas').first()
>>> user
User('nicolas','nicolas@gmail.com', 'default.jpg')
>>>
>>> user.id
1
>>> post_1 = Post(title='Blog1',content='First blog post content
', user_id=user.id)
>>> post_2 = Post(title='Blog2',content='Second blog post content', user_id=user.id)
>>>
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()
>>>
>>> user.posts
>>> user.posts
[Post('Blog1','2021-12-15 03:23:09.183752'), Post('Blog2','2021-12-15 03:23:09.215440')]
>>>
>>> post = Post.query.first()
>>>
>>> post
Post('Blog1','2021-12-15 03:23:09.183752')
>>>
>>> post.author
User('nicolas','nicolas@gmail.com', 'default.jpg')
>>>

# --------------------- bcrypt 
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> bcrypt.generate_password_hash('testing')
b'$2b$12$i03CJiNvhSkEeCadShuXVeZdXs.cND5lBK3njU9zJy0unkhH9Mj66'
>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$7GkcJxanFl799rDFm1kMguJUiVg8jhnOv1x5o6lkTjUfFEP29/Qga'
>>> password = bcrypt.generate_password_hash('testing').decode('utf-8')
>>> bcrypt.check_password_hash(password, 'testing')
True
>>>


==================== pagination-------------------

>>> from blog.models import Post
C:\Users\USER\AppData\Local\Programs\Python\Python39\lib\site-packages\flask_sqlalchemy\__init__.py:872: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  warnings.warn(FSADeprecationWarning(
>>>
>>> Post.query.all()
[Post('GOING ABOVE AND BEYOND TO SERVE ','2021-12-16 03:48:18.674232'), Post('Human resources office','2021-12-22 01:15:18.669420'), Post('Honest And Dependable','2021-12-22 01:16:01.305422'), Post('parallel thinking','2021-12-22 01:17:42.952203'), Post('what people say about the world','2021-12-22 01:18:19.265167')]
>>>
>>> posts = Post.query.paginate()
>>> posts
<flask_sqlalchemy.Pagination object at 0x000001CE966699A0>
>>> dir(posts)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages', 'per_page', 'prev', 'prev_num', 'query', 'total']
>>>
>>>
>>> posts.per_page
20
>>> posts.page
1
>>> for post in posts.items:
...     print(post)
...
Post('GOING ABOVE AND BEYOND TO SERVE ','2021-12-16 03:48:18.674232')
Post('Human resources office','2021-12-22 01:15:18.669420')
Post('Honest And Dependable','2021-12-22 01:16:01.305422')
Post('parallel thinking','2021-12-22 01:17:42.952203')
Post('what people say about the world','2021-12-22 01:18:19.265167')
>>>
>>> posts = Post.query.paginate(per_page=3)
>>> posts.page
1
>>> for post in posts.items:
...     print(post)
...
Post('GOING ABOVE AND BEYOND TO SERVE ','2021-12-16 03:48:18.674232')
Post('Human resources office','2021-12-22 01:15:18.669420')
Post('Honest And Dependable','2021-12-22 01:16:01.305422')
>>>



================== generate expirely token ===============
>>>
>>> from itsdangerous import TimedJSONWebSignatureSerializer as serializer
>>>
>>> s = serializer('secret', 30)
>>> token = s.dumps({'user_id': 1}).decode('utf-8')
>>> token
'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0MDE0NjUxOCwiZXhwIjoxNjQwMTQ2NTQ4fQ.eyJ1c2VyX2lkIjoxfQ.7OlHQeZ8eEuQxvo-o4mXCTW24VPRRq_Kfhi5Z84-LrSUX1IKHKzUiOOl9XTqGD7ygQt1NP4DxjQonxiPftoXBA'
>>> s.loads(token)
{'user_id': 1}
>>> s.loads(token)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\USER\AppData\Local\Programs\Python\Python39\lib\site-packages\itsdangerous\jws.py", line 233, in loads
    raise SignatureExpired(
itsdangerous.exc.SignatureExpired: Signature expired
>>>