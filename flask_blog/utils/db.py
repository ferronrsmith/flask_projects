from flask.globals import g
from werkzeug.security import generate_password_hash
from datetime import datetime
import json

def user_exists(username):
    """ The following function checks if a user exists in the db """
    cur = g.db.execute('select * from users where username = ?',[username])
    return cur.rowcount > 0

def get_user(uid):
    """ The following function retrieves a users from the database """
    cur = g.db.execute('select username from users where id = ?',[uid])
    row = cur.fetchone()
    if row :
        return row[0]

def get_user_pass(username):
    """ Gets a user object from the db """
    cur = g.db.execute('select id, password from users where username = ?',[username])
    return cur.fetchone()

def create_user(username, firstname, lastname, password):
    """ Inserts a user record into the database """
    g.db.execute('insert into users (username, password, firstname, lastname) \
                             values (?, ?, ?, ?)',
        [username, generate_password_hash(password), firstname, lastname])
    # werkzeug security hash is used to secure user password
    g.db.commit()

def get_blog_post(id):
    """  The following methods retrieves a blog with the specified ID from the db   """
    cur = g.db.execute('select title, description_enc, date_created, last_modified, tags, '
                       'id, user_id, description from posts where id = (?)', [id])
    row = cur.fetchone()
    if row :
        return dict(title=row[0], desc=row[1], date_created=row[2],last_modified=row[3],
            tags=json_to_tags(row[4]), id=row[5], uid=row[6], desc_enc=row[7], comments=get_blog_comments(id))

def get_n_posts(limit):
    """ Retrieve blog entries from the database """
    cur = g.db.execute('select title, description_enc, date_created, last_modified,'
                       ' tags, user_id, id from posts order by id desc')
    posts = [dict(title=row[0], desc=row[1], date_created=row[2],
        last_modified=row[3], tags=json_to_tags(row[4]), uid=row[5], id=row[6])\
             for row in cur.fetchmany(size=limit)]
    return posts

def get_comment_count(post_id):
    """ The following method returns the count of comment for a following blog <id>  """
    cur = g.db.execute('select count(*) as count from comments where post_id = (?)', [post_id])
    return cur.fetchone()[0]

def post_search(keyword):
    """ The following method searches the database for matching keywords and returns a list of matching  items"""
    cur = g.db.execute('select title, description_enc, date_created, last_modified,'
                       ' tags, user_id, id from posts  where tags like ? ', [any_tag(keyword)])
    posts = [dict(title=row[0], desc=row[1], date_created=row[2],
        last_modified=row[3], tags=row[4], uid=row[5], id=row[6])\
             for row in cur.fetchall()]
    return posts

def post_action(title, desc, desc_enc, tags, uid, action):
    if action == 'insert':
        g.db.execute('insert into posts (title, description, description_enc, '
                     'date_created, tags, user_id) values (?, ?, ?, ?, ?, ?)',
            [title,desc,desc_enc,datetime.now(),tags_to_json(tags),uid])
    elif action == 'update':
        g.db.execute('update posts set title=?, description=?, description_enc=?,\
                  tags=?, last_modified=? where user_id=?',
            [title, desc, desc_enc, tags_to_json(tags),datetime.now(), uid])
    g.db.commit()

def delete_post(id):
    """ delete a blog post"""
    g.db.execute('delete from comments where post_id = ?', [id])
    g.db.execute('delete from posts where id = ?', [id])
    g.db.commit()

def create_blog_comment(text,post_id,user_id):
   """ The following method creates a blog post comment """
   g.db.execute('insert into comments (comments,date_created,user_id,post_id)'
                ' values (?,?,?,?)', [text,datetime.now(),user_id,post_id])
   g.db.commit()

def get_blog_comments(post_id):
    """ The following method retrieve comments for a blog  """
    cur = g.db.execute('select * from comments where post_id = (?)', [post_id])
    comments = [dict(text=row[1],date=row[2],uid=row[3],post_id=row[4]) for row in cur.fetchall()]
    return comments

def any_tag(keyword):
    """ Adds the % to both sides of keyword search """
    return "%{0}%".format(keyword)

def tags_to_json(val):
    """  Coverts tags to json string """
    return json.dumps(dict(tags=val.split(',')))

def json_to_tags(val):
    """ converts jsonified tags to string object  """
    ','.join(json.loads(val)['tags'])
