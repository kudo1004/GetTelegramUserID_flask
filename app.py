from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError, PeerIdInvalidError
import asyncio
import os

api_id = 27762792
api_hash = '9738786356de12185e59b8d2f35863a9'
session_name = 'session'  # file session sẽ tạo trong cùng thư mục

app = Flask(__name__)

async def fetch_user(q):
    async with TelegramClient(session_name, api_id, api_hash) as client:
        if q.isdigit():
            user = await client.get_entity(int(q))
        else:
            user = await client.get_entity(q)
        return user


@app.route('/debug', methods=['GET'])
def debug():
    filename = 'session.session'  # tên file session bạn dùng
    can_read = os.access(filename, os.R_OK)
    can_write = os.access(filename, os.W_OK)
    file_exists = os.path.exists(filename)

    return jsonify({
        'file': filename,
        'exists': file_exists,
        'can_read': can_read,
        'can_write': can_write,
    })


@app.route('/get_user', methods=['GET'])
def get_user():
    q = request.args.get('q')
    if not q:
        return jsonify({'telegram': "@kudo1004", 'error': 1, 'message': 'Thiếu tham số ?q=username hoặc ?q=id'}), 400

    try:
        user = asyncio.run(fetch_user(q))  # Tạo event loop mới, chạy async function
        return jsonify({
            'telegram': "@kudo1004",
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'is_bot': user.bot,
            'verified': user.verified,
            'fake': user.fake,
            'scam': user.scam,
            'restricted': user.restricted,
            'premium': user.premium,
            'lang_code': user.lang_code,
            'status': str(user.status),
            'has_profile_photo': user.photo is not None,
        })

    except (UsernameNotOccupiedError, PeerIdInvalidError):
        return jsonify({'telegram': "@kudo1004", 'error': 1, 'message': 'Không tìm thấy người dùng'}), 404
    except Exception as e:
        return jsonify({'telegram': "@kudo1004", 'error': 1, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
