from bluelog.extentions import db
from datetime import datetime


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(50))
    blog_sub_title = db.Column(db.String(150))
    about = db.Column(db.Text)
    name = db.Column(db.String(30))
    email = db.Column(db.String(254))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)        # 分类名称不允许重复
    posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    comments = db.relationship('Comment', back_populates='post', cascade='all,delete-orphan')  # 及联删除


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))        # 站点地址
    body = db.Column(db.Text)               # 正文
    from_admin = db.Column(db.Boolean, default=False)   # 是否来自管理员的评论
    reviewed = db.Column(db.Boolean, default=False)     # 是否通过审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    # 每条评论可以有多个评论，评论和回复之间是一对多的关系，与自身创建连接
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 主评论
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])    # 把id字段设置为远程侧 P236
    # 主评论的多回复
    replies = db.relationship('Comment', back_populates='replied', cascade='all')       # 主评论删掉后，这条评论的回复都删掉
