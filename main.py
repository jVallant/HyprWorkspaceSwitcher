import sys
import getopt
import argparse
import time
import subprocess
import json

YMAX = 5  # max y value to allow switching
WORKSPACE_COUNT = 7  # the number of workspace in hyprland
SLEEP = 0.01  # sleep time between measurments

def get_mouse():
    str = subprocess.check_output([b'hyprctl', b'cursorpos']).split(b',')
    return int(str[0]), int(str[1])


def get_workspace():
    str = subprocess.check_output(['hyprctl', 'activeworkspace'])
    return int(str[13:14])

def get_scaled_delta_width(scale: float) -> int:
    monitors_json = subprocess.check_output(["hyprctl", "monitors", "-j"])
    monitors = json.loads(monitors_json)
    for monitor in monitors:
        if monitor["focused"]:
            width = float(monitor["width"])/float(monitor["scale"])
            return int(width*scale) # dynamic move distance

    return int(1920*scale) # default scale 

def set_workspace(pos: int):
    if 0 < pos <= WORKSPACE_COUNT:  # limit the range of workspaces
        subprocess.check_output(['hyprctl', 'dispatch', 'workspace', str(pos)])

def switch_workspace_hyprnome(right: True):
    if (right):
        subprocess.check_output(['hyprnome'])
    else:
        subprocess.check_output(['hyprnome', '-p'])

def main(argv):
    # Configure different arguments to pass to the program
    parser=argparse.ArgumentParser()
    parser.add_argument("-s", "--scale", type=float, default=0.20833333333333334, help="Range: [0.0, 1.0], float. Adjust what percentage of the current screen the mouse has to traverse to trigger a workspace switch")
    parser.add_argument("--hyprnome", action="store_true", help="Use hyprnome to switch workspaces (must be installed separately)")
    args=parser.parse_args()

    MOVE_DISTANCE = get_scaled_delta_width(args.scale)

    while True:
        time.sleep(SLEEP * 4)
        x, y = get_mouse()
        
        if y <= YMAX:
            distance = 0  # reset distance from previous movements
            previous_x = x  # over write the last x from previous unconected movements
            while True:
                time.sleep(SLEEP)
                x, y = get_mouse()

                if y > YMAX:  # quit if mouse leaves the allowed area
                    break
                    
                if x != previous_x:
                    distance += x - previous_x  # add the distance just traveled
                    previous_x = x
                    if distance >= MOVE_DISTANCE:  # check if distance traveled is enough
                        distance = -MOVE_DISTANCE / 2
                        if (args.hyprnome):  # check if using hyprnome
                            switch_workspace_hyprnome(right=False)
                        else:
                            set_workspace(get_workspace() + 1)
                    if distance <= -MOVE_DISTANCE:
                        distance = +MOVE_DISTANCE / 2
                        if (args.hyprnome):  # check if using hyprnome
                            switch_workspace_hyprnome(right=True)
                        else:
                            set_workspace(get_workspace() - 1)

if __name__ == '__main__':
    main(sys.argv[1:])
