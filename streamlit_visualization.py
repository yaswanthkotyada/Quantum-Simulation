import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time

# Load results from JSON file
def load_results():
    try:
        with open("quantum_results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Error: quantum_results.json file not found!")
        return None
    except json.JSONDecodeError:
        st.error("Error: Invalid JSON format!")
        return None

# Load the results
results = load_results()

if results:
    ground_state_energy = results.get("ground_state_energy", 0.0)
    iterations = results.get("iterations", 100)
    energy_convergence = np.array(results.get("energy_convergence", np.linspace(0.6, -0.886786, iterations)))

    # Streamlit UI
    st.title("Quantum Simulation - VQE Visualization")

    # Sidebar Controls
    st.sidebar.header("Visualization Controls")
    show_histogram = st.sidebar.checkbox("Show Energy Distribution", True)
    show_running_avg = st.sidebar.checkbox("Show Running Average", True)
    use_plotly = st.sidebar.checkbox("Use Plotly for Interactive Plots", True)

    st.write("### Ground-State Energy Calculation")
    st.write(f"**Ground-State Energy:** {ground_state_energy:.6f} Ha")
    st.write(f"**Total Iterations:** {iterations}")

    # Energy Convergence Plot
    st.write("### Energy Convergence")
    if use_plotly:
        fig_convergence = px.line(
            x=np.arange(len(energy_convergence)), 
            y=energy_convergence, 
            labels={"x": "Iterations", "y": "Energy (Hartree)"},
            title="VQE Energy Convergence"
        )
        st.plotly_chart(fig_convergence)
    else:
        fig, ax = plt.subplots()
        ax.plot(energy_convergence, label="Energy Convergence", color="blue")
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Energy (Hartree)")
        ax.legend()
        ax.set_title("VQE Energy Convergence")
        ax.grid()
        st.pyplot(fig)

    # Histogram Plot (Optional)
    if show_histogram:
        st.write("### Energy Distribution")
        if use_plotly:
            fig_hist = px.histogram(
                energy_convergence, nbins=30, 
                title="Energy Distribution", 
                labels={'x': "Energy (Hartree)", 'y': "Frequency"}
            )
            st.plotly_chart(fig_hist)
        else:
            fig, ax = plt.subplots()
            ax.hist(energy_convergence, bins=20, alpha=0.7, color='blue')
            ax.set_xlabel("Energy (Hartree)")
            ax.set_ylabel("Frequency")
            ax.set_title("Energy Distribution")
            st.pyplot(fig)

    # Running Average Plot (Optional)
    if show_running_avg:
        st.write("### Running Average of Energy")
        running_avg = np.cumsum(energy_convergence) / np.arange(1, len(energy_convergence) + 1)
        if use_plotly:
            fig_avg = px.line(
                x=np.arange(len(running_avg)), y=running_avg, 
                labels={"x": "Iterations", "y": "Energy (Hartree)"},
                title="Running Average of Energy"
            )
            st.plotly_chart(fig_avg)
        else:
            fig, ax = plt.subplots()
            ax.plot(running_avg, label='Running Average', color="green")
            ax.set_xlabel("Iterations")
            ax.set_ylabel("Energy (Hartree)")
            ax.set_title("Running Average of Energy")
            ax.legend()
            st.pyplot(fig)

    # Progress bar for energy convergence
    st.subheader("Energy Convergence Progress")
    progress_bar = st.progress(0)
    
    for i in range(iterations):
        progress_bar.progress((i+1) / iterations)
        time.sleep(0.01)  # Simulated delay for visualization

    # Display final results
    st.write(f"**Final Computed Ground-State Energy:** {round(energy_convergence[-1], 6)} Hartree")
    st.write(f"**Total Iterations Processed:** {iterations}")

