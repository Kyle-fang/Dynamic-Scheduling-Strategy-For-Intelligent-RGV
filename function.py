

def one_step_time(ai_settings, step):
    MT = move_time(ai_settings, step)
    wait_time = RGV_wait_time(ai_settings, step, MT)
    L_UL_time = loading_and_unloading_time(ai_settings, step)
    if ai_settings.CNC_remaining_processing_time[step-1] >= MT:
        T = ai_settings.CNC_remaining_processing_time[step-1] + L_UL_time
    else:
        T = MT + L_UL_time
    return T + ai_settings.RGV_clear_time

def move_time(ai_settings, step):
    if step < 3 and step > 0:
        L = 1
    elif step < 5 and step > 2:
        L = 2
    elif step < 7 and step > 4:
        L = 3
    else:
        L = 4
    if ai_settings.Locate_RGV-L == 0:
        return 0
    elif abs(ai_settings.Locate_RGV-L) == 1:
        return ai_settings.move_one_step_time
    elif abs(ai_settings.Locate_RGV-L) == 2:
        return ai_settings.move_two_step_time
    else:
        return ai_settings.move_three_step_time
def RGV_wait_time(ai_settings, one_step, MT):
    if ai_settings.CNC_remaining_processing_time[one_step-1] > MT:
        wait_time = ai_settings.CNC_remaining_processing_time[one_step-1]-MT
    else:
        wait_time=0
    return wait_time

def loading_and_unloading_time(ai_settings, step):
    if step%2 == 0:
        time = ai_settings.RGV_up_odd_time
    else:
        time = ai_settings.RGV_up_even_time

    return time

def update_status(ai_settings, next_place, next_CNC, optimal_time):
    ai_settings.Locate_RGV = next_place
    #ai_settings.CNC_status[next_CNC-1] = 1
    for num in range(1,9):
        ai_settings.CNC_remaining_processing_time[num-1] = ai_settings.CNC_remaining_processing_time[num-1] - optimal_time

    ai_settings.CNC_remaining_processing_time[next_CNC-1] = ai_settings.CNC_work_time


