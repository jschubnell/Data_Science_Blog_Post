'''
This module contains helper functions to transform and clean Airbnb's Seattle Dataset
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer


def clean_calendar(df):
    '''
    A function to clean and set the calendar ready for comparissons
    
    Parameters:
    df (pandas.Dataframe): A pandas dataframe containing airbnb's calendar data
    
    Returns:
    df (pandas.Dataframe): Cleaned dataframe
    '''
    
    df.date = pd.to_datetime(df.date, format='%Y-%m-%d')
    df.drop_duplicates(inplace=True)
    
    map_available = lambda value: 1 if value == "t" else 0
    df.available = df.available.apply(map_available)
    
    df = clean_price(df)
    
    return df

def clean_price(df):
    ''' Transform price column to integer representing the value in cents
    
    Parameter:
    df (pandas.Dataframe): Pandas dataframe containing a price column
    
    Return:
    df (pandas.Dataframe): Pandas dataframe with the price column representing the cents value in integer
    '''
    
    df.price = df.price.fillna(0)
    
    strip_price = lambda value: value.lstrip('$').replace(',','').replace('.', '') if type(value) == str else value
    
    df.price = df.price.apply(strip_price)
    df.price = df.price.astype('int')
    
    return df

def check_date_range(df):
    ''' Check the starting and ending dates in a dataframe
    
    Parameter:
    df (pandas.Dataframe): A dataframe with columns: [listing_id, date, available, price]       
    '''
    starting_dates = df.groupby('listing_id', axis=0).min().date
    finishing_dates = df.groupby('listing_id', axis=0).max().date
    distinct_starting_dates = set(starting_dates)
    distinct_finishing_dates = set(finishing_dates)
    if len(distinct_starting_dates) == 1 and len(distinct_finishing_dates) == 1:
        begin = distinct_starting_dates.pop().strftime('%Y-%m-%d')
        end = distinct_finishing_dates.pop().strftime('%Y-%m-%d')
        print(f"All listings begin at {begin} and end at {end}")
    else:
        print("The listings doesn't have equivalent starting or finishing dates.")
        print(f"Starting dates: {distinct_starting_dates}")
        print(f"Finishing dates: {distinct_finishing_dates}")
        
def plot_availability(df, city, startingDate=None, finishingDate=None, freq='W', savePlot=False):
    ''' Plot the distribution of listings available in a dataframe
    
    Parameter:
    df (pandas.Dataframe): A dataframe with columns: [listing_id, date, available, price]
    city (str): The city name from the dataframe
    startingDate (str): Starting day from week with format "YYYY-MM-DD"
    finishingDate (str): Finishing day from week with format "YYYY-MM-DD"
    freq (str): Frequency indiciating the aggregation in time.
                'D' for daily frequency, W' for weekly frequency, 'M' for monthly frequency.
                Ref: (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases)
    savePlot (boolean): If True will save the plot with city name and frequency, e.g: city_freq.png
    
    '''
    mpl.style.use('seaborn')
    title_dict = {'D': 'Daily',
                  'W': 'Weekly',
                  'M': 'Monthly'}
    plt.rcParams['figure.figsize'] = [18, 9]
    # Grouping by frequency to count number of listings
    weekly_count = df[df.available == 1].groupby(pd.Grouper(key='date', freq=freq)).count().listing_id
    if freq == 'M':
        weekly_count.index = weekly_count.index.strftime('%b/%Y')
    else:
        weekly_count.index = weekly_count.index.strftime('%Y-%m-%d')
    if startingDate and finishingDate:
        weekly_count.loc[startingDate: finishingDate].plot(kind='bar', color='steelblue')
    else:
        weekly_count.plot(kind='bar', color='steelblue')
    plt.title(f'Available Listings in {city} ({title_dict[freq]})', fontsize=16)
    plt.xlabel(f'Period ({title_dict[freq]})', fontsize=12)
    plt.ylabel(f'Available Listings', fontsize=12)
    plt.xticks(fontsize=12, rotation=45, ha='right')
    plt.yticks(fontsize=12)
    if savePlot:
        plt.savefig(f'./graphs/barplot_availability_{city}_{freq}.png', bbox_inches='tight');
    
def plot_avarage_price(df, city, startingDate=None, finishingDate=None, neighbourhood=None, freq='W', err=False):
    ''' Plot the weekly distribution of avarage prices in a dataframe
    
    Parameter:
    df (pandas.Dataframe): A dataframe with columns: [listing_id, date, available, price, neighbourhood]
    city (str): The city name from the dataframe
    startingDate (str): Starting day from week with format "YYYY-MM-DD"
    finishingDate (str): Finishing day from week with format "YYYY-MM-DD"
    neighbourhood (str): String with the neighbourhood's name
    freq (str): Frequency indiciating the aggregation in time 
                'D' for daily frequency, W' for weekly frequency, 'M' for monthly frequency.
                Ref: (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases)
    err (bool): Plot error indicators (standard deviation)
    
    '''
    mpl.style.use('seaborn')
    plt.rcParams['figure.figsize'] = [18, 9]
    title_dict = {'D': 'Daily',
                  'W': 'Weekly',
                  'M': 'Monthly'}
    if neighbourhood:
        df = df[df.neighbourhood_cleansed == neighbourhood]
    weekly_mean = df.groupby(pd.Grouper(key='date', freq=freq)).mean().price/100
    weekly_mean.index = weekly_mean.index.strftime('%Y-%m-%d')
    if err:
        weekly_std = df.groupby(pd.Grouper(key='date', freq=freq)).std().price/100
        weekly_std.index = weekly_std.index.strftime('%Y-%m-%d')
    else:
        weekly_std = 0
    if startingDate and finishingDate:
        weekly_mean.loc[startingDate: finishingDate].plot(kind='bar', yerr=weekly_std)
    else:
        weekly_mean.plot(kind='bar', yerr=weekly_std)
    plt.title(f'Avarage of Listing Price ({title_dict[freq]}) in {city}', fontsize=16)
    plt.xlabel(f'Period ({title_dict[freq]})', fontsize=12)
    plt.ylabel(f'Average Price', fontsize=12)
    plt.xticks(fontsize=12, rotation=45, ha='right')
    plt.yticks(fontsize=12);
    
def facetplot_neighbourhoods(df, savePlot=False):
    ''' Plot the neighbourhoods availability at a facetplot
    
    Parameter:
        df (pd.DataFrame): Dataframe with the following columns (date, neigbourhoods, count of listing)
        savePlot (boolean): Save the plot
    
    '''

    # Create a grid
    g = sns.FacetGrid(df, col='neighbourhood_group_cleansed', hue='neighbourhood_group_cleansed', col_wrap=5,
                      size=3, aspect=1.2)

    # Set log scale for y-axis
    g = g.set(yscale='log')

    # Rotate xtick labels
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(60)


    # Add the line over the area with the plot function
    g = g.map(plt.plot, 'date', 'listing_id')

    # Rename y label
    g = g.set_ylabels('Available Listings')
    
    # Rename x label
    g = g.set_xlabels('Dates')

    # Control the title of each facet
    g = g.set_titles("{col_name}")

    # Add a title for the whole plot
    plt.subplots_adjust(top=0.92)
    g = g.fig.suptitle('Neighbourhood Availability')

    # Save the graph
    if savePlot:
        plt.savefig(f'./graphs/facetplot.png', bbox_inches='tight');
    
    # Show the graph
    plt.show()
    
def one_hot_encode_amenities(df):
    ''' This function will separate the amenities for each datapoint into columns.
    
    Parameter:
    df (pandas.Dataframe): Dataframe containing a column called amenities. Each cell in the column contains
    a string representation of the set of amenities.
    
    Returns:
    amenities_df (pandas.Dataframe): Dataframe in which each row represents the original datapoint and the columns indicate
    which amenities that datapoint has.
    
    '''
    # Parsing the strings in each row for a list of amenities
    df = df['amenities'].apply(lambda amenities: amenities.strip('{}').replace('"', '').split(','))
    # One-hot encoding the amenities
    mlb = MultiLabelBinarizer()
    amenities = mlb.fit_transform(df)
    # Generating DataFrame
    amenities_df = pd.DataFrame(data=amenities, columns=mlb.classes_)
    # Droping first empty column
    amenities_df = amenities_df.iloc[:, 1:]
    
    return amenities_df