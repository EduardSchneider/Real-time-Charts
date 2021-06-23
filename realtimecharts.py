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

    def __init__(self, connector_config, address):
        self.connector_config = connector_config
        self.variables = []
        self.address = address

    # Initialization function which creates an address of the connection
    # Historical dataframe for saving changes as data comes in
    # Periodic df runs argument 1 every interval
    def generate_connection(self, interval='1s'):
        self.historical_dataframe = pd.DataFrame()
        self.df = PeriodicDataFrame(self.data_to_timestamp, interval)

    # Connects to the server using the selected connector function
    # Adds each variable found in the returned value  from connector function
    def create_variables(self):
        df = rtconnectors.connector_functions[self.connector_config][1](self)

        for variable in df.columns:
            self.variables.append(variable)

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
        self.panels = pn.Tabs()
        self.panel_names = []

    # Creates the connection and basic panels
    def initialize(self, address, index):
        self.create_connection(address, index)
        self.create_basic_panels()

    # Creates connection with address and connector function
    def create_connection(self, address, index):
        self.connection = Connection(index, address)
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

        for i in range(len(rtpanels.basic_panels)):

            panel = rtpanels.basic_panels[i](self)
            
            self.panel_names.append(panel[0])
            self.panels.append(panel)

    # Adds panel based on clicked button
    def add_panel(self, index):
        
        panel = rtpanels.panel_functions[index][1](self)
        print(panel)
        
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
        
    def delete_panel(self, panel_index):
                    
        self.panel_names.pop(panel_index)
        self.panels.pop(panel_index)

class MasterDashboard:
    
    def __init__(self):
        self.dashboards = []
        self.dashboard_names = []
        self.panels = pn.Tabs()
        
    def add_dashboard(self, name, address, index):
        
        dashboard = Dashboard()
        dashboard.initialize(address, index)
        
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

    def delete_dashboard(self, index):

        self.dashboard_names.pop(index)
        self.dashboards.pop(index)
        self.panels.pop(index)
        
    def delete_panel(self, dashboard_index, panel_index):
        print(dashboard_index, panel_index)
        self.dashboards[dashboard_index].delete_panel(panel_index)
        
    def display(self):
        return self.panels
