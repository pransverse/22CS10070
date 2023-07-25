#####################################################################
# This script presents how to use the most basic features of the environment.
# It configures the engine, and makes the agent perform random actions.
# It also gets current state and reward earned with the action.
# <episodes> number of episodes are played.
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

import os
from random import choice
import math
from time import sleep
import vizdoom as vzd
import numpy as np
import cv2 as cv


def navigate(game, vars, target):
    if (
        abs(int(vars[0]) - int(target[0])) < 4
        and abs(int(vars[1]) - int(target[1])) < 4
    ):
        return None
    dx = target[0] - vars[0]
    dy = target[1] - vars[1]
    angle = (math.atan2(dy, dx) * 180 / math.pi) % 360
    print("angle: ", angle)
    turn_angle = angle - vars[2]
    print("turn: ", turn_angle)
    action = [0, 0, 1, 0, -turn_angle]
    game.make_action(action)
    return 1


if __name__ == "__main__":
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    # Now it's time for configuration!
    # load_config could be used to load configuration instead of doing it here with code.
    # If load_config is used in-code configuration will also work - most recent changes will add to previous ones.
    # game.load_config("../../scenarios/basic.cfg")

    # Sets path to additional resources wad file which is basically your scenario wad.
    # If not specified default maps will be used and it's pretty much useless... unless you want to play good old Doom.
    game.set_doom_scenario_path("C:\Prans\AGV\ViZDoom\MAP01.wad")

    # Sets map to start (scenario .wad files can contain many maps).
    game.set_doom_map("map01")

    game.load_config("github\ViZDoom\scenarios\level1.cfg")

    # Sets resolution. Default is 320X240
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    # Sets the screen buffer format. Not used here but now you can change it. Default is CRCGCB.
    game.set_screen_format(vzd.ScreenFormat.RGB24)

    # Enables depth buffer.
    game.set_depth_buffer_enabled(True)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(True)

    # Enables buffer with top down map of the current episode/level.
    game.set_automap_buffer_enabled(True)

    # Enables information about all objects present in the current episode/level.
    game.set_objects_info_enabled(True)

    # Enables information about all sectors (map layout).
    game.set_sectors_info_enabled(True)

    # Sets other rendering options (all of these options except crosshair are enabled (set to True) by default)
    game.set_render_hud(False)
    game.set_render_minimal_hud(False)  # If hud is enabled
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(False)  # Bullet holes and blood on the walls
    game.set_render_particles(False)
    game.set_render_effects_sprites(False)  # Smoke and blood
    game.set_render_messages(False)  # In-game messages
    game.set_render_corpses(False)
    game.set_render_screen_flashes(
        True
    )  # Effect upon taking damage or picking up items

    # Adds buttons that will be allowed to use.
    # This can be done by adding buttons one by one:
    # game.clear_available_buttons()
    # game.add_available_button(vzd.Button.MOVE_LEFT)
    # game.add_available_button(vzd.Button.MOVE_RIGHT)
    # game.add_available_button(vzd.Button.ATTACK)
    # Or by setting them all at once:
    game.set_available_buttons(
        [
            vzd.Button.MOVE_LEFT,
            vzd.Button.MOVE_RIGHT,
            vzd.Button.MOVE_FORWARD,
            vzd.Button.MOVE_BACKWARD,
            vzd.Button.TURN_LEFT_RIGHT_DELTA,
        ]
    )
    # Buttons that will be used can be also checked by:
    print("Available buttons:", [b.name for b in game.get_available_buttons()])

    # Adds game variables that will be included in state.
    # Similarly to buttons, they can be added one by one:
    # game.clear_available_game_variables()
    # game.add_available_game_variable(vzd.GameVariable.AMMO2)
    # Or:
    game.set_available_game_variables(
        [
            vzd.GameVariable.POSITION_X,
            vzd.GameVariable.POSITION_Y,
            vzd.GameVariable.ANGLE,
        ]
    )
    print(
        "Available game variables:",
        [v.name for v in game.get_available_game_variables()],
    )

    # Causes episodes to finish after 200 tics (actions)
    game.set_episode_timeout(200)

    # Makes episodes start after 10 tics (~after raising the weapon)
    game.set_episode_start_time(10)

    # Makes the window appear (turned on by default)
    game.set_window_visible(True)

    # Turns on the sound. (turned off by default)
    # game.set_sound_enabled(True)
    # Because of some problems with OpenAL on Ubuntu 20.04, we keep this line commented,
    # the sound is only useful for humans watching the game.

    # Sets the living reward (for each move) to -1
    game.set_living_reward(-1)

    # Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
    game.set_mode(vzd.Mode.PLAYER)

    # Enables engine output to console.
    # game.set_console_enabled(True)

    # Initialize the game. Further configuration won't take any effect from now on.
    game.init()

    # Define some actions. Each list entry corresponds to declared buttons:
    # MOVE_LEFT, MOVE_RIGHT, ATTACK
    # game.get_available_buttons_size() can be used to check the number of available buttons.
    # 5 more combinations are naturally possible but only 3 are included for transparency when watching.
    actions = [
        [True, False, True, False, 1],
        [False, True, False, True, 1],
        [False, True, True, False, -1],
        [True, False, False, True, -1],
    ]

    # Run this many episodes
    episodes = 1

    # Sets time that will pause the engine after each action (in seconds)
    # Without this everything would go too fast for you to keep track of what's happening.
    sleep_time = 2.5  # = 0.028

    for i in range(episodes):
        print("Episode #" + str(i + 1))

        # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
        game.new_episode()

        while not game.is_episode_finished():
            # Gets the state
            state = game.get_state()
            # Which consists of:
            n = state.number
            vars = state.game_variables
            print(vars)

            game.make_action([0, 0, 1, 0, 45])
            game.make_action([0, 0, 1, 0, 0], 40)

            if sleep_time > 0:
                sleep(sleep_time)

            vars = game.get_state().game_variables
            automap = state.automap_buffer
            # error handling

            # self position
            pos_y, pos_x = np.where((automap == [255, 255, 255]).all(axis=-1))
            x, y = pos_x[0], pos_y[0]

            flags = 0
            sub_array = automap[y - 2 : y + 3, x - 2 : x + 3]
            # check for corners
            for p in range(5):
                for q in range(5):
                    if list(sub_array[p][q]) == [11, 27, 47]:
                        flags += 1
            if flags >= 5:
                print("corner detected")
                # find closest exit
                b, c = 0, 0
                for b in range(5, 50):
                    for c in range(-b, b + 1):
                        if (
                            automap[y + c][x + b][0]
                            == automap[y + c][x + b][1]
                            == automap[y + c][x + b][2]
                        ):
                            target = x + b, y + c
                            break
                        if (
                            automap[y + c][x - b][0]
                            == automap[y + c][x - b][1]
                            == automap[y + c][x - b][2]
                        ):
                            target = x - b, y + c
                            break
                        if (
                            automap[y + b][x + c][0]
                            == automap[y + b][x + c][1]
                            == automap[y + b][x + c][2]
                        ):
                            target = x + c, y + b
                            break
                        if (
                            automap[y - b][x + c][0]
                            == automap[y - b][x + c][1]
                            == automap[y - b][x + c][2]
                        ):
                            target = x + c, y - b
                            break
                target = np.array(target).astype("float")
                target = target - [448.83273, 207.3518]
                target[0] /= 0.09293
                target[1] /= -0.09168
                while navigate(game, vars, target):
                    state = game.get_state()
                    vars = state.game_variables
                    print(vars)
                    automap = state.automap_buffer
                    cv.imshow("ViZDoom Map Buffer", automap)
                    cv.waitKey(1)

            break

            # Prints state's game variables and reward.
            print("State #" + str(n))
            print("Game variables:", vars)
            print("=====================")
            if n == 50:
                break

            if sleep_time > 0:
                sleep(sleep_time)

        # Check how the episode went.
        print("Episode finished.")
        print("Total reward:", game.get_total_reward())
        print("************************")

    # It will be done automatically anyway but sometimes you need to do it in the middle of the program...
    game.close()
