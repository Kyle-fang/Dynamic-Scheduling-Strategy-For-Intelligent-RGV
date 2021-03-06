class Settings():
    def __init__(self):
        self.Locate_RGV = 1     #1:在#1位置 2:在#2位置 3:在#3位置 4:在#4位置
        self.RGV_status = 0     #0：不在工作状态(即在等待状态中） 1：在工作状态
        self.CNC_status = [0,0,0,0,0,0,0,0]     #0：不在加工 1：在加工
        self.CNC_type = [0,0,0,0,0,0,0,0]   #CNC的类型，1：加工第一道工序， 2：加工第二道工序
        self.CNC_remaining_processing_time = [0,0,0,0,0,0,0,0]      #CNC剩余加工时间
        #RGV分别移动一步，两步，三步的时间
        self.move_one_step_time = 0
        self.move_two_step_time = 0
        self.move_three_step_time = 0
        #两道工序加工的时间
        self.CNC_work_time_1 = 0
        self.CNC_work_time_2 = 0
        #RGV分别给奇数号CNC和偶数号CNC上料的时间
        self.RGV_up_even_time = 0
        self.RGV_up_odd_time = 0
        #物料清洗时间
        self.RGV_clear_time = 0