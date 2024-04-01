import time
import subprocess

YMAX = 5  # max y value to allow switching
MOVE_DISTANCE = 400  # distance need to travel to switch workspace
WORKSPACE_COUNT = 7  # the number of workspace in hyprland
SLEEP = 0.01  # sleep time between measurments


def get_mouse():
    str = subprocess.check_output([b'hyprctl', b'cursorpos']).split(b',')
    return int(str[0]), int(str[1])


def get_workspace():
    str = subprocess.check_output(['hyprctl', 'activeworkspace'])
    return int(str[13:14])


def set_workspace(pos: int):
    if 0 < pos <= WORKSPACE_COUNT:  # limit the range of workspaces
        subprocess.check_output(['hyprctl', 'dispatch', 'workspace', str(pos)])


if __name__ == '__main__':
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
                    if distance >= MOVE_DISTANCE:  # check if distance traveld is enough
                        distance = -MOVE_DISTANCE / 2
                        set_workspace(get_workspace() + 1)
                    if distance <= -MOVE_DISTANCE:
                        set_workspace(get_workspace() - 1)
                        distance = +MOVE_DISTANCE / 2
