from flask import *
import sqlite3
import random
import time
from hacks.kookooverify.helper import *
from hacks.kookooverify.config import *

app = Blueprint('kookooverify', __name__, template_folder='templates')

'''
DB Message status
0 = Unverified
1 = Verified
2 = Cancelled through API
3 = Cancelled due to too many attempts
'''
@app.route('/test')
def test():
        return jsonify(status=0, lol=[{'dshj':'87hd','jdhzxj':['dsv','vxz']}])

@app.route('/')
def verify():
        params = request.args
        try:
                phone_no = params['phone_no'][-10:] # only last 10 digits
                brand = params['brand']
        except:
                return jsonify({'status': 2, 'error_text': 'phone_no and brand parameters required!'})
        conn = sqlite3.connect(DATA_DIR + DB_FILE_NAME)
        conn.execute('CREATE TABLE IF NOT EXISTS {} (created_at REAL, phone_no TEXT, code TEXT, request_id TEXT, status INTEGER, brand TEXT)'.format(TABLE_REQUEST_ID))
        conn.execute('CREATE TABLE IF NOT EXISTS {} (created_at REAL, code TEXT, request_id TEXT)'.format(TABLE_CHECKS))
        validFrom = time.time() - validity
        row = conn.execute('SELECT request_id FROM {} WHERE created_at >= ? AND phone_no == ? AND status == 0'.format(TABLE_REQUEST_ID), (validFrom, phone_no)).fetchone()
        if row:
                request_id = row[0]
                safeClose(conn)
                return jsonify({'request_id': request_id, 'status': 10,
                                                'error_text': 'Concurrent verifications to the same number are not allowed'})
        request_id = createUid()
        code = createCode()
        print(request_id, code)
        conn.execute('INSERT INTO {} VALUES (?,?,?,?,?,?)'.format(TABLE_REQUEST_ID), (time.time(), phone_no, code, request_id, 0, brand))
        safeClose(conn)
        kookooResponse = sendSms(phone_no, codeMessage(brand, code), kookoo_api_key)
        return jsonify({'status': 0, 'kookoo_response': kookooResponse, 'request_id': request_id})

@app.route('/check')
def check():
        params = request.args
        try:
                request_id = params['request_id']
                code = params['code']
        except:
                return jsonify({'status': 2, 'error_text': 'request_id and code parameters required!'})
        conn = sqlite3.connect(DATA_DIR + DB_FILE_NAME)
        validFrom = time.time() - validity
        tries = conn.execute('SELECT * FROM {} WHERE created_at >= ? AND request_id==?'.format(TABLE_CHECKS), (validFrom, request_id)).fetchall()
        if len(tries) >= 3:
                return jsonify({'status': 15, 'error_text': 'Verify Limit Exceeded'})
        row = conn.execute('SELECT * FROM {} WHERE created_at >= ? AND request_id == ?'.format(TABLE_REQUEST_ID), (validFrom, request_id)).fetchone()
        print('Row:', row)
        if not row:
                return jsonify({'status': 6, 'error_text': 'Request ID does not exist or is expired'})
        if row[4] == 1: # if status == 1
                return jsonify({'status': 18, 'error_text': 'Verified already'}) 
        if row[4] == 2: # if status == 2
                return jsonify({'status': 19, 'error_text': 'Verification cancelled'})
        conn.execute('INSERT INTO {} VALUES (?,?,?)'.format(TABLE_CHECKS), (time.time(), code, request_id))
        if row[2] != code: # if code == received code
                safeClose(conn)
                return jsonify({'status': 16, 'error_text': 'The code provided does not match the expected value'})
        conn.execute('UPDATE {} SET status=1 WHERE request_id == ?'.format(TABLE_REQUEST_ID), (request_id,))
        safeClose(conn)
        return jsonify({'status': 0, 'request_id': request_id, 'message': 'Verified successfully'})

@app.route('/search')
def search():
        params = request.args
        try:
                request_id = params['request_id']
        except:
                return jsonify(status=2, error_text='request_id parameters required!')
        conn = sqlite3.connect(DATA_DIR + DB_FILE_NAME)
        row = conn.execute('SELECT * FROM {} WHERE request_id==?'.format(TABLE_REQUEST_ID), (request_id,)).fetchone()
        if not row:
                return jsonify(status=101, error_text='No response found')
        delta = time.time() - row[0]
        status = 'SUCCESS' if row[4]==1 else 'EXPIRED' if delta>5*60 else 'IN PROGRESS' if row[4]==0 else 'CANCELLED'
        checks = []
        for check in conn.execute('SELECT * FROM {} WHERE request_id==?'.format(TABLE_CHECKS), (request_id,)):
                checks.append(dict(created_at=epochToDate(check[0]),
                                                   code=check[1],
                                                   status='VALID' if check[1]==row[2] else 'INVALID'))
        safeClose(conn)
        return jsonify(brand=row[5],
                                   created_at=epochToDate(row[0]),
                                   checks=checks,
                                   phone_no=row[1],
                                   request_id=row[3],
                                   status=status)

@app.route('/control')
def control():
        params = request.args
        try:
                request_id = params['request_id']
                cmd = params['cmd']
        except:
                return jsonify({'status': 2, 'error_text': 'request_id and cmd parameters required!'})
        conn = sqlite3.connect(DATA_DIR + DB_FILE_NAME)
        if cmd == 'cancel':
                conn.execute('UPDATE {} SET status=2 WHERE request_id == ?'.format(TABLE_REQUEST_ID), (request_id,))
                safeClose(conn)
                return jsonify(status=0, response='CANCELLED')
        return jsonify(status=1, response='INVALID COMMAND')

def createCode():
        return random.randint(1000, 9999)

def createUid(): # good enough for purposes of the Kookoo demo
        uid = str(time.time()) + str(random.random())
        uid = uid.replace('.', '')
        return uid

def codeMessage(brand, code):
        return '{} code: {}. Valid for 5 minutes.'.format(brand, code)

def epochToDate(secs):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(secs))
