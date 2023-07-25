from argparse import ArgumentParser
import os
from random import choice
import vizdoom as vzd
import numpy as np
import math
import cv2 as cv

# DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deadly_corridor.cfg")
DEFAULT_CONFIG = "github\ViZDoom\scenarios\level1.cfg"


def map_to_game(q):
    q = q - [448.94429, 206.82446]
    q[:, 0] /= 0.08839
    q[:, 1] /= -0.08888
    return q


def navigate(game, vars, target):
    if (
        abs(int(vars[0]) - int(target[0])) < 6
        and abs(int(vars[1]) - int(target[1])) < 6
    ):
        return None
    dx = target[0] - vars[0]
    dy = target[1] - vars[1]
    angle = (math.atan2(dy, dx) * 180 / math.pi) % 360
    turn_angle = int(angle - vars[2])
    action = [0, 0, 0, 0, -turn_angle]
    game.make_action(action)
    action = [0, 0, 1, 0, 0]
    game.make_action(action)
    return 1


if __name__ == "__main__":
    """
    ############################################################################################################################################################
    These are pre-set configurations for level1 and level2 of the task, please dont change them

    ############################################################################################################################################################
    """

    parser = ArgumentParser(
        "ViZDoom example showing different buffers (screen, depth, labels)."
    )
    parser.add_argument(
        dest="config",
        default=DEFAULT_CONFIG,
        nargs="?",
        help="Path to the configuration file of the scenario."
        " Please see "
        "../../scenarios/*cfg for more scenarios.",
    )

    args = parser.parse_args()

    game = vzd.DoomGame()

    # Use other config file if you wish.
    game.load_config("github\ViZDoom\scenarios\level1.cfg")

    # OpenCV uses a BGR colorspace by default.
    game.set_screen_format(vzd.ScreenFormat.BGR24)

    # Sets resolution for all buffers.
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    # Enables depth buffer.
    game.set_depth_buffer_enabled(True)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(True)

    # Enables buffer with top down map of he current episode/level .
    game.set_automap_buffer_enabled(True)
    game.set_automap_mode(vzd.AutomapMode.OBJECTS)
    game.set_automap_rotate(False)
    game.set_automap_render_textures(False)

    # game.set_render_hud(True)
    game.set_render_hud(False)
    game.set_render_minimal_hud(False)

    # entire map is shown
    game.add_game_args("+viz_am_center 1")

    """
    ##############################################################################################################################################################
    Feel free to change anything after this
    ##############################################################################################################################################################
    """
    # uncomment this if you want to play the game with keyboard controls
    # game.set_mode(vzd.Mode.SPECTATOR)

    # The buttons you can use to make actionns currently are:
    # MOVE_LEFT, MOVE_RIGHT, MOVE_FORWARD, MOVE_BACKWARD, TURN_LEFT_RIGHT_DELTA
    # setting available buttons here:
    game.set_available_buttons(
        [
            vzd.Button.MOVE_LEFT,
            vzd.Button.MOVE_RIGHT,
            vzd.Button.MOVE_FORWARD,
            vzd.Button.MOVE_BACKWARD,
            vzd.Button.TURN_LEFT_RIGHT_DELTA,
        ]
    )

    # check this link for all available buttons, use any you find useful: https://github.com/mwydmuch/ViZDoom/blob/master/doc/Types.md#button

    # The state variables which you get from the game currently are:
    # POSITION_X, POSITION_Y, ANGLE
    # setting available game variables here:
    game.set_available_game_variables(
        [
            vzd.GameVariable.POSITION_X,
            vzd.GameVariable.POSITION_Y,
            vzd.GameVariable.ANGLE,
        ]
    )

    # check this link for all available game variables, use any you find useful: https://github.com/mwydmuch/ViZDoom/blob/master/doc/Types.md#gamevariable

    game.init()

    episodes = 1
    sleep_time = 0.028

    for i in range(episodes):
        print("Episode #" + str(i + 1))

        # Not needed for the first episode but the loop is nicer.
        game.new_episode()

        # retrieve path from rrt star:
        loaded_arrays = np.load("path.npz", allow_pickle=True)
        path = loaded_arrays["path_arr"]
        path = np.array(path).astype("float")
        path = map_to_game(path)

        # episode ends after you reach the key(end of game) or after a given time(300 seconds fixed in the config file)
        while not game.is_episode_finished():
            # Gets the state and possibly do something with it
            state = game.get_state()
            vars = state.game_variables
            automap = state.automap_buffer
            # cv.imwrite("map.png", automap)
            cv.imshow("ViZDoom Map Buffer", automap)
            cv.waitKey(1)

            n = len(path)
            i = 0

            while i < n - 1:
                dist = int(math.sqrt(np.sum(abs(vars[:2] - path[i + 1]) ** 2)))
                count = 0
                prev_vars = game.get_state().game_variables
                target = path[i + 1]
                while navigate(game, vars, target):
                    count += 1
                    state = game.get_state()
                    if not state:
                        break
                    vars = state.game_variables
                    automap = state.automap_buffer
                    cv.imshow("ViZDoom Map Buffer", automap)
                    cv.waitKey(1)

                    # error handling
                    if count >= dist:
                        if choice([0, 1]):
                            i -= 2
                        print("broke")
                        break

                i += 1

            if automap is not None:
                cv.imshow("ViZDoom Map Buffer", automap)

            cv.waitKey(int(sleep_time * 1000))

        print("\n\n\nEpisode finished!\n\n")
        print("************************")

    cv.destroyAllWindows()
