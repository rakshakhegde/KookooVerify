import time
import xml.etree.ElementTree as ET
import sqlite3
from hacks.kookooverify.helper import *

conn = sqlite3.connect(DATA_DIR + DB_FILE_NAME)
t = time.time()
rows = conn.execute('SELECT phone_no, code, brand FROM {} WHERE created_at >= ? AND ?-created_at >= 150 AND status == 0'.format(TABLE_REQUEST_ID), (t - validity, t))
for phone_no, code, brand in rows:
        print(phone_no, code, brand)
        code = ' '.join(code)
        response = ET.Element('response')
        ET.SubElement(response, 'playtext').text = 'Your {} activation code is {}. I repeat. {}'.format(brand, code, code)
        ET.SubElement(response, 'hangup')
        makeCall(phone_no, ET.tostring(response))
safeClose(conn)
