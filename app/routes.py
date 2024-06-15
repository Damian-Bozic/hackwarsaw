from flask import Blueprint, request, jsonify
from . import db
from .models import User, Request, Tag

main = Blueprint('main', __name__)

# CRUD for User
@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        surname=data['surname'],
        phone=data['phone'],
        pesel=data['pesel'],
        email=data['email'],
        street=data['street'],
        postal_code=data['postal_code'],
        city=data['city']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

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

# CRUD for Request
@main.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    user = User.query.get(data['creator_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    new_request = Request(
        name=data['name'],
        description=data['description'],
        image=data.get('image'),
        creator=user
    )
    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            new_request.tags.append(tag)
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

# CRUD for Tag
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

# Voting for a request
@main.route('/requests/<int:request_id>/vote', methods=['POST'])
def vote_request(request_id):
    data = request.get_json()
    user = User.query.get(data['user_id'])
    req = Request.query.get(request_id)
    if not user or not req:
        return jsonify({'message': 'User or Request not found'}), 404
    if user in req.voters:
        return jsonify({'message': 'User has already voted'}), 400
    req.voters.append(user)
    db.session.commit()
    return jsonify({'message': 'Vote added'})
