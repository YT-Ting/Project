from flask import Flask, jsonify, Blueprint
from flask_pymongo import PyMongo
from flask_docs import ApiDoc
import re

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://dbuser:admin123@cluster0-zke9w.mongodb.net/591?retryWrites=true&w=majority"'
app.config['JSON_AS_ASCII'] = False
app.config['API_DOC_MEMBER'] = ['api']

ApiDoc(app)
mongodb = PyMongo(app)
api = Blueprint('api', __name__)


@api.route('/all', methods=['GET'])
def get_all():
    """
     全部租屋資訊
     Response Format
     *JSON Example
        {
        "result": [
            {
            "出租者": "林小姐",
            "出租者身份": "代理人",
            "地點": "新北市",
            "型態": "公寓",
            "性別要求": "男女生皆可",
            "現況": "獨立套房",
            "聯絡電話": "0955-590-232"
            },
        }
        """
    framework = mongodb.db.db
    output = []
    for q in framework.find():
        output.append({'地點': q['地點'], '出租者': q['出租者'],
                       '出租者身份': q['出租者身份'], '聯絡電話': q['聯絡電話'],
                       '型態': q['型態'], '現況': q['現況'],
                       '性別要求': q['性別要求']})
    return jsonify({'result': output})


@api.route('/<gender>/<location>', methods=['GET'])
def get_requirement(gender, location):
    """
        @@@
        #### example
            指定租屋條件
            url='http://127.0.0.1:5000/api/<gender>/<location>'
            gender =男生 or 女生 or 男女生皆可
            location = 台北市 or 新北市
        @@@
        """
    framework = mongodb.db.db
    output = []
    for q in framework.find({'性別要求': gender, '地點': location}):
        output.append({'地點': q['地點'], '出租者': q['出租者'],
                       '出租者身份': q['出租者身份'], '聯絡電話': q['聯絡電話'],
                       '型態': q['型態'], '現況': q['現況'],
                       '性別要求': q['性別要求']})
    if not output:
        output = 'No results found'

    return jsonify({'result': output})


@api.route('/<phone>', methods=['GET'])
def get_phone(phone):
    """
            @@@
            #### example
                指定聯絡電話
                url='http://127.0.0.1:5000/api/<phone>
                phone = XXX-XXX-XXX
            @@@
            """
    framework = mongodb.db.db
    output = []
    for q in framework.find({'聯絡電話': phone}):
        output.append({'地點': q['地點'], '出租者': q['出租者'],
                       '出租者身份': q['出租者身份'], '聯絡電話': q['聯絡電話'],
                       '型態': q['型態'], '現況': q['現況'],
                       '性別要求': q['性別要求']})
    if not output:
        output = 'No results found'

    return jsonify({'result': output})


@api.route('/非屋主', methods=['GET'])
def get_not_host():
    """
    非屋主的出租條件
    *JSON Example
        {
        "result": [
            {
            "出租者": "林小姐",
            "出租者身份": "代理人",
            "地點": "新北市",
            "型態": "公寓",
            "性別要求": "男女生皆可",
            "現況": "獨立套房",
            "聯絡電話": "0955-590-232"
            },
        }
    """
    framework = mongodb.db.db
    output = []
    for q in framework.find({'出租者身份': {'$nin': ['屋主']}}):
        output.append({'地點': q['地點'], '出租者': q['出租者'],
                       '出租者身份': q['出租者身份'], '聯絡電話': q['聯絡電話'],
                       '型態': q['型態'], '現況': q['現況'],
                       '性別要求': q['性別要求']})
    if not output:
        output = 'No results found'

    return jsonify({'result': output})


@api.route('/tpe_ms_wu', methods=['GET'])
def get_tpe_ms_wu():
    """
        【臺北】【屋主為女性】【姓氏為吳】的出租條件
        *JSON Example
        {
            "result": [
            {
            "出租者": "吳小姐",
            "出租者身份": "屋主",
            "地點": "台北市",
            "型態": "電梯大樓",
            "性別要求": "NULL",
            "現況": "整層住家",
            "聯絡電話": "0916-861-540"
            },
        }
        """
    framework = mongodb.db.db
    output = []
    for q in framework.find({'出租者': {'$in': [re.compile(u'吳小姐'), re.compile(u'吳太太')]},
                             '出租者身份': '屋主', '地點': '台北市'}):
        output.append({'地點': q['地點'], '出租者': q['出租者'],
                       '出租者身份': q['出租者身份'], '聯絡電話': q['聯絡電話'],
                       '型態': q['型態'], '現況': q['現況'],
                       '性別要求': q['性別要求']})
    if not output:
        output = 'No results found'

    return jsonify({'result': output})


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
