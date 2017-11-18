import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import os


class Navigation(gym.Env):
    """Navigation

    avoid hazards

    """
    def __init__(self, grid_size=10):

        self.grid_size = grid_size
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0., high=2., shape=(grid_size,grid_size))
        self.observation = None
        # self._seed()
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        """Run one timestep of the environment's dynamics.
        Accepts an action and returns a tuple (observation, reward, done, info).
        # Arguments
            action (object): An action provided by the environment.
        # Returns
            observation (object): Agent's observation of the current environment.
            reward (float) : Amount of reward returned after previous action.
            done (boolean): Whether the episode has ended, in which case further step() calls will return undefined results.
            info (dict): Contains auxiliary diagnostic information (helpful for debugging, and sometimes learning).
        """
        assert self.action_space.contains(action)

        self.observation[self.vessel] = 0
        self.move_vessel(action)
        self.step_count += 1
        reward = -1

        done = False
        if self.destination == self.vessel:
            self.score += 1
            reward = 100
            self.observation[self.vessel] = 2
            self.new_destination()
            self.observation[self.destination] = 1.5
            self.step_count = 0
            # done = True
        elif self.hit_land() or self.step_count == 30:
            reward = -100
            done = True
        else:
            self.observation[self.vessel] = 2

        if self.score > 10:
            done = True

        return self.observation, reward, done, {"moves": self.step_count, "score": self.score}

    def new_destination(self):
        # if self.total_score >= 100:
        #     self.destination = (-1, -1)
        #     pass
        while True:
            destination = np.random.randint(1, self.grid_size - 1, 2)
            destination = (destination[0], destination[1])
            if destination == self.vessel:
                continue
            else:
                self.destination = destination
                break

    def move_vessel(self, action):


        if action == 4:
            action = self.previous_action
        else:
            self.previous_action = action

        v = self.vessel

        if action == 0:
            self.vessel = (v[0] - 1, v[1])
        elif action == 1:
            self.vessel = (v[0] + 1, v[1])
        elif action == 2:
            self.vessel = (v[0], v[1] - 1)
        elif action == 3:
            self.vessel = (v[0], v[1] + 1)



    # def get_state(self):
    #     canvas = self.observation
    #     canvas[self.vessel[0], self.vessel[1]] = 2.
    #     canvas[self.destination[0], self.destination[1]] = 1.5
    #     return canvas

    def hit_land(self):
        return self.observation[self.vessel] == 1

    # def _render(self, mode='human', close=False):
    #     """ Viewer only supports human mode currently. """
    #     plt.imshow(self.observation, interpolation='none')
    def rand_xy(self):
        return np.random.randint(1, self.grid_size - 1, int((self.grid_size ** 2) * 0.1))


    def _reset(self):
        """
             Resets the state of the environment and returns an initial observation.

             # Returns
                 observation (object): The initial observation of the space. Initial reward is assumed to be 0.
             """
        self.vessel = (4,4)
        self.new_destination()
        self.score = 0
        self.step_count = 0
        if np.random.randint(2) == 0:
            self.previous_action = 0
        else:
            self.previous_action = 1

        self.observation = np.ones((self.grid_size,) * 2)
        self.observation[1:-1, 1:-1] = 0.
        self.observation[self.rand_xy(), self.rand_xy()] = 1
        self.observation[self.vessel] = 2.
        self.observation[self.destination] = 1.5

        return self.observation

    def render(self, mode='human',close=True):
        # pass
        fld = '/Users/davesteps/Google Drive/pycharmProjects/keras_RL/'
        if 'images' not in os.listdir(fld):
            os.mkdir(fld + 'images')
        # for i in range(len(frames)):
        plt.imshow(self.observation, interpolation='none')
        plt.savefig(fld + 'images/' + str(self.step_count) + ".png")

