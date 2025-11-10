import streamlit as st
from datetime import datetime
import fastf1

# modules
from fetch_data import load_session
import fastest_lap_comparison
import final_ranking
import tyre_analysis
import top2_drivers_best_laps_comparison


# enable FastF1 cache
fastf1.Cache.enable_cache("external_data/fastf1")

@st.cache_data
def get_gp_names_for_year(year: int):
    #Return a list of all Grand Prix names available for the given year.
    try:
        schedule = fastf1.get_event_schedule(year, include_testing=False)
        return sorted(schedule['EventName'].dropna().unique().tolist())
    except Exception as e:
        st.warning(f" Could not fetch schedule for {year}: {e}")
        return []

# --- streamlit UI ---
st.set_page_config(page_title="F1 Race Analysis", page_icon="🏁")
st.title("F1 Race Analysis Dashboard")

# current year for upper bound
current_year = datetime.now().year

selected_year = st.number_input(
    "Enter the year",
    min_value=1950,
    max_value=current_year,
    value=current_year,
    step=1
)

# Load GP names only for the selected year
gp_list = get_gp_names_for_year(selected_year)

if not gp_list:
    st.error("No Grand Prix data found for this year.")
else:
    selected_gp = st.selectbox("Select a Grand Prix", gp_list)

if st.button("Start Race Analysis"):
    try:
        with st.spinner(f"Loading sessions for {selected_gp} {int(selected_year)}...", show_time=True):
            # load sessions
            quali_session = load_session(selected_year, selected_gp, "Q")
            race_session = load_session(selected_year, selected_gp, "R")

        st.success("Geand Prix Data successfully loaded!")

        st.header("Qualifying Session")
        fastest_driver, fig1 = fastest_lap_comparison.plot_the_final_time_ranking(quali_session)

        st.subheader(f"- Delta times of each driver compared to {fastest_driver}, the fastest driver")

        st.pyplot(fig1) # to print the plot

        st.markdown(f"""
        * This plot clearly shows how much 'slower' every driver was compared to **{fastest_driver}** during qualifying session. 
        """)

        st.header("Final Race Ranking")
        fig2 = final_ranking.plot_the_final_ranking(race_session)
        st.pyplot(fig2)

        st.header("Tyre Analysis During Race")
        
        st.subheader("Analysis: ")
        st.markdown("""
        This plot shows the lap time, tyre distribution for each driver. 

        * **Key Insight:** It shows how different tyre compounds affected each drivers lap times.
        * It also helps to notice the average tire life-time.   
        """)

        fig3 = tyre_analysis.plot_sessions_tyre_compounds_and_stints(race_session)
        st.pyplot(fig3) 

        fig31, fastest_driver_name = tyre_analysis.plot_sessions_tyre_choices_using_seaborn(race_session)
        st.pyplot(fig31)

        st.markdown(f"""
        This plot shows the tyre choice and laptime for each lap for all drivers. 

        * **Key Insight:** It shows how different tyre compounds affected each drivers lap times.
        * One key takeaway is that we can clearly tell **{fastest_driver_name}** was the fastest driver during the race    
        """)

        st.caption("Data shown for all laps.")

        st.header("Fastest Lap Comparison Between the Two Quickest Drivers")
        the_fastest_of_two, the_second_driver, fig4 = top2_drivers_best_laps_comparison.plot_2_fastest_laps_comparison_side_by_side(race_session)
        st.pyplot(fig4)

        st.markdown(f"""

        * **Legend:** The vertical dotted lines mark the turns 
        * **Key Isights:** This plot helps us realize where **{the_fastest_of_two}** gained the advantage over **{the_second_driver}**
        * The most important parts to focus are the breaking points, and at which point the drivers picked up their speed. This helps us to realize the small differences in their lap-time.
        """)
        st.success("Analysis completed!")

    except Exception as e:
        st.error(f" Error: {e}")