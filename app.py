from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required