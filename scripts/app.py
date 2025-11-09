import streamlit as st
from datetime import datetime
import fastf1

# modules
from fetch_data import load_session
import fastest_lap_comparison
import final_ranking
import tyre_analysis


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
st.title("🏎️ F1 Race Analysis Dashboard")

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

        st.success("GP Data successfully loaded!")

        st.header("Qualifying Session")
        fastest_lap_comparison.get_all_drivers_fastest_lap(quali_session)
        fastest_lap_comparison.calculate_drivers_delta_time_compared_to_pole(quali_session)
        fig1 = fastest_lap_comparison.plot_the_final_time_ranking(quali_session)
        st.pyplot(fig1)

        st.header("Final Race Ranking")
        fig2 = final_ranking.plot_the_final_ranking(race_session)
        st.pyplot(fig2)

        st.header("Tyre Analysis During Race")
        fig3 = tyre_analysis.plot_sessions_tyre_compounds_and_stints(race_session)
        st.pyplot(fig3) # to print the plot

        st.success("Analysis completed!")

    except Exception as e:
        st.error(f" Error: {e}")
