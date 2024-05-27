import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
    index_col=[0],
    parse_dates=[0],
)

# Clean data
# clean quantiles top and bottom .025
quantile = 0.025
lower = df['value'].quantile(quantile)
higher = df['value'].quantile(1 - quantile)
lower_mask = df['value'] > lower
higher_mask = df['value'] < higher
df = df[lower_mask & higher_mask]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14,4))
    ax.plot(df, 'r', linewidth=1)
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'Months'], as_index=False).mean()
    df_bar = df_bar.sort_values(['year', 'Months'], ascending=True)
    
    # Draw bar plot
    plt.clf()
    fig, ax = plt.subplots(figsize=(8,8))
    width = 0.04
    cur_offset = 5.5 * width
    all_years = df_bar['year'].unique()
    bars = []
    # for each month create appropriate 1d arrays with same shape
    for month in range(1,13):
        # get the same month at all years
        current_df = df_bar[df_bar['Months'] == month]
        means = current_df['value'].values.tolist()
        years = current_df['year'].values
        # if the month is missing in a given year, add zero as the mean for it
        # works only for "border" years - the first or last
        years_missing_month = set(all_years.tolist()) - set(years.tolist())
        if len(years_missing_month) != 0:
            for year in years_missing_month:
                if year > years.max():
                    means.append(0)
                elif year < years.min():
                    means.insert(0, 0)
        
        # two first args are arrays so it creates bars for
        # the month for all years 
        # appended to bar list in order to set legend - acts as a pointer
        bars.append(ax.bar(all_years - cur_offset, means, width))
        cur_offset -= width
    # customize lables and ticks
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    monthmap = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    ax.legend(bars, monthmap)
    ax.set_xticks(ticks=all_years) # get rid of decimal ticks
    ax.tick_params('x', labelrotation=90)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months = ['Jan','Feb','Mar','Apr','May','Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']
    plt.clf()
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(24,8))
    g = sns.boxplot(df_box, 
                x='month',
                y='value',
                hue='month',
                order=months,
                ax=ax2)
    g.set_xlabel('Month')
    g.set_ylabel('Page Views')
    g.set_title('Month-wise Box Plot (Seasonality)')

    g1 = sns.boxplot(df_box,
                     x='year',
                     y='value',
                     hue='year',
                     ax=ax1,
                     legend=False,
                    palette=sns.color_palette(n_colors=4))
    g1.set_xlabel('Year')
    g1.set_ylabel('Page Views')
    g1.set_title('Year-wise Box Plot (Trend)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
