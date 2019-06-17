def Init():
    global RGV_MOVE_TIME  # RGV移动下标个单位距离所用时间
    global CNC_WORK_TIME  # CNC加工物料所用时间
    global RGV_IMPORT_CNC_TIME  # RGV为CNC上下料所用时间
    global RGV_CLEAR_TIME  # RGV清洗物料所用时间
    global EndTime  # 工作期间时间单元个数 8*60*60s
    global AllProduct
    global NowTime
    global TimeUnit  # 默认时间单元 1s
    global CNC_Carry_State  # 【0】没有工件在加工 【1】有工件在加工或加工完成
    global CNC_Min_Time  # 【0】加工完成 【X】正在加工
    global RGV_Carry_State  # 【0，X】不存在工件 【1，0】存在工件正在加工 【1，1】存在工件已加工完成
    global RGV_Locat  # 0,1 2,3 4,5 6,7
    global RGV_Min_Time
    RGV_MOVE_TIME = [0, 20, 33, 46]
    CNC_WORK_TIME = 560
    RGV_IMPORT_CNC_TIME = [28, 31, 28, 31, 28, 31, 28, 31]
    RGV_CLEAR_TIME = 25
    EndTime = 28800
    AllProduct = 0  # 起始成品个数
    NowTime = 0  # 当前时间节点 起始时间 0s
    TimeUnit = 1  # 默认时间单元 1s
    CNC_Carry_State = [0, 0, 0, 0, 0, 0, 0, 0]  # 【0】没有工件在加工 【1】有工件在加工或加工完成
    CNC_Min_Time = [0, 0, 0, 0, 0, 0, 0, 0]  # 【0】加工完成 【X】正在加工
    RGV_Carry_State = [0, 0]  # 【0，X】不存在工件 【1，0】存在工件正在加工 【1，1】存在工件已加工完成
    RGV_Locat = 0  # 0,1 2,3 4,5 6,7
    RGV_Min_Time = 0
Init()