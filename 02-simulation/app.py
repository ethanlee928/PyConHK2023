from time import time

import pandas as pd
from pyfmc.simulations.gbm import GBM

import streamlit as st

st.set_page_config(page_title="Monte-Carlo Simulation", page_icon="💹")


with st.container():
    st.header("PyTorch Accelerated Monte-Carlo Simulation")
    st.subheader("Geometric Brownian motion (GBM)")
    st.latex(
        r"""
        \frac{\Delta S}{S}=\mu\Delta t + \sigma\epsilon\sqrt{\Delta t}
        """
    )
    st.write(
        "where S is stock price, µ is the expected return, σ is the standard deviation of returns, ε is the random variable."
    )

with st.container():
    with st.form("parameters"):
        st.subheader("Configure Simulation")
        n_walkers = st.number_input(label="Number of random walkers", value=int(1e6), min_value=1, max_value=int(1e10))
        n_steps = st.number_input(label="Number of steps to simulate", value=100, min_value=1, max_value=1000)
        n_traj = st.number_input(label="Number of trajectories to plot", value=50, min_value=1, max_value=1000)
        perc_var = st.slider("% Value at Risk", min_value=70, max_value=99, step=1, value=95)
        device_acc = st.toggle("Device Accelerated (use CUDA / MPS)")
        data_file = st.file_uploader(label="Data file", type=["csv"], accept_multiple_files=False)
        show_df = st.form_submit_button(label="Show DataFrame")
        if data_file is not None:
            df = pd.read_csv(data_file)
        if show_df and df is not None:
            st.dataframe(df, use_container_width=True)
        start = st.form_submit_button("Start")

with st.container():
    if start and df is not None:
        st.subheader("Simulation Results")
        sim = GBM(df, n_walkers, n_steps, n_traj, device_acc=device_acc)
        t_start = time()
        with st.spinner("In Progress ..."):
            result = sim.simulate()
        sim_duration = time() - t_start
        st.write(f"Simluation time: {round(sim_duration, 2)}s")

        traj = result.trajectories()
        distribution = result.price_distribution()
        return_distribution = result.return_distribution()
        dist_fig, _ = distribution.plot(bins=500)
        return_fig, return_ax = return_distribution.plot(kde=True)
        value_at_risk = result.VaR(alpha=100 - perc_var)
        return_ax.axvline(value_at_risk, color="r", linestyle="--")
        return_ax.text(
            value_at_risk,
            return_ax.get_ylim()[1],
            f"{perc_var}% VaR: {value_at_risk:.2f}",
            color="r",
            ha="left",
            va="top",
        )
        st.line_chart(data=traj.value())
        left_col, right_col = st.columns(2)
        with left_col:
            st.pyplot(dist_fig)
        with right_col:
            st.pyplot(return_fig)
        st.write(f"There's {100 - perc_var}% chance with the odds of losing {abs(value_at_risk * 100):.2f}%")
