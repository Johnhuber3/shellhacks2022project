import pandas as pd;
import matplotlib.pyplot as plt;
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import numpy as np;


# read full group csv
fullGroup = pd.read_csv('./data/full_grouped.csv');

# condense Dataframe to Date, Country, Confirmed Cases
condensed = pd.DataFrame(fullGroup, columns=['Date', 'Country/Region', 'Confirmed']);
G19 = ['Argentina', 'Australia', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Italy', 'Japan', 'South Korea', 'Mexico', 'Russia', 'Saudi Arabia', 'South Africa', 'Turkey', 'United Kingdom', 'US']

# format y-axis to shorthand
def numericalTickFormatter(number):
    if number < 10**3:
        return number;
    elif number < 10**6:
        return f"{round(number/(10**3), 2)}K";
    else:
        return f"{round(number/(10**6), 2)}M";

# function makes animated graph
def makeVideoGraph():

    for country in G19:
        
        # initialize the plot figure with a specific country
        fig = plt.figure();
        specificCountry = [country];
        specificCountryDataFrame = pd.DataFrame(condensed.loc[condensed['Country/Region'].isin(specificCountry)])
        
        countryName = country;
        
        # store all dates for country
        dates = [];
        
        # format the dates to values from january 22
        for i in range(22, 209):
            if i >= 22 and i <= 31:
                dates.append('2020-01-' + str(i));
            elif i >= 32 and i <= 40:
                dates.append('2020-02-0' + str(i-31));
            elif i >= 41 and i <= 60:
                dates.append('2020-02-' + str(i-31));
            elif i >= 61 and i <= 69:
                dates.append('2020-03-0' + str(i-60));
            elif i >= 70 and i <= 91:
                dates.append('2020-03-' + str(i-60));
            elif i >= 92 and i <= 100:
                dates.append('2020-04-0' + str(i-91));
            elif i >= 101 and i <= 121:
                dates.append('2020-04-' + str(i-91));
            elif i >= 122 and i <= 130:
                dates.append('2020-05-0' + str(i-121));
            elif i >= 131 and i <= 152:
                dates.append('2020-05-' + str(i-121));
            elif i >= 153 and i <= 161:
                dates.append('2020-06-0' + str(i-152));
            elif i >= 162 and i <= 182:
                dates.append('2020-06-' + str(i-152));
            elif i >= 183 and i <= 191:
                dates.append('2020-07-0' + str(i-182));
            elif i >= 192 and i <= 209:
                dates.append('2020-07-' + str(i-182));
        
        # create dataframe that is filtered for dates included in the dates array  
        datefilter = pd.DataFrame(specificCountryDataFrame.loc[specificCountryDataFrame['Date'].isin(dates)]);
        
        # use datefilter dataframe and create numpy array from 'Confirmed' values
        confirmed = datefilter['Confirmed'].to_numpy();
        
        # create a numpy array from day 1 to 188
        days = np.arange(start=1, stop=188, step=1);
        
        # set the tick steps and font size of x-axis
        plt.xticks(np.arange(start=1, stop=188, step=20), fontsize=7);
        
        # set font size of y-ticks
        plt.yticks(fontsize=7)
        
        # set style of figure
        plt.style.use('ggplot');
        
        # function animates the graph
        def animate(i):
            
            # clear the figure
            plt.clf();
            
            # set the labels for figure
            plt.xlabel('Days Since January 22', fontsize=7);
            plt.ylabel('Confirmed Cases', fontsize=7);
            plt.title(f"{ countryName } Confirmed Cases")
            
            # plot the graph
            plt.plot(days[:i], confirmed[:i]) 
            plt.gca().set_yticklabels([ numericalTickFormatter(number) for number in plt.gca().get_yticks() ]);
        
        # call the animate function
        animator = animation.FuncAnimation(fig, animate, frames=182 ,interval=35, repeat=False);
        
        # save the animation to mp4
        writervideo = animation.FFMpegWriter(fps=10)
        animator.save('./videoGraphs/' + countryName +'.mp4', writer=writervideo);
        print('Done ' + str(countryName));
    
# function creates a static graph
def makeStaticGraph():
    
    # Create graph for each G19 country
    for country in G19:
        fig = plt.figure();
        plt.style.use('ggplot')
        specificCountry = [country];
        
        # create dataframe for specific country
        specificCountryDataFrame = pd.DataFrame(condensed.loc[condensed['Country/Region'].isin(specificCountry)]);

        countryName = country;

        dates = [];

        # assigning dates to specific day since pandemic started (jan 22 - july 27)
        for i in range(22, 209):
            if i >= 22 and i <= 31:
                dates.append('2020-01-' + str(i));
            elif i >= 32 and i <= 40:
                dates.append('2020-02-0' + str(i-31));
            elif i >= 41 and i <= 60:
                dates.append('2020-02-' + str(i-31));
            elif i >= 61 and i <= 69:
                dates.append('2020-03-0' + str(i-60));
            elif i >= 70 and i <= 91:
                dates.append('2020-03-' + str(i-60));
            elif i >= 92 and i <= 100:
                dates.append('2020-04-0' + str(i-91));
            elif i >= 101 and i <= 121:
                dates.append('2020-04-' + str(i-91));
            elif i >= 122 and i <= 130:
                dates.append('2020-05-0' + str(i-121));
            elif i >= 131 and i <= 152:
                dates.append('2020-05-' + str(i-121));
            elif i >= 153 and i <= 161:
                dates.append('2020-06-0' + str(i-152));
            elif i >= 162 and i <= 182:
                dates.append('2020-06-' + str(i-152));
            elif i >= 183 and i <= 191:
                dates.append('2020-07-0' + str(i-182));
            elif i >= 192 and i <= 209:
                dates.append('2020-07-' + str(i-182));

        datefilter = pd.DataFrame(specificCountryDataFrame.loc[specificCountryDataFrame['Date'].isin(dates)]);

        # make a numpy array from datefilter dataframe using only the 'Confirmed' column
        confirmed = datefilter['Confirmed'].to_numpy();
        
        # set labels for figure
        plt.xlabel('Number of Days');
        plt.ylabel('Confirmed Cases');
        plt.title(country);
        
        # make numpy array from day 1 to day 188
        days = np.arange(start=1, stop=188, step=1)
        plt.xticks(np.arange(start=1, stop=188, step=20))
        
        # plot figure
        plt.plot(days, confirmed);  
        plt.gca().set_yticklabels([ numericalTickFormatter(number) for number in plt.gca().get_yticks() ]);
        
        # save figure as a png
        fig.savefig('./staticGraphs/' + countryName +'.png', bbox_inches='tight');
        print('Done ' + str(countryName))
        fig.clf()


fileType = input('png or mp4');
if fileType == 'png':
    makeStaticGraph();
elif fileType == 'mp4':
    makeVideoGraph();