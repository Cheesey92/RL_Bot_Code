# This is the main file where you control your bot's strategy

from util.objects import *
from util.routines import *
from util.tools import *
# Hi! Corbin here. Note the line below says GoslingUtils in the videos.
# DO NOT change the line below. It's no longer compatible with GoslingUtils so we renamed it.
# There are a few places like this where the code that you started with (the code you downloaded) might
# look different than the videos. THAT'S OK! Don't change it. We've made it better over time.
# Just follow along with the videos and it will all work the same.
class Bot(BotCommandAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        if self.intent is not None:
            return
        if self.kickoff_flag:
            # set_intent tells the bot what it's trying to do
            if abs(self.me.location[0]) > 1000:
                return self.set_intent(dodge_kickoff())
            else:
                return self.set_intent(kickoff())
        # if we're infront of the ball, retreat
        if self.is_in_front_of_ball() is True:
            self.set_intent(goto(self.friend_goal.location))
            return
        self.set_intent(short_shot(self.foe_goal.location))
        targets = {
            'at_opponent_goal' : (self.foe_goal.left_post, self.foe_goal.right_post),
            'away from our net' : (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self,targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            return
        if len(hits['away from our net']) > 0:
            self.set_intent(hits['away from our net'][0])
            return
        
        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            return

        target_boost = self.get_closest_large_boost()
        if target_boost is not None:
            self.set_intent(goto(target_boost.location))
            return
        
        if self.is_opponent_close():
            self.set_intent(goto(self.friend_goal.location))
            print('done')
            return