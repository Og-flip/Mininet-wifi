# Mininet-WiFi AP Optimization with Reinforcement Learning

This project uses Mininet-WiFi to simulate a wireless network environment and implements a reinforcement learning (RL) agent to optimize the power consumption of access points (APs). The RL agent learns to switch APs between active and idle states based on traffic load, reducing overall power consumption.

## Features

- Simulate WiFi network with Mininet-WiFi
- Implement a simple RL agent using Q-learning
- Optimize AP states to reduce power consumption
- Plot results showing active APs and rewards over episodes

## Requirements

- Mininet-WiFi
- NumPy
- Matplotlib

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Og-flip/Mininet-wifi
    cd Mininet-wifi
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the optimization script:
    ```bash
    python optimize_aps.py
    ```

2. After running the script, you can interact with the Mininet-WiFi CLI to inspect the network:
    ```bash
    mininet-wifi> <your_commands_here>
    ```

3. The script will also generate and display plots showing the optimization results.

## Script Overview

- `optimize_aps.py`: Main script to set up the Mininet-WiFi network, implement the RL agent, run the optimization, and plot the results.
- `requirements.txt`: Lists the required Python packages.

## Plotting Results

The script will display two plots:
- **Active APs per Episode**: Shows the number of active APs over each episode.
- **Total Reward per Episode**: Shows the total reward accumulated over each episode.
