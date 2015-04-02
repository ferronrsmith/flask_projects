import urllib2
from werkzeug.security import generate_password_hash
from flask.globals import g
from flask import jsonify
import string
from random import choice
from urllib2 import URLError

def create_user(username, firstname, lastname, password):
  """ Inserts a user record into the database """
  g.db.execute('insert into register (username, fname, lname, pwd) \
      values (?, ?, ?, ?)',
      [username.lower(), firstname, lastname, generate_password_hash(password)])
  # werkzeug security hash is used to secure user password
  g.db.commit()
    
def get_user_pass(username):
  """ Gets a user object from the db """
  cur = g.db.execute('select rid, pwd from register where username = ?',[username.lower()])
  return cur.fetchone()
    
def user_exists(username):
  """ The following function checks if a user exists in the db """
  cur = g.db.execute('select * from register where username = ?',[username.lower()])
  row = cur.fetchone()
  return cur.rowcount > 0

def get_user(uid):
  """ The following function retrieves a user from the db """
  cur = g.db.execute('select username from register where rid = ?',[uid])
  row = cur.fetchone()
  if row :
      return row[0]
        
def url_exist(longurl,rid):
  """ The following function checks if a url exists in the db """
  if longurl is None:
      return None
  else :
    cur = g.db.execute('select shorturl from url where longurl = ? and rid = ?', [longurl, rid])
    row = cur.fetchone()
    if row:
      return row[0]
    else:
      return None

def get_user_urls(uid):
  """ The following function retrieves a user from the db """
  cur = g.db.execute('select longurl, shorturl from url where rid = ? order by id desc',[uid])
  entries = [dict(longurl_short=txtlimiter(row[0]), longurl=row[0], shorturl=row[1]) for row in cur.fetchall()]
  return entries

def txtlimiter(longurl, limit=50):
  """ The following function limits a url to a specific length 
       extremely long urls may be a css nightmare, this method can be used to fix this issue by limiting url length to size:limit
       longurl := url to be limited
       limit   := max length of longurl value
  """
  if longurl is None:
    return longurl
  elif len(longurl) > limit:
    return longurl[0:limit-3] + str('...')
  else:
    return longurl
 
def get_url(longurl, path):
  status_code = 404
  status_txt = 'PAGE_NOT_FOUND'
  url = ''
  url_hash = ''
  long_url = ''
  protocol = ''
  exists = False
  
  dburl = url_exist(format_url(longurl),g.uid)
  status_code = check_url(format_url(longurl), dburl is not None)
  if status_code == 400: # check if a long url was entered
      status_txt = "BAD_REQUEST"
  elif status_code == 404: # check if page was found
      longurl = longurl
  elif dburl is None: # check if url is not in db, if not create it and return json string
    cur = g.db.execute('insert into url (rid, longurl, shorturl)\
    values (?,?,?)', [g.uid, format_url(longurl), hash_link()])
    g.db.commit()
    dburl = url_exist(format_url(longurl), g.uid)
    status_txt = 'OK'
    url = 'http://'+ path + '/' + xstr(dburl)
    url_hash = dburl
    long_url = longurl
    protocol = get_protocol(long_url)
  else: #url is in db
    status_txt = 'OK'
    url = 'http://' + path + '/' + xstr(dburl)
    url_hash = dburl
    long_url = longurl
    protocol = get_protocol(long_url)
    exists = True
  return jsonify(status_code = status_code, data = {'url':url,'hash':url_hash, \
    'long_url':longurl, 'exists':exists}, status_txt = status_txt, proto=protocol)
  

def jsonurl(path,shorturl):
    """ Search db if short url exist """

    status_code = 404
    status_txt = 'ENTRY_NOT_FOUND'
    url = ''
    url_hash = ''
    long_url = ''
    protocol = ''
    cur = g.db.execute('select longurl from url where shorturl = ?', [shorturl])
    row =  cur.fetchone()
    if row :
        status_code = 200
        status_txt = 'OK'
        url = 'http://' + path + '/' + shorturl
        url_hash = shorturl
        long_url = row[0]
        protocol = get_protocol(row[0])

    return jsonify(status_code = status_code, data = {'url':url,'hash':url_hash, \
          'long_url':long_url}, status_txt = status_txt)

def searchurl(shorturl):
    """ Search db if short url exist """
    cur = g.db.execute('select longurl from url where shorturl = ?', [shorturl])
    row =  cur.fetchone()
    if row :
        return row[0]
    else :
        return None

# validate url
def check_url(url, indb=False, nonet=True):
  """ The following function verifies that a url is valid and working 
      url   := url to be verfied
      indb  := boolean short circuit value that is set to true if the url already exists in the db (status_code : 200)
               reduces blocking IO and don't bother to check url
      nonet := this value returns an immediate 200. Used in cases where there is no net to test if a URL is valid
  """
  # please note this might return a 404 for https request due to authentication reasons
  try :
    if nonet:
      return 200
    elif indb:
      return 200 # extra param to prevent from re-validating the url & reduce the effect of blocking IO
    elif url is None:
      return 400 # no url supplied (automatic 400)
    else :
      u = urllib2.urlopen(url)
      u.read()
      return u.getcode()
  except URLError, e:
     return e.code

def hash_link(length=8, chars=string.letters + string.digits):
  """ Generates a random hash link 
      length := length of hash to generate
      chars  := character range to be used when generating hash
  """
  return ''.join([choice(chars) for i in range(length)])

def format_url(url):
  """ Formats a url url. if http/https is not present it is appended to the url"""
  http = url.find('http://')
  https = url.find('https://')
  if http >= 0 or https >= 0:
      return url
  else :
      return 'http://' + url

def get_protocol(url):
    """ Retrieves the protocol type from a supplied url """
    https = url.find('https://')
    if https >= 0 :
        return 'https://'
    return 'http://'
        
def xstr(s):
  """ the following function format None i.e null object to an empty string """
  return '' if s is None else str(s)

def join_args(url,args):
    """ Join url arguments together e.g. ?s=BJS?m=2008-05
        output : http://finance.yahoo.com/q/op?s=BJS?m=2008-05
        url := original url
        ls := list of url arguments
    """
    count = 0
    output = ''
    for k, v in args:
        if k != 'longurl':
            if count < 1:
                output += '?' + k[0] + '=' + v[0]
                count+=1
            else :
                output += '&' + k[0] + '=' + v[0]
                count+=1
        else :
            count += 1
    return url + output