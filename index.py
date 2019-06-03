import os
from conf import *

Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
session = session()

@auth.verify_password
def check_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        response = jsonify({'message': 'Username ya existe!'})
        response.status_code = 400
        return response
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(1800) # sesion de 30 minutos
    return jsonify({'token': token.decode('ascii'), 'duration': 1800})

@app.route('/api/check')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@app.route('/api/get-post/<int:id>')
def get_post(id):
    post = Blog.query.get(id)
    if not post:
        abort(400)
    return jsonify({'title': post.title, 'body': post.body, 'created': post.created, 'updated': post.updated})

@app.route('/api/new-post', methods=['POST'])
@auth.login_required
def new_post():
    user_id = g.user.id
    title = request.json.get('title')
    body = request.json.get('body')
    if title is None or body is None:
        response = jsonify({'message': 'Bad request!'})
        response.status_code = 400
        return response
    post = Blog()
    post.set_user_id(user_id)
    post.set_title(title)
    post.set_body(body)
    db.session.add(post)
    db.session.commit()
    return (jsonify({'id': post.id, 'action': 'created'}), 201,
            {'Location': url_for('get_post', id=post.id, _external=True)})

@app.route('/api/edit-post/<int:id>', methods=['POST'])
@auth.login_required
def edit_post(id):
    user_id = g.user.id
    title = request.json.get('title')
    body = request.json.get('body')
    if title is None or body is None:
        response = jsonify({'message': 'Bad request!'})
        response.status_code = 400
        return response
    post = Blog().query.filter(and_(Blog.id==id, Blog.user_id==user_id)).first()
    if not post:
        response = jsonify({'message': 'Nothing found!'})
        response.status_code = 400
        return response
    post.set_title(title)
    post.set_body(body)
    db.session.add(post)
    db.session.commit()
    return (jsonify({'id': post.id, 'action': 'updated'}), 201,
            {'Location': url_for('get_post', id=post.id, _external=True)})


@app.route('/api/delete-post/<int:id>', methods=['POST'])
@auth.login_required
def delete_post(id):
    user_id = g.user.id
    post = Blog().query.filter(and_(Blog.id==id, Blog.user_id==user_id)).first()
    if not post:
        response = jsonify({'message': 'Nothing found!'})
        response.status_code = 400
        return response
    db.session.delete(post)
    db.session.commit()
    return (jsonify({'id': post.id, 'action': 'deleted'}), 201,
            {'Location': url_for('get_post', id=post.id, _external=True)})

### MISC

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)

print 'Inicializando'

try:

	while True:

		time.sleep(0.1)

finally:

	print "Exit"
	GPIO.cleanup()