from flask import Blueprint, render_template, url_for, request, jsonify, redirect, flash, session
from backend.db import db

# untuk membuat blueprint, kita harus mendeklarasikan sebuah variable 
# didalam blueprint ada 2 argument,
authapp = Blueprint('authapp', __name__)

@authapp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return "oke"
    return render_template('login.html')


@authapp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        return "oke"
    return render_template('register.html')
