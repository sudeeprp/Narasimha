
class Doer:
    def __init__(self, requester_func):
        self.requester = requester_func
    
    def do(self, actions):
        for activity in actions if actions else []:
            done_func = activity['done'] if 'done' in activity else None
            self.requester(activity['do'], done_func)
