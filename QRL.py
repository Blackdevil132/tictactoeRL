import sys
import numpy as np

import TicTacToe
import pickle

from utility import checkWin

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
    def __init__(self, total_episodes, learning_rate, discount_rate, decay_rate, space, rewards=(10, -100, 5)):
        self.total_episodes = total_episodes
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.epsilon = 1.0
        self.max_epsilon = 1.0
        self.min_epsilon = 0.1
        self.decay_rate = decay_rate

        self.action_space = space[0]
        self.observation_space = space[1]

        self.qtable = {}
        self.rewards = rewards
        self.environment = None

    def statusBar(self, iteration):
        bar_len = 60
        filled_len = int(round(bar_len * iteration / self.total_episodes))
        percents = round(100.0 * iteration / float(self.total_episodes), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('\r[%s] %s%%' % (bar, percents))
        sys.stdout.flush()

    def exportToFile(self, path="qtable"):
        with open(path + '.pkl', 'wb') as f:
            pickle.dump(self.qtable, f, pickle.HIGHEST_PROTOCOL)

    def updateQ(self, state, action, reward, max_future_reward):
        # if state is unknown, add empty entry to qtable
        if state not in self.qtable:
            self.qtable[state] = np.zeros(self.action_space)

        # if state is final, set q-value to reward
        if reward != 0:
            self.qtable[state][action] = reward
        else:
            # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
            # qtable[new_state,:] : all the actions we can take from new state
            self.qtable[state][action] = self.qtable[state][action] + self.learning_rate * (
                    reward + self.discount_rate * max_future_reward - self.qtable[state][action])

    def updateEpsilon(self, episode):
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)

    def getMaxFutureReward(self, next_state):
        possible_future_rewards = [0]
        # check all possible next states and get max rewards for all possible enemy actions
        for i in range(9):
            if next_state[i] == 0:
                new_next_state = list(next_state)
                new_next_state[i] = -1
                new_next_state = tuple(new_next_state)
                try:
                    possible_future_rewards.append(np.max(self.qtable[new_next_state][:]))
                except KeyError:
                    possible_future_rewards.append(0)

        return np.max(possible_future_rewards)

    def initLearning(self):
        # init Game Environment
        self.environment = TicTacToe.Game(self.rewards)

    def learnFromSteps(self, list_of_steps):
        # iterate through all steps taken by the agent from last to first and learn
        for step in list_of_steps:
            state, action, next_state, reward = step

            # get maximum possible future reward for the activated state
            future_reward = self.getMaxFutureReward(next_state)

            # update qtable-entry for current state and action
            self.updateQ(state, action, reward, future_reward)

    def run(self):
        self.initLearning()

        # execute Game and learn
        for episode in range(self.total_episodes):
            # display progress bar
            if episode % (self.total_episodes/1000) == 0:
                self.statusBar(episode)

            # Reset the environment
            self.environment.reset()

            # execute one iteration of the game
            steps = self.environment.run(self.qtable, self.epsilon)

            # iterate through all steps taken by the agent from last to first and learn
            self.learnFromSteps(reversed(steps))

            # Reduce epsilon
            self.updateEpsilon(episode)

        self.exportToFile()

    def getWLRs(self, number_of_runs=1000):
        env = TicTacToe.Game(self.rewards)
        results = [0, 0, 0]

        for episode in range(number_of_runs):
            # Reset the environment
            env.reset()
            # run game
            steps = env.run(self.qtable)
            # get reward from last step
            reward = steps[-1][3]
            for i in range(3):
                if reward == self.rewards[i]:
                    results[i] += 1

        return results
