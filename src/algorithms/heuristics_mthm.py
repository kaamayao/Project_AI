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

def get_total_cost_patients(data):
    return data['RELATIVE_WEIGHT'].sum()

def get_cost_z(assigned_patiens_data,data_sorted_weigth):
    assigned_patients_count_day = 0
    total_cost_assigned = 0   
    total_cost = data_sorted_weigth['RELATIVE_WEIGHT'].sum()
    for i in range(0, len(assigned_patiens_data)):
        for j in range(0, len(assigned_patiens_data[i])):  
            total_cost_assigned = total_cost_assigned + get_total_cost_patients(assigned_patiens_data[i][j])
        total_cost = total_cost - total_cost_assigned
        total_cost_assigned = 0

def shuffle_data(data):
    for i in range(0, len(data) - 2):
        data[i] = shuffle_data_items(data[i], data[i+1])
    return data

def check_restrains(data):
    can_schedule_patients = (data['LOS'].sum() <= 5)
    return can_schedule_patients

def get_weight_data(data):
    return data['PRIORITY'].sum() / data['LOS'].sum()

def shuffle_data_items(dataframes):
    for i in range(0, len(dataframes)):
        for j in range(i, len(dataframes)):
            min_dataframe_length = min(len(dataframes[i].index),len(dataframes[j].index))
            for k in range(0, min_dataframe_length - 1):
                if((dataframes[i].iloc[k]['LOS'] == dataframes[j].iloc[k]['LOS']) and
                    get_weight_data(dataframes[j].iloc[k]) > get_weight_data(dataframes[i].iloc[k])                    ): 
                    dataframes[i].loc[len(dataframes[i].index)] = dataframes[j].iloc[k].values.tolist()
                    dataframes[j] = dataframes[j].drop(dataframes[j].index[k])
    return dataframes

def get_row_index_by_los(data, los):
    max_index = -1
    max_value_los = 0
    for i in range(0, len(data)):
        if((data.iloc[i]['LOS'] <= los) and (max_value_los <= data.iloc[i]['LOS'])):
            max_index = i
            max_value_los = data.iloc[i]['LOS']
    return max_index

def fill_horizon(data): 
    for i in range(0, len(data)):
        total_los = data[i]['LOS'].sum()
        required_los = 5 - total_los 
        if(required_los > 0):
            for j in range(i+1, len(data)): 
                max_index_los = get_row_index_by_los(data[j],required_los)
                if(max_index_los >= 0):
                    required_los = required_los - data[j].iloc[max_index_los]['LOS']
                    data[i].loc[len(data[i].index)] = data[j].iloc[max_index_los].values.tolist()
                    data[j] = data[j].drop(data[j].index[max_index_los])
    return data
    
def filter_empty_dataframes(dataframes):
    res_array = []
    for i in range(0, len(dataframes)): 
        if( not dataframes[i].empty):
            res_array.append(dataframes[i])
    return res_array

def getHorizonPlanning(assigned_patiens_data): 
    return [assigned_patiens_data[n:n+OR_MAX] for n in range(0, len(assigned_patiens_data), OR_MAX)]

def print_horizon_planning(data):
    for i in range(0, len(data)):
        print('Week: ', i+1)
        for j in range(0, len(data[i])):
            print('\nOR:', j+1)
            print(data[i][j])
        print('.......................\n')

def main_heuristics_mthm(data): 
    data['LOS'] = data['LOS'].replace(6,1)
    relative_weight_index_data = get_relative_weight_patient_data(data)
    data_sorted_weigth = sort_data_by_weight(data,relative_weight_index_data)
    assign_patients_data = assign_patients(data_sorted_weigth)
    assign_patients_data = filter_empty_dataframes(fill_horizon(assign_patients_data))
    horizon_planning = getHorizonPlanning(assign_patients_data)
    print_horizon_planning(horizon_planning)
    get_cost_z(horizon_planning, data_sorted_weigth)
    print('time:', time.time() - start)
