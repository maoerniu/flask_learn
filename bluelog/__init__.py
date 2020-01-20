#  -*- coding: utf-8 -*-
import os

import click
from flask import Flask, render_template
from bluelog.extentions import bootstrap, db, moment, mail, ckeditor
from bluelog.models import Admin, Category

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name == None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging(app)           # 注册日志处理器
    register_extentions(app)        # 扩展初始化
    register_blueprints(app)        # 注册蓝本
    register_shell_context(app)     # 注册shell上下文处理函数
    register_template_context(app)  # 注册模版上下文处理函数
    register_errors(app)            # 注册错误处理函数
    register_cmomands(app)          # 注册自定义shell命令
    return app


def register_logging(app):
    pass


def register_extentions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, uri_prefix='/admin')
    app.register_blueprint(auth_bp, uri_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400


def register_cmomands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generages the fake categories, posts and comments"""
        from bluelog.fakes import fake_admin, fake_categories, fake_comments, fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories()

        click.echo('Generating %d posts' % post)
        fake_posts()

        click.echo('Generating %d comments' % comment)
        fake_comments()

        click.echo('Done')


# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db)
#
#
# @app.errorhandler(400)
# def bad_request(e):
#     return render_template('errors/400.html'), 400
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('errors/404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('errors/500.html'), 500
#
#
# @app.cli.command()
# @click.option('--drop', is_flag=True, help='Create after drop.')
# def initdb(drop):
#     """Initialize the database."""
#     if drop:
#         click.confirm('This operation will delete the database, do you want to continue?', abort=True)
#         db.drop_all()
#         click.echo('Drop tables.')
#     db.create_all()
#     click.echo('Initialized database.')
