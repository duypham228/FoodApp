import session_manager


class test():
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def print(self):
        print(session_manager.sessions)
    
    def create_session(self, username):
        session_manager.create_session(username)
    

test1 = test(session_manager)
test2 = test(session_manager)

test1.create_session("test1")
test2.create_session("test2")

test1.print()

