import uuid
import time
from http.cookies import SimpleCookie

sessions = {}

def create_session(username):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'username': username, 'timestamp': time.time()}
    
    # Create a SimpleCookie for the session ID
    session_cookie = SimpleCookie()
    session_cookie['session_id'] = session_id
    session_cookie['session_id']['path'] = '/'
    session_cookie['session_id']['expires'] = 7200  # Set the expiration time (e.g., 30 minutes)

    # Return the session ID as a cookie string
    return session_cookie

def is_valid_session(session_id):
    if session_id in sessions:
        session = sessions[session_id]
        # Check session expiration (e.g., 30 minutes)
        if time.time() - session['timestamp'] < 7200:
            session['timestamp'] = time.time()
            return True
        else:
            del sessions[session_id]
    return False

def get_username(session_id):
    if session_id in sessions:
        return sessions[session_id]['username']
    return None
