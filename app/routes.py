import os
from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Request, Tag

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256')
    new_user = User(
        name=data['name'],
        surname=data['surname'],
        phone=data['phone'],
        pesel=data['pesel'],
        email=data['email'],
        street=data['street'],
        postal_code=data['postal_code'],
        city=data['city'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login failed'}), 401
    login_user(user)
    session['user_id'] = user.id
    return jsonify({'message': 'Login successful', 'user_id': user.id})


@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@main.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.name = data.get('name', user.name)
    user.surname = data.get('surname', user.surname)
    user.phone = data.get('phone', user.phone)
    user.pesel = data.get('pesel', user.pesel)
    user.email = data.get('email', user.email)
    user.street = data.get('street', user.street)
    user.postal_code = data.get('postal_code', user.postal_code)
    user.city = data.get('city', user.city)
    db.session.commit()
    return jsonify({'message': 'User updated'})


@main.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})


@main.route('/requests', methods=['POST'])
@login_required  # Asegúrate de que esta ruta requiera autenticación
def create_request():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    name = request.form.get('name')
    description = request.form.get('description')

    file = request.files.get('image')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        image_url = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    else:
        image_url = None

    new_request = Request(
        name=name,
        description=description,
        image=image_url,
        creator=user
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'message': 'Request created'}), 201


@main.route('/requests', methods=['GET'])
def get_requests():
    requests = Request.query.all()
    return jsonify([request.to_dict() for request in requests])


@main.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    req = Request.query.get_or_404(request_id)
    return jsonify(req.to_dict())


@main.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.get_json()
    req = Request.query.get_or_404(request_id)
    req.name = data.get('name', req.name)
    req.description = data.get('description', req.description)
    req.image = data.get('image', req.image)
    db.session.commit()
    return jsonify({'message': 'Request updated'})


@main.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    req = Request.query.get_or_404(request_id)
    db.session.delete(req)
    db.session.commit()
    return jsonify({'message': 'Request deleted'})


@main.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    new_tag = Tag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({'message': 'Tag created'}), 201


@main.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags])


@main.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.to_dict())


@main.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.get_json()
    tag = Tag.query.get_or_404(tag_id)
    tag.name = data.get('name', tag.name)
    db.session.commit()
    return jsonify({'message': 'Tag updated'})


@main.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted'})


@main.route('/requests/<int:request_id>/vote', methods=['POST'])
@login_required
def vote_request(request_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    request = Request.query.get(request_id)
    if not request:
        return jsonify({'message': 'Request not found'}), 404

    if user in request.voters:
        return jsonify({'message': 'User has already voted for this request'}), 400

    request.voters.append(user)
    db.session.commit()
    return jsonify({'message': 'Vote recorded', 'votes': len(request.voters)}), 200


@main.route('/requests/<int:request_id>/votes', methods=['GET'])
def get_votes(request_id):
    req = Request.query.get_or_404(request_id)
    voters = [user.to_dict() for user in req.voters]
    vote_count = len(voters)
    return jsonify({'voters': voters, 'vote_count': vote_count}), 200


@main.route('/')
def page():
    return render_template('page.html')
