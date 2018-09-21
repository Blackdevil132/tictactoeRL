import sys
import numpy as np
import tictactoeRL
import pickle
import random

# total_episodes = 500000        # Total episodes
# learning_rate = 0.8           # Learning rate
max_steps = 99  # Max steps per episode
# gamma = 0.95                  # Discounting rate

# Exploration parameters
epsilon = 1.0  # Exploration rate
max_epsilon = 1.0  # Exploration probability at start
min_epsilon = 0.01  # Minimum exploration probability


# decay_rate = 0.004             # Exponential decay rate for exploration prob


class QRL:
    def __init__(self, total_episodes, learning_rate, gamma, decay_rate, rewards=(10, -100, 5)):
        self.total_episodes = total_episodes
        self.learning_rate = learning_rate
        self.max_steps = max_steps
        self.discount_rate = gamma
        self.epsilon = epsilon
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate

        self.action_space = 9
        self.observation_space = 19683

        self.qtable = {}
        self.rewards = rewards

        self.iteration = 0

    def statusBar(self):
        bar_len = 60
        filled_len = int(round(bar_len * self.iteration / self.total_episodes))
        percents = round(100.0 * self.iteration / float(self.total_episodes), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('\r[%s] %s%%' % (bar, percents))
        sys.stdout.flush()

    def saveToFile(self, path="qtable"):
        with open(path + '.pkl', 'wb') as f:
            pickle.dump(self.qtable, f, pickle.HIGHEST_PROTOCOL)

    def learn(self):
        # List of rewards
        env = tictactoeRL.Game(self.rewards)
        max_refresh = self.total_episodes/1000

        for episode in range(self.total_episodes):
            self.iteration = episode
            if self.iteration % max_refresh == 0:
                self.statusBar()

            # Reset the environment
            env.reset()
            total_rewards = 0

            steps = env.run(self.qtable, self.epsilon)
            for step in steps:
                state, action, new_state, reward = step

                if state not in self.qtable:
                    self.qtable[state] = np.zeros(self.action_space)
                if new_state not in self.qtable:
                    self.qtable[new_state] = np.zeros(self.action_space)

                # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
                # qtable[new_state,:] : all the actions we can take from new state
                pos_rewards = [0]
                for i in range(9):
                    if new_state[i] == ' ':
                        new_new_state = list(new_state)
                        new_new_state[i] = 'X'
                        new_new_state = tuple(new_new_state)
                        try:
                            pos_rewards.append(np.max(self.qtable[new_new_state][:]))
                        except KeyError:
                            pos_rewards.append(0)
                try:
                    future_reward = np.max(pos_rewards)
                except ValueError:
                    print(pos_rewards)
                    raise RuntimeError

                self.qtable[state][action] = self.qtable[state][action] + self.learning_rate * (
                        reward + self.discount_rate * future_reward - self.qtable[state][action])

                total_rewards += reward

            # Reduce epsilon
            self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)

    def test(self):
        env = tictactoeRL.Game(self.rewards)
        wins = 0
        draws = 0
        losses = 0

        for episode in range(1000):
            # Reset the environment
            env.reset()
            steps = env.run(self.qtable, self.epsilon)
            reward = steps[-1][3]
            if reward == self.rewards[0]:
                wins += 1
            elif reward == self.rewards[1]:
                losses += 1
            else:
                draws += 1

        return wins, draws, losses
