import numpy as np
import tictactoeRL
import random

total_episodes = 20000        # Total episodes
learning_rate = 0.8           # Learning rate
max_steps = 99                # Max steps per episode
gamma = 0.95                  # Discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.01            # Minimum exploration probability
decay_rate = 0.005             # Exponential decay rate for exploration prob


class QRL:
    def __init__(self, action_space, observation_space):
        self.total_episodes = total_episodes
        self.learning_rate = learning_rate
        self.max_steps = max_steps
        self.discount_rate = gamma
        self.epsilon = epsilon
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate

        self.action_space = action_space
        self.observation_space = observation_space

        self.qtable = {}

    def learn(self):
        # List of rewards
        rewards = []
        env = tictactoeRL.Game()

        for episode in range(self.total_episodes):
            # Reset the environment
            env.reset()
            total_rewards = 0

            steps, reward = env.run(self.qtable, self.epsilon)
            for step in steps:
                state, action, new_state = step

                # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
                # qtable[new_state,:] : all the actions we can take from new state
                if state not in self.qtable:
                    self.qtable[state] = np.zeros(self.action_space)
                if new_state not in self.qtable:
                    self.qtable[new_state] = np.zeros(self.action_space)

                self.qtable[state][action] = self.qtable[state][action] + self.learning_rate * (
                        reward + self.discount_rate * np.max(self.qtable[new_state][:]) - self.qtable[state][action])

                total_rewards += reward

            # Reduce epsilon
            self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)
            rewards.append(total_rewards)

    def test(self):
        env = tictactoeRL.Game()
        wins = 0
        draws = 0
        losses = 0

        for episode in range(1000):
            # Reset the environment
            env.reset()
            steps, reward = env.run(self.qtable, self.epsilon)
            if reward == 10:
                wins += 1
            elif reward == -10:
                losses += 1
            else:
                draws += 1

        return wins, draws, losses
