import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import json

def parse_html(html_file):
    data_list = [[]]
    with open(html_file, 'r') as file:
            read = csv.reader(file)
            row_n = 0
            c = 0
            for row in read:
                if ("row" in str(row)):
                    if (c >=2 or row_n > 0):
                        index = str(row).find("row")
                        if index != -1:
                            new_string = str(row)[index:]
                            new_string = new_string.replace("]", " ").replace(",", " ").replace("\"", " ").replace("'", " ").replace("<", " ").replace(">"," ").replace("/td","").replace("/th","")
                        if ("row"+str(row_n) in new_string):
                            new_string = new_string.replace("row"+str(row_n), "").replace(" ", "")
                            new_string = new_string.replace("fluxtime", " ").replace("fluxjulian", " ").replace("fluxcarrington", " ").replace("fluxobs", " ").replace("fluxadj", " ").replace("fluxursi", " ")

                            data_list[row_n].append(new_string.replace("row"+str(row_n), "").replace(" ", ""))
                    c+=1
                    if (row_n == 0 and c > 9) or (row_n > 0 and c == 7):
                        data_list.append([])
                        row_n+=1
                        c = 0
                
            #index using data_list[row][column] - fluxdate, fluxtime, fluxjulian, fluxcarrington, fluxobs, fluxadj, fluxursi

def IQR(data):
    # Calculate IQR
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    #print("IQR:", iqr)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    valid_data = [x for x in data if x >= lower_bound and x <= upper_bound]
    # Calculate average of validated data
    avg = np.mean(valid_data)
    #print("Average:", avg)

    return avg

def plot_1_day(times, values, avg):
    
    # Plot baseline and today's entries
    plt.title("Solar Flux (SFU) - [2023-10-07]")
    plt.plot(times, values, 'bo', label="Today's Entries")
    plt.plot(times, values, 'b-', label="Todays Flux")
    
    # Set y-axis scale
    if float(max(values)) > 200:
        plt.ylim([100, max(values)+50])
    else:
        plt.ylim([100, 201])
    
    #plot todays values line
    for i in range(len(times)-1):
        plt.plot([times[i], times[i+1]], [values[i], values[i+1]], 'b-')
    #plot average line
    plt.axhline(y=avg, color='g', linestyle='--', label="Average Flux")
    # Plot high flux line
    plt.axhline(y=200, color='r', linestyle='--', label="High Flux")
    
    plt.legend()
    plt.show()

def plot_10_day(times, values, avg):
    plt.title("Solar Flux (SFU) - 10 Day")
    plt.plot(times, values, 'bo', label="Today's Entries")
    plt.plot(times, values, 'b-', label="Todays Flux")
    
    # Set y-axis scale
    if float(max(values)) > 200:
        plt.ylim([100, max(values)+50])
    else:
        plt.ylim([100, 201])
    
    #plot 10 day values line
    for i in range(len(values)-1):
        plt.plot([times[i], times[i+1]], [values[i], values[i+1]],'b-')
    #plot average line
    plt.axhline(y=avg, color='g', linestyle='--', label="Average Flux")
    # Plot high flux line
    plt.axhline(y=200, color='r', linestyle='--', label="High Flux")
    
    plt.xticks(times, rotation=45)
    
    plt.legend()
    plt.show()

def FluxProcessing():
    # Flux is important for us to measure because it is a measure of the sun's activity and can be used to predict solar flares. 
    # in times of high flux, we can expect to see more solar flares and have to be careful with our satellites. Solar flares can 
    # damage satellites and cause them to malfunction leading to a loss of data, or even a loss of the satellite itself.

    #USE ALTITUDE OF SATELLITE TO CALCULATE FLUX. URSI FOR IONOSPHERIC FLUX (ISS LEVELS), OBSERVED FOR LEO SATELLITE FLUX
    
    cwd = os.getcwd()
    full_cwd = cwd+'\milkywaycoders\src\data\SolarFlux.csv'

    html_file = cwd+'\milkywaycoders\src\data\Daily flux values.html'
    
    #parse_html(html_file)  #To use if we take straight from the website

    today = datetime.date.today()
    #date = today.strftime("%Y-%m-%d")
    date = "2023-10-07"
    todays_times = []
    todays_values = []
    ten_day_labels = []
    ten_day_values = []

    try:
        with open(full_cwd, 'r') as file:
            reader = csv.reader(file)
            data = []
            count = 0
            for row in reader:
                if count == 0:
                    count+=1
                else:
                    data.append(float(row[6]))
                    
                    count+=1
                    
                    dat = datetime.datetime.strptime(row[0], "%Y-%m-%d")
                    diff = datetime.datetime.today() - dat
                    if (diff.days <= 10):
                        ten_day_labels.append(row[0][5:])
                        ten_day_values.append(float(row[6]))
                
                #cant use active day because it is not updated every day
                if (str(row[0]) == str(date)):
                    todays_times.append(row[1])
                    
                    todays_values.append(float(row[6]))
 
            avg = IQR(data)

            plot_1_day(todays_times, todays_values, avg)
            plot_10_day(ten_day_labels, ten_day_values, avg)
            
    except IOError:
        print("Could not open file:", full_cwd)

FluxProcessing()

def filter_data(geomag_data, flux_values):
    mean_flux = np.mean(flux_values)
    std_flux = np.std(flux_values)
    threshold_flux = mean_flux + 2 * std_flux

    filtered_data = [point for point in geomag_data if point[0] <= threshold_flux]

    return filtered_data

def geomag_plot(filtered_data, clr):
    # Plot data
    #for plt.plot(geomag_data[2], geomag_data[0], -o)
    x = [point[2] for point in filtered_data]
    y = [point[0] for point in filtered_data]
    plt.scatter(x, y, s=0.05, color=clr, alpha=0.7)

    # Plot line of best fit
    z = np.polyfit(range(len(y)), y, 20)
    p = np.poly1d(z)
    plt.plot(x, p(range(len(y))), color=clr, linestyle='-', linewidth=2)

    #plot average line
    avg = p(len(y)/2)
    plt.axhline(y=avg, color=clr, linestyle='--', linewidth=1)
    #plt.text(x[0], avg, "{:.2f} MeV".format(avg), color='black', size=10)

    plt.legend(['Points (≤50 MeV)', '    Best Fit','    Average', 'Points (≤100 MeV)','    Best Fit','    Average', 'Points (≥100 MeV)','    Best Fit','    Average'], fontsize=6)



def GeomagProcessing():
    #https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json

    # Open JSON file and load data
    with open(os.getcwd()+'\milkywaycoders\src\data\GOES_proton_data.json', 'r') as file:
        data = json.load(file)

    # Create lists to store data
    geomag50_data = []
    geomag100_data = []
    geomag100_plus_data = []

    # Access data from JSON object
    date = "2023-10-07"
    for obj in data:
        if(obj['time_tag'][:10] == date):
            obj['energy'] = int(obj['energy'].replace(">=", "").replace(" MeV", ""))
            if (obj['energy'] <= 50):
                geomag50_data.append([obj['flux'], obj['energy'], obj['time_tag']])
            elif (obj['energy']  <= 100 and obj['energy'] > 50): 
                geomag100_data.append([obj['flux'], obj['energy'] , obj['time_tag']])
            else:
                geomag100_plus_data.append([obj['flux'], obj['energy'] , obj['time_tag']])

    # Calculate distribution of flux values
    flux_50_max_values = [point[0] for point in geomag50_data]
    flux_100_max_values = [point[0] for point in geomag100_data]
    flux_100_plus_values = [point[0] for point in geomag100_plus_data]
    
    # Filter data
    filtered_50 = filter_data(geomag50_data, flux_50_max_values)
    filtered_100 = filter_data(geomag100_data, flux_100_max_values)
    filtered_100p = filter_data(geomag100_plus_data, flux_100_plus_values)

    geomag_plot(filtered_50, 'g')
    geomag_plot(filtered_100, 'orange')
    geomag_plot(filtered_100p, 'red')


    plt.axhline(y=10, color='r', linestyle='--', label="High Flux")
    plt.title("GOES Proton Flux (2023-10-07)")
    plt.yscale('log')
    plt.ylim([0.1, 1])
    plt.xlabel('Time')
    plt.ylabel('Proton Flux')
    plt.gca().yaxis.set_major_locator(ticker.FixedLocator(np.concatenate((np.arange(0, 0.11, 0.01), np.arange(0.1, 1.1, 0.1)))))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))


    plt.show()

GeomagProcessing()

#Somethings using DSCOVR data
#Something using CER?
#USse map of earth / Van allen belt and plot sat location on it

#def RadiationProcessing(satx, saty):

#RadiationProcessing(0, 0)