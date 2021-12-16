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