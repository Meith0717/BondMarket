from dataclasses import dataclass

@dataclass
class data:
    person_name : str
    amount      : float
    comment     : str
    date        : str

@dataclass
class settings:
    data_path       : str
    appearance      : str
    jear            : int
    month           : int

@dataclass
class app_state:
    data_array          : list  # [data]
    settings            : settings 
    safe_state_data     : bool 

def push_to_data_array (app_state : app_state, name : str, amount : float, comment : str, date : str) -> None:
    d : data = data(name, amount, comment, date)
    if name == '' or amount == '' or comment == '':
        pass
    else:
        if app_state.data_array == []:
            app_state.data_array.append(d)
        else:
            state : bool = True
            for i in range(len(app_state.data_array)):
                if app_state.data_array[i].date <= date:
                    state = False
                    app_state.data_array.insert(i, d)
                    break
            if state:
                app_state.data_array.append(d)
    app_state.safe_state_data = False

def pop_from_data_array (app_state : app_state, name : str, amount : float, comment : str, date : str) -> None:
    d = data(name, amount, comment, date)
    for i in range(len(app_state.data_array)):
        if app_state.data_array[i] == d:
            app_state.safe_state_data = False
            return app_state.data_array.pop(i)
    return None

def find_names (app : app_state):
    names = []
    for data in app.data_array:
        name : str = data.person_name
        if name not in names and f"{app.settings.jear}.{app.settings.month}" in data.date:
            names += [name]
        elif name not in names and app.settings.month == 'all':
            names += [name]
    return names
