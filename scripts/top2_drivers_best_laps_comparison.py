import fastf1
import matplotlib.pyplot as plt

def prepare_driver_data_for_plotting(session):
    laps_clean = session.laps[session.laps['LapTime'].notna()]

    # gets only the data the 2 fastest driverss to later fetch their data 
    top2 = (laps_clean.groupby('Driver')['LapTime']
                    .min()
                    .sort_values()
                    .head(2))
    drivers = list(top2.index)  

    # prepare the dictionary for both drivers
    driver_data = {}
    vmins, vmaxs = [], [] #used for plot range of the minspeed and max speed

    for drv in drivers:
        lap = session.laps.pick_driver(drv).pick_fastest()
        car = lap.get_car_data().add_distance() #get car data and the distance
        color = fastf1.plotting.get_team_color(lap['Team'], session=session) 
        label = f"{drv}  ({str(lap['LapTime']).split()[-1]})"
        driver_data[drv] = {'car': car, 'color': color, 'label': label}
        vmins.append(car['Speed'].min())
        vmaxs.append(car['Speed'].max())

    the_fastest_of_two = session.results.loc[
    session.results['Abbreviation'] == drivers[0], 'FullName'
    ].iloc[0]

    the_second_driver = session.results.loc[
    session.results['Abbreviation'] == drivers[1], 'FullName'
    ].iloc[0]


    return (the_fastest_of_two, the_second_driver, driver_data, vmins, vmaxs)
    
def plot_2_fastest_laps_comparison_side_by_side(session):
    the_fastest_of_two, the_second_driver, driver_data, vmins, vmaxs = prepare_driver_data_for_plotting(session=session)

    # Corner info
    circuit_info = session.get_circuit_info()

    # plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # plot both lines
    for drv, info in driver_data.items():
        car = info['car']
        ax.plot(car['Distance'], car['Speed'],
                color=info['color'], linewidth=1.8, label=info['label'])

    # Vertical dotted lines for corners
    v_min = min(vmins)
    v_max = max(vmaxs)
    ax.vlines(x=circuit_info.corners['Distance'],
            ymin=v_min-20, ymax=v_max+20,
            linestyles='dotted', colors='grey')


    # Labels, legend, limits
    ax.set_xlabel('Distance along track (m)')
    ax.set_ylabel('Speed in km/h')
    ax.legend(title='Driver (best lap)')
    ax.set_ylim([v_min - 40, v_max + 20])

    return (the_fastest_of_two, the_second_driver, fig)