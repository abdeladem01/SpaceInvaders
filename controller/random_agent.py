import numpy as np
import csv

class RandomAgent():

    def __init__(self, nx, ny, nd, num_actions, game, gamma, alpha, n_episodes, max_iter, epsilon):

        self.num_actions = num_actions
        self.game = game

        self.Q = np.zeros([nx, ny, nd, num_actions])

        # self.gamma = 0.8
        # self.alpha = 0.1
        # self.n_episodes = 500
        # self.max_iter = 50000
        # self.epsilon = 0.9

        self.gamma = gamma
        self.alpha = alpha
        self.n_episodes = n_episodes
        self.max_iter = max_iter
        self.epsilon = epsilon


    def learn(self):
        

        for e in range(self.n_episodes):
            reward_sum = 0
            self.game.reset()
            state = self.game.get_state()
            

            count = 0
            while count < self.max_iter:

                action = self.select_action(state)

                next_state, reward, done = self.game.step(action)

                reward_sum += reward

                if done:
                    break
                
                self.updateQ(state, action, reward_sum, next_state)

                state = next_state
                count += 1
            
            print("Episode : ", e, "Reward: ", reward_sum)
            self.append_to_csv("plot_episode_rewards.csv", [e, reward_sum, self.Q[state][action]])

            self.epsilon = max(self.epsilon - 1 / (self.n_episodes - 1.), 0)

    def updateQ(self, state, action, reward, next_state):
        current_q = self.Q[state][action]
        next_q = reward + self.gamma * max(self.Q[next_state])
        self.Q[state][action] = current_q + self.alpha * (next_q - current_q) 

    def saveQ(self, filename) :
        np.save(filename, self.Q)

    def loadQ(self, filename):
        self.Q = np.load(filename)


    def select_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.Q[state][:])
        
    def append_to_csv(self, filename, row):
        with open(filename, mode='a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row)