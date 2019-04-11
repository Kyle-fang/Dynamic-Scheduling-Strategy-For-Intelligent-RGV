Con=[0 for _ in range(len(Zeros_CNC)*10)]
print(Con)
for count_0 in range(len(Times_CNC)):
    for count_1 in CNC_Carry_State:
        if count_1==0:
            Con[count_0*len(Zeros_CNC)+count_1]=RGV_IMPORT_CNC_TIME[count_0]
        elif count_1==1:
            Con[count_0*len(Zeros_CNC)+count_1] = RGV_IMPORT_CNC_TIME[count_0]
print(Con)