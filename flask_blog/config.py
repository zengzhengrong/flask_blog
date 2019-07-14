import os
import json

with open('./profile.json','r') as f:
    profile = json.load(f)

class Config:
    SECRET_KEY = profile.get('SECRET_KEY')
    # dev SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:5432@127.0.0.1:5432/flaskdb'
    SQLALCHEMY_DATABASE_URI = 'postgresql://flaskdb:5432@db:5432/flaskdb'
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # SQLALCHEMY_MAX_OVERFLOW = 20
    #配置email
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USE_TLS = True
    MAIL_USERNAME = profile.get('EMAIL_USER')
    MAIL_PASSWORD = profile.get('EMAIL_PASSWORD')