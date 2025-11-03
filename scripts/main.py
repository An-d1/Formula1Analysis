from fetch_data import load_session
import fastest_lap_comparison 
import final_ranking
import tyre_analysis

import fastf1

year = 2020
gp = "Russia"
session_type_for_quali = "Q"
session_type_for_race = "R"


# Quali plot starts here / But these methods can also be used to compare all the drivers fastest lap
quali_session = load_session(year, gp, session_type_for_quali)

fastest_lap_comparison.get_all_drivers_fastest_lap(quali_session)
fastest_lap_comparison.calculate_drivers_delta_time_compared_to_pole(quali_session)
fastest_lap_comparison.plot_the_final_time_ranking(quali_session)

# Final Ranking
race_session = load_session(year, gp, session_type_for_race)
final_ranking.plot_the_final_ranking(race_session)

# tyre analysis during the race
tyre_analysis.plot_sessions_tyre_compounds_and_stints(race_session)
