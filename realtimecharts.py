import hvplot.pandas
import hvplot.streamz
import holoviews as hv
import pandas as pd
import requests
import param
import panel as pn
from streamz.dataframe import PeriodicDataFrame

import rtpanels
import rtconnectors

# Connection class for creating a connection to an external server
class Connection:

    def __init__(self):
        self.variables = []

    # Initialization function which creates an adress of the connection
    # Historical dataframe for saving changes as data comes in
    # Periodic df runs argument 1 every interval
    def generate_connection(self, interval='1s'):
        self.adress = input('Enter your online adress (default is HTTP): ')
        interval_user = input('How often, in seconds, would you like to pull data from the server (e.g. 1s = 1 second)')
        
        
        self.get_connector_function()
        self.historical_dataframe = pd.DataFrame()
        self.df = PeriodicDataFrame(self.data_to_timestamp, interval)
        self.create_variables

    # Connects to the server using the selected connector function
    # Adds each variable found in the returned value  from connector function
    def create_variables(self):
        df = rtconnectors.connector_functions[self.connector_config][1](self)

        for variable in df.columns:
            self.variables.append(variable)

    # Asks for which connector function the user wishes to use
    # If only 1 is found, the default HTTP connector is used
    def get_connector_function(self):
        if len(rtconnectors.connector_functions) == 1:
            print('Only 1 connector found')
            print(f'using {rtconnectors.connector_functions[0][0]}')
            self.connector_config = 0

        else:
            print('Found connector functions: ')
            i = 0
            for connector in rtconnectors.connector_functions:
                print(f'{i}: {connector[0]}')
                i += 1

            option = input('Enter number of function you would like to use: ')
            self.connector_config = int(option)

    # Changes gotten dataframe from connector function to indexed timestamp df
    # Has to be separate or Periodic df refuses to work
    def data_to_timestamp(self, **kwargs):
        df = rtconnectors.connector_functions[self.connector_config][1](self)

        df['time'] = [pd.Timestamp.now()]
        df = df.set_index('time')

        self.add_entry_to_historical_dataframe(df)

        return df

    # Adds  new row to historical memory df
    # Function is called every interval of Periodic df
    def add_entry_to_historical_dataframe(self, entry):
        self.historical_dataframe = self.historical_dataframe.append(entry)

#  Dashboard class with panels and connection
class Dashboard:

    def __init__(self):
        self.panels = pn.Tabs(closable=True)
        self.panel_names = []

    # Creates the connection and basic panels
    def initialize(self):
        self.create_connection()
        self.create_basic_panels()

    # Creates connection with adress and connector function
    def create_connection(self):
        self.connection = Connection()
        self.connection.generate_connection()
        self.connection.create_variables()

    # Returns the panels within Dashboard class
    def display(self):
        return self.panels

    # Saves dataframe to same folder
    def save_dataframe(self):
        self.connection.historical_dataframe.to_csv('historical_df.csv')

    # Creates basic panels on initialization
    def create_basic_panels(self):
        self.create_functions_panel()


        for panel in rtpanels.basic_panels:

            panel = panel(self)
            self.panel_names.append(panel[0])
            self.panels.append(panel)

    # Adds panel based on clicked button
    def add_panel(self, function, names):

        index = names.index(function)

        panel = rtpanels.panel_functions[index][1](self)
        
        self.panel_names.append(rtpanels.panel_functions[index][0])
        self.panels.append(panel)

    # Adds panel when called manually, dashboard.display() updates automatically
    def add_a_panel(self):

        print('Which panel would you like to add?:')
        i = 0 
        for function in rtpanels.panel_functions:
            print(f'{i}: {function[0]}')
            i += 1

        answer = int(input('enter index of desired panel: '))
        
        if answer > len(rtpanels.panel_functions):
            print('Not a valid option, quitting')

        self.panel_names.append(rtpanels.panel_functions[answer][0])
        self.panels.append(rtpanels.panel_functions[answer][1](self))
        
    def delete_panel(self):
        
        print('Which panel would you like to delete?:')
        i = 0
        for name in self.panel_names:
            print(f'{i}: {name}')
            i += 1
            
        answer = input('enter index of the panel you wish to delete: ')
        
        self.panel_names.pop(int(answer))
        self.panels.pop(int(answer))

    # Creates the function panel to launch functions in
    # Currently non-functioning
    def create_functions_panel(self):

        save_button = pn.widgets.Button(name='save dataframe', button_type='primary')
        save_button.on_click = self.save_dataframe()
        panel_names = []

        for panel in rtpanels.panel_functions:
            panel_names.append(panel[0])

        selectable_functions = pn.widgets.Select(name='Optional panels', options = panel_names)
        function_button = pn.widgets.Button(name='add panel', button_type='primary')

        function_button.on_click = self.add_panel(selectable_functions.value, panel_names)
        
        self.panel_names.append('Functions panel')
        self.panels.append(('Functions', pn.Column(save_button, pn.Row(selectable_functions, function_button))))
        
class MasterDashboard:
    
    def __init__(self):
        self.dashboards = []
        self.dashboard_names = []
        self.panels = pn.Tabs(closable=True)
        
    def add_dashboard(self):
        
        print('Creating dashboard...')
        print('Dashboard initializing')
        dashboard = Dashboard()
        dashboard.initialize()
        
        name = input('What name should the dashboard have?: ')
        self.dashboard_names.append(name)
        self.dashboards.append(dashboard)
        self.panels.append((name, dashboard.panels))
    
    def add_panel(self):
        
        print('For which dashboard would you like to add a panel?')
        i = 0
        for name in self.dashboards:
            print(f'{i}: {self.dashboard_names[i]}')
            i += 1
            
        dashboard_select = input('enter index of the dashboard you would like to add a panel to: ')
        self.dashboards[int(dashboard_select)].add_a_panel()

    def delete_dashboard(self):

        print('Which dashboard would you like to delete?:')
        i = 0
        for name in self.dashboards:
            print(f'{i}: {self.dashboard_names[i]}')
            i += 1

        answer = input('enter index of the dashboard you wish to delete: ')

        self.dashboard_names.pop(int(answer))
        self.dashboards.pop(int(answer))
        
    def delete_panel(self):

        print('From which dashboard would you like to delete a panel?:')
        i = 0
        for name in self.dashboards:
            print(f'{i}: {self.dashboard_names[i]}')
            i += 1

        answer = input('enter index of the dashboard you wish to delete a panel from: ')
        self.dashboards[int(answer)].delete_a_panel()
        self.dashboards[int(answer)].delete_a_panel()
        
    def initialize(self):
        self.add_dashboard()
        
    def display(self):
        return self.panels
