from setuptools import setup, find_packages

# Setup configuration for the tool
setup(
    name='Real-time Charts',
    version='0.2',
    long_description="Real-time Charts creates a dashboard of real-time charts using a user-defined connector type. This program is useful for setting up charts and exploring auto-updating data quickly on a server.",
    packages=find_packages(),
    license_files=('LICENSE.txt',),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'hvplot', # For creating plots
        'holoviews', # Dependency
        'panel', # For creating dashboard
        'requests', # For connecting to external servers
        'param', # For creating parameters within dashboards
        'streamz' # For creating a periodically updating dataframe
    ]
)