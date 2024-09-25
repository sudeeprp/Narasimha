
class Doer:
    def __init__(self, player_func, serialtalker_func):
        self.play = player_func
        self.talk = serialtalker_func
    
    def do(self, actions):
        for activity in actions if actions else []:
            done_func = activity['done'] if 'done' in activity else None
            self.play(activity['do'], done_func)
            self.talk(activity['do'])
