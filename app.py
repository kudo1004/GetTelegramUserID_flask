from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

api_id = 27762792
api_hash = '9738786356de12185e59b8d2f35863a9'

# Đường dẫn đến file session đã upload lên server
session_path = 'tmp/session'  # <-- nhớ upload session.session lên /tmp/

app = Flask(__name__)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient(session_path, api_id, api_hash, loop=loop)

async def startup():
    await client.start()
    print("✅ Telegram client started")

loop.run_until_complete(startup())

@app.route('/get_user', methods=['GET'])
def get_user():
    q = request.args.get('q')
    if not q:
        return jsonify({'error': 1, 'message': 'Thiếu tham số ?q=id hoặc ?q=username'}), 400

    try:
        if q.isdigit():
            user = loop.run_until_complete(client.get_entity(int(q)))
        else:
            user = loop.run_until_complete(client.get_entity(q))

        return jsonify({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', None),
            'is_bot': getattr(user, 'bot', None),
            'verified': getattr(user, 'verified', None),
            'fake': getattr(user, 'fake', None),
            'scam': getattr(user, 'scam', None),
            'restricted': getattr(user, 'restricted', None),
            'premium': getattr(user, 'premium', None),
            'lang_code': getattr(user, 'lang_code', None),
            'status': str(getattr(user, 'status', None)),
            'has_profile_photo': user.photo is not None,
        })
    except Exception as e:
        return jsonify({'error': 1, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
