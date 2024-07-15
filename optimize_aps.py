import matplotlib.pyplot as plt
from mininet.wifi.net import Mininet_wifi
from mininet.wifi.node import Station, OVSKernelAP
from mininet.wifi.link import wmediumd, mesh, adhoc
from mininet.wifi.cli import CLI_wifi
from mininet.wifi.wmediumdConnector import interference
import numpy as np
import random

class SimpleRLAgent:
    def __init__(self, num_aps):
        self.num_aps = num_aps
        self.q_table = np.zeros((2 ** num_aps, num_aps))  # State-action space
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate

    def get_state(self, ap_states):
        return int(''.join(map(str, ap_states)), 2)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.num_aps - 1)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state, action] = self.q_table[state, action] + self.alpha * (
            reward + self.gamma * self.q_table[next_state, best_next_action] - self.q_table[state, action])

def optimize_aps():
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    # Create stations and access points
    sta1 = net.addStation('sta1', ip='10.0.0.1/8')
    ap1 = net.addAccessPoint('ap1', ssid='ssid_ap1', mode='g', channel='1', position='30,50,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid_ap2', mode='g', channel='1', position='60,50,0')
    c1 = net.addController('c1')

    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)

    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    aps = [ap1, ap2]
    rl_agent = SimpleRLAgent(num_aps=len(aps))

    active_aps_per_episode = []
    rewards_per_episode = []

    for episode in range(1000):  # Run for a number of episodes
        ap_states = [1 for _ in aps]  # Initially, all APs are active
        state = rl_agent.get_state(ap_states)
        total_reward = 0
        for _ in range(10):  # Each episode has a number of steps
            action = rl_agent.choose_action(state)
            ap_states[action] = 1 - ap_states[action]  # Toggle AP state

            # Apply the action by enabling/disabling the AP
            if ap_states[action] == 1:
                aps[action].start([c1])
            else:
                aps[action].stop()

            next_state = rl_agent.get_state(ap_states)

            # Reward function: for simplicity, reward is negative of number of active APs
            reward = -sum(ap_states)
            total_reward += reward

            rl_agent.update_q_table(state, action, reward, next_state)
            state = next_state

        active_aps_per_episode.append(sum(ap_states))
        rewards_per_episode.append(total_reward)

    CLI_wifi(net)
    net.stop()

    # Plotting results
    plt.figure()
    plt.plot(active_aps_per_episode, label='Active APs per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Number of Active APs')
    plt.legend()
    plt.title('Active APs per Episode')

    plt.figure()
    plt.plot(rewards_per_episode, label='Total Reward per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.legend()
    plt.title('Total Reward per Episode')

    plt.show()

if __name__ == '__main__':
    optimize_aps()
