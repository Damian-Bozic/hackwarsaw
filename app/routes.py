from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, current_app
from app import db, bcrypt
from app.models import User, BankAccount, ArtType, ArtSubtype
import stripe

bp = Blueprint('routes', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        street_address = request.form['street_address']
        postal_code = request.form['postal_code']
        city = request.form['city']
        youtube_link = request.form['youtube_link']
        instagram_link = request.form['instagram_link']
        art_type_id = request.form['art_type_id']

        user = User(email=email, first_name=first_name, last_name=last_name,
                    street_address=street_address, postal_code=postal_code, city=city,
                    youtube_link=youtube_link, instagram_link=instagram_link, art_type_id=art_type_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@bp.route('/bank_account', methods=['GET', 'POST'])
def bank_account():
    if request.method == 'POST':
        account_holder_name = request.form['account_holder_name']
        account_number = request.form['account_number']
        routing_number = request.form['routing_number']
        user_id = request.form['user_id']

        bank_account = BankAccount(account_holder_name=account_holder_name,
                                   account_number=account_number, routing_number=routing_number, user_id=user_id)
        db.session.add(bank_account)
        db.session.commit()

        flash('Bank account added successfully!', 'success')
        return redirect(url_for('routes.profile', user_id=user_id))

    return render_template('bank_account.html')

@bp.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    data = request.get_json()
    amount = data['amount']

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        payment_method_types=['card'],
    )

    return jsonify({
        'clientSecret': intent['client_secret']
    })
