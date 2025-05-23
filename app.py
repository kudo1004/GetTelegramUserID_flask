from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError, PeerIdInvalidError
import asyncio

api_id = 27762792  # ← Thay bằng của bạn
api_hash = '9738786356de12185e59b8d2f35863a9'
session_name = 'session'

app = Flask(__name__)

# Tạo loop mới 100% không bị lỗi trên Python 3.10+
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient(session_name, api_id, api_hash, loop=loop)

# Khởi động Telegram client
async def startup():
    await client.start()
    print("✅ Telegram client started")

loop.run_until_complete(startup())

@app.route('/get_user', methods=['GET'])
def get_user():
    q = request.args.get('q')
    if not q:
        return jsonify({'telegram': "@kudo1004", 'error': 1, 'message': 'Thiếu tham số ?q=username hoặc ?q=id'}), 400

    try:
        if q.isdigit():
            user = loop.run_until_complete(client.get_entity(int(q)))
        else:
            user = loop.run_until_complete(client.get_entity(q))

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
            'status': str(user.status),  # chuyển status thành chuỗi
            'has_profile_photo': user.photo is not None,
})


    except (UsernameNotOccupiedError, PeerIdInvalidError):
        return jsonify({'telegram': "@kudo1004", 'error': 1, 'message': 'Không tìm thấy người dùng'}), 404
    except Exception as e:
        return jsonify({'telegram': "@kudo1004", 'error': 1, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
