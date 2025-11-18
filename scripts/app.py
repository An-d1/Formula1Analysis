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

       # Qualifying
        st.header("Qualifying Session")
        fastest_driver, fig1 = fastest_lap_comparison.plot_the_final_time_ranking(quali_session)
        
        st.subheader(f"Gap to Pole Position ({fastest_driver})")
        st.pyplot(fig1)

        st.markdown(f"""
        **How to read this chart:**
        * **The Baseline:** The fastest driver ({fastest_driver}) is at 0.0s.
        * **The Gap:** The bars represent the time delta (in seconds) for every other driver relative to the pole position.
        * **Interpretation:** 
            * **A gradual slope** indicates a competitive field where car performance is close.
            * **Large jumps** between drivers often indicate different car performances, where some cars struggled in comparison to others.
        """)

        # Race Ranking
        st.header("Final Race Ranking")
        fig2 = final_ranking.plot_the_final_ranking(race_session)
        st.pyplot(fig2)
        
        st.markdown("""
        This chart visualizes the final finishing order. Comparing this against the qualifying results helps to identify drivers who had strong **race pace** (moved up) versus those who struggled with tyre management or incidents (dropped down).
        """)

        # Tyre Analysis
        st.header("Tyre Analysis During Race")

        fig3, fastest_driver_name = tyre_analysis.plot_sessions_tyre_choices_using_seaborn(race_session)
        
        st.subheader("Lap Time Distribution by Compound")
        st.pyplot(fig3)

        st.markdown(f"""
        **Performance Insights:**
        * **Vertical Spread:** A "tall" cluster of dots indicates high inconsistency or significant tyre degradation (laps getting slower over time). A "tight" cluster indicates consistent pace.
        * **Compound Pace:** Lower clusters represent faster compounds. 
        * **Benchmark:** We can also see that **{fastest_driver_name}**, set the overall fastest pace.
        """)

        st.subheader("Tyre Strategy & Stint History")
        st.markdown("""
        Tyre behavior dictates race strategy. The visualization below shows every driver's stint length and compound choice.
        """)

        fig31 = tyre_analysis.tyre_stint_distribution(race_session)
        st.pyplot(fig31)

        st.markdown(f"""
        **Strategic Takeaways:**
        * **Stint Count:** Many high bars suggest a high-degradation race requiring multiple stops.
        """) 
        st.caption("Data shown for all completed laps.")

        # Fastest lap telementry
        st.header("Fastest Lap Comparison")
        
        the_fastest_of_two, the_second_driver, fig4 = top2_drivers_best_laps_comparison.plot_2_fastest_laps_comparison_side_by_side(race_session)
        
        st.subheader(f"Head-to-Head: {the_fastest_of_two} vs {the_second_driver}")
        st.pyplot(fig4)
        
        st.markdown(f"""
        **How to read this telemetry trace:**
        
        1.  **The Track Map:** The **vertical dotted lines** indicate the corners (turns) on the circuit. The white space between these lines represents the straights.
        
        2.  **The Drivers:** This chart compares **{the_fastest_of_two}** and **{the_second_driver}**, who recorded the two single fastest laps of the race. 
            * *Note:* These are not necessarily the race leaders. A driver might be ranked lower but pitted late for fresh tyres to set a "qualifying style" lap.

        **Where was the time gained?**
        * **Braking Points:** Look at the line just before a vertical dotted line. If the curve drops *later* for one driver, it means they braked later, carrying speed deeper into the entry of the corner.
        * **Cornering Speed (Apex):** Look at the "valleys" (the lowest points at the dotted lines). A higher valley indicates a higher minimum speed through the middle of the corner.
        * **Traction (Exit):** Observe how steeply the line rises after the dotted line. A steeper slope means the driver was able to get back on full throttle earlier.
        """)
        
        st.success("Analysis completed!")
        
    except Exception as e:
        st.error(f" Error: {e}")