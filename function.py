from settings import Settings

def one_step_time(move_time, wait_time, RGV_clear_time, Locate_RGV, one_step,move_one_step_time):
    move_time()


def move_time(locate_RGV, one_step, move_one_step_time, move_two_step_time):
    if one_step == 1 or 2:
        L = 1
    elif one_step == 3 or 4:
        L = 2
    elif one_step == 5 or 6:
        L = 3
    else:
        L = 4
    if abs(locate_RGV-L) == 1:
        return move_one_step_time
    elif abs(locate_RGV-L) == 2:
        return move_two_step_time

def wait_time():
    pass
