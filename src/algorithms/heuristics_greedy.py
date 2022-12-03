import pandas as pd
import time

OR_MAX = 2
coefficients = []
horizon_calendar = []
start = time.time()

def relative_weight_patient(data, patient_index):  
    return data.iloc[patient_index]['PRIORITY'] / data.iloc[patient_index]['LOS'] 

def get_relative_weight_patient_data(data):
    data_arr = [[i, relative_weight_patient(data, i)] for i in range(0, len(data))]
    return pd.DataFrame(data_arr, columns = ['INDEX','RELATIVE_WEIGHT']).sort_values(ascending=False,by=['RELATIVE_WEIGHT'])

def sort_data_by_weight(data, relative_weight_index_data):
    sorted_data = pd.DataFrame([data.iloc[int(relative_weight_index_data.iloc[i]['INDEX'])] for i in range(0 , len(relative_weight_index_data))])
    sorted_data['RELATIVE_WEIGHT'] = relative_weight_index_data['RELATIVE_WEIGHT']
    return sorted_data

def assign_patients(data_sorted_weigth): 
    i = 0
    res_list = [] 
    aux_list = []
    total_los = 0
    while i < len(data_sorted_weigth):
        total_los = total_los + data_sorted_weigth.iloc[i]['LOS']
        if(total_los<=5): 
            aux_list.append(data_sorted_weigth.iloc[i])
            i=i+1
        else:
            total_los = 0
            res_list.append(pd.DataFrame(aux_list))
            aux_list = []
    return res_list

def getHorizonPlanning(assigned_patiens_data): 
    return [assigned_patiens_data[n:n+OR_MAX] for n in range(0, len(assigned_patiens_data), OR_MAX)]

def print_horizon_planning(data):
    for i in range(0, len(data)):
        print('Week: ', i+1)
        for j in range(0, len(data[i])):
            print('\nOR:', j+1)
            print(data[i][j])
        print('.......................\n')

def get_total_cost_patients(data):
    return data['RELATIVE_WEIGHT'].sum()

def get_cost_z(assigned_patiens_data,data_sorted_weigth):
    assigned_patients_count_day = 0
    total_cost_assigned = 0   
    total_cost = data_sorted_weigth['RELATIVE_WEIGHT'].sum()
    print(1,'& ', total_cost, '&', time.time() - start, '\\\\')
    for i in range(0, len(assigned_patiens_data)):
        for j in range(0, len(assigned_patiens_data[i])):  
            total_cost_assigned = total_cost_assigned + get_total_cost_patients(assigned_patiens_data[i][j])
        total_cost = total_cost - total_cost_assigned
        print(i+2,'& ', round(total_cost,2), '&', round(time.time() - start, 4), 'ms \\\\')
        total_cost_assigned = 0

def main_heuristics_greedy(data): 
    data['LOS'] = data['LOS'].replace(6,1)
    relative_weight_index_data = get_relative_weight_patient_data(data)
    data_sorted_weigth = sort_data_by_weight(data,relative_weight_index_data)
    assign_patients_data = assign_patients(data_sorted_weigth)
    print('....................................')
    print('HORIZON PLANNING:')
    print_horizon_planning(getHorizonPlanning(assign_patients_data))
    print('Time Ellapsed: ', time.time() - start )

