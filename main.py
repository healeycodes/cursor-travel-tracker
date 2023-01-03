import math
import time

import rumps
from pynput import mouse


class DistanceTravelled(rumps.App):
    # sets the menu bar text of this 'app'
    def update_title(self, new_title):
        self.title = new_title


distance_travelled_app = DistanceTravelled('')

state = {
    'last_render_tick': time.time(),
    'cur_x': None,
    'cur_y': None,
    'total_dist': 0
}


def on_move():
    def inner_on_move(x, y):
        if state['cur_x'] is None or state['cur_y'] is None:
            # the first event sets the initial 'current point'
            state['cur_x'] = x
            state['cur_y'] = y
        else:
            # for the following events, we can track the distance travelled
            state['total_dist'] += math.hypot(x -
                                              state['cur_x'], y - state['cur_y'])
            state['cur_x'] = x
            state['cur_y'] = y

        # to stop flickering, only update every second
        cur_time = time.time()
        if cur_time - state['last_render_tick'] > 1:
            state['last_render_tick'] = cur_time
            readable_total_dist = f"Your cursor has travelled {int(state['total_dist'])} pixels"
            distance_travelled_app.update_title(
                readable_total_dist
            )
    return inner_on_move


mouse.Listener(on_move=on_move()).start()
# # to block execution, we could instead use..
# with mouse.Listener(on_move=on_move()) as listener:
#     listener.join()

if __name__ == "__main__":
    distance_travelled_app.run()
