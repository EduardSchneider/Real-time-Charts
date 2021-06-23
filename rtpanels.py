import panel as pn

'''
This python file is intended for use alongside the realtimecharts module.
This file is used to create and load panels of the realtimecharts Dashboard.
Each function in this file is added to a  list of  functions below.

The functions below use plotting functions already imported by realtimecharts.
Want to add plotting modules? Import them at the top of this file.

Want to create your own panel? Add a new function below that creates a new panel.

PANEL MAKE-UP
The panel is created using the panel module. Check the documentation of Holoviews panels to learn more about creating panels.
As long as the returned panel is a functional panel, it will work within realtimecharts. Test this in an isolated instance to see if your function returns a panel.
The input of each function needs to be a connection. This is a Connection instance that is stored within Dashboard during the initialization.

Finally, the functions below need to return a tuple:
The first object in the tuple must be a string. This string represents the title of the panel added to the dashboard.
The second object is the panel object itself that is created within the function.
'''

def get_index(dashboard):
    
    return len(dashboard.panels)


def create_variables_panel(dashboard):

    connection = dashboard.connection

    text = ''
    i = 1

    for variable in connection.variables:
        text += f'variable {i}: {variable} \n'
        i += 1

    variable_panel = pn.Column()
    variable_panel.append(connection.df)
    variable_panel.append(pn.pane.Markdown(text))

    return ('Variables', variable_panel)


def create_lineplot_panel(dashboard):

    connection = dashboard.connection

    lineplot_panel = pn.Column()

    for variable in connection.variables:
        plot = pn.Pane(connection.df.hvplot.line(y=variable, backlog=1000))
        lineplot_panel.append(plot)

    return ('Line plot', lineplot_panel)


def create_scatterplot_panel(dashboard):

    index = get_index(dashboard)

    connection = dashboard.connection

    scatterplot_panel = pn.Column()

    x = pn.widgets.Select(name='x-axis', options = connection.variables)
    y = pn.widgets.Select(name='y-axis', options = connection.variables)

    plot_button = pn.widgets.Button(name='add plot', button_type='primary')
    
    # plot_button.on_click(on_click_scatterplot(connection, x.value, y.value))
    
    # scatterplot_panel.append(pn.Row(x, y, plot_button))

    for i in range(len(connection.variables)):

        for j in range(i+1, len(connection.variables)):

            plot = connection.df.hvplot.scatter(y=connection.variables[i], x=connection.variables[j], backlog=1000)
            scatterplot_panel.append(plot)

    return ('Scatter plot', scatterplot_panel)


def create_violinplot_panel(dashboard):

    connection = dashboard.connection
    
    violin_panel = pn.Column(pn.Pane(connection.df.hvplot.violin(connection.variables, backlog=1000)))

    return ('Violin plot', violin_panel)

def create_historical_histogram_panel(dashboard):
    
    connection = dashboard.connection
    
    hist_panel = pn.Column()
    
    for i in range(len(connection.variables)):

        plot = connection.historical_dataframe.hvplot.hist(y=connection.variables[i])
        hist_panel.append(plot)
        
    return ('Historical histogram', hist_panel)

# *-------------------------------------------------------------------------------------------------------*

def on_click_scatterplot(connection, x, y):
    print('hello')
    plot = connection.df.hvplot.scatter(y=y, x=x, backlog=1000)
    return plot

def on_click_scatterplot2(dashboard, x, y, index):
    print('yo')
    plot = connection.df.hvplot.scatter(y=y, x=x, backlog=1000)
    scatterplot_panel.append(pn.Pane(plot))
    
# *-------------------------------------------------------------------------------------------------------*

# add your created function in the list below to load it as part of the Dashboard initialization

basic_panels = [
    create_lineplot_panel,
    create_scatterplot_panel,
    create_violinplot_panel
]

panel_functions = [    
    ('Variable panel', create_variables_panel),
    ('Lineplot panel', create_lineplot_panel),
    ('Scatterplot panel', create_scatterplot_panel),
    ('Violinplot panel', create_violinplot_panel),
    ('Historical scatter panel', create_historical_histogram_panel)
]

