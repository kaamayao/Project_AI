from src.algorithms.heuristics_greedy import main_heuristics_greedy
from src.algorithms.heuristics_mthm import main_heuristics_mthm
from data.data_generate import get_data

def execute_option(option):
    use_default_dataset = False
    use_default_syntetic_dataset = False
    if option == '3' or option == '':
        return
    number_patients = 80
    try:                            
        number_patients = int(input('Input the number of patients(default=80):'))
        print() 
    except ValueError:
        number_patients = 80
        print() 

    print('number_patients',number_patients)
    default_syntenthic = [200, 500, 1000, 5000, 10000]
    use_default_dataset = number_patients == 80

    try:                            
        index_value_syntethic = default_syntenthic.index(number_patients)
        use_default_syntetic_dataset = True 
        print() 
    except ValueError:
        print() 

    data = get_data(int(number_patients), use_default_dataset, use_default_syntetic_dataset)
    if option == '1':
        main_heuristics_greedy(data)
    if option == '2':
        main_heuristics_mthm(data)

def prompt_main_menu():
    option = ''
    while(option != '3'):
        option = ''
        print('\n...........................')
        print('MMS Schedule solver')
        print('...........................')
        print('1. Solve using greedy heuristic')
        print('2. Solve using mthm heuristic')
        print('3. Exit')
        option = input("")
        execute_option(option)
    
prompt_main_menu()
