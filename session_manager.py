import uuid
import time

sessions = {}

def create_session(username):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'username': username, 'timestamp': time.time()}
    return session_id

def is_valid_session(session_id):
    if session_id in sessions:
        session = sessions[session_id]
        # Check session expiration (e.g., 30 minutes)
        if time.time() - session['timestamp'] < 1800:
            session['timestamp'] = time.time()
            return True
        else:
            del sessions[session_id]
    return False

def get_username(session_id):
    if session_id in sessions:
        return sessions[session_id]['username']
    return None