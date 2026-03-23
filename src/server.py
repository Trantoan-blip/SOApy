import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import linkedin_service
import gmail_service
import calendar_service

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global storage for tokens (should use database in production)
linkedin_token = None
google_tokens = None


# ==================== LinkedIn Routes ====================
@app.route('/linkedin/auth-url', methods=['GET'])
def linkedin_auth_url():
    """Lấy URL xác thực LinkedIn"""
    url = linkedin_service.get_auth_url()
    return jsonify({'url': url})


@app.route('/callback', methods=['GET'])
def linkedin_callback():
    """Callback sau khi LinkedIn redirect về"""
    try:
        code = request.args.get('code')
        global linkedin_token
        linkedin_token = linkedin_service.get_access_token(code)
        profile = linkedin_service.get_profile(linkedin_token)
        return jsonify({'success': True, 'profile': profile})
    except Exception as err:
        return jsonify({'error': str(err)}), 500


@app.route('/linkedin/profile', methods=['GET'])
def linkedin_profile():
    """Xem profile LinkedIn"""
    try:
        if not linkedin_token:
            return jsonify({'error': 'Chưa xác thực LinkedIn'}), 401
        profile = linkedin_service.get_profile(linkedin_token)
        return jsonify(profile)
    except Exception as err:
        return jsonify({'error': str(err)}), 500


@app.route('/linkedin/post', methods=['POST'])
def linkedin_post():
    """Đăng bài LinkedIn"""
    try:
        data = request.get_json()
        text = data.get('text')
        result = linkedin_service.create_post(linkedin_token, text)
        return jsonify({'success': True, 'result': result})
    except Exception as err:
        return jsonify({'error': str(err)}), 500


# ==================== Gmail Routes ====================
@app.route('/google/auth-url', methods=['GET'])
def google_auth_url():
    """Lấy URL xác thực Google"""
    url = gmail_service.get_auth_url()
    return jsonify({'url': url})


@app.route('/google/callback', methods=['GET'])
def google_callback():
    """Callback sau khi Google redirect về"""
    try:
        code = request.args.get('code')
        global google_tokens
        google_tokens = gmail_service.set_tokens(code)
        return jsonify({'success': True, 'message': 'Google đã kết nối!'})
    except Exception as err:
        return jsonify({'error': str(err)}), 500


@app.route('/gmail/list', methods=['GET'])
def gmail_list():
    """Xem danh sách email"""
    try:
        emails = gmail_service.list_emails()
        return jsonify(emails)
    except Exception as err:
        return jsonify({'error': str(err)}), 500


@app.route('/gmail/send', methods=['POST'])
def gmail_send():
    """Gửi email"""
    try:
        data = request.get_json()
        to = data.get('to')
        subject = data.get('subject')
        body = data.get('body')
        gmail_service.send_email({'to': to, 'subject': subject, 'body': body})
        return jsonify({'success': True, 'message': 'Email đã gửi!'})
    except Exception as err:
        return jsonify({'error': str(err)}), 500


# ==================== Calendar Routes ====================
@app.route('/calendar/events', methods=['GET'])
def calendar_events():
    """Xem danh sách sự kiện"""
    try:
        events = calendar_service.list_events()
        return jsonify(events)
    except Exception as err:
        return jsonify({'error': str(err)}), 500


@app.route('/calendar/create', methods=['POST'])
def calendar_create():
    """Tạo sự kiện mới"""
    try:
        data = request.get_json()
        event = calendar_service.create_event(
            summary=data.get('summary'),
            description=data.get('description'),
            start=data.get('start'),
            end=data.get('end')
        )
        return jsonify({'success': True, 'event': event})
    except Exception as err:
        return jsonify({'error': str(err)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(debug=False, host='0.0.0.0', port=port)
