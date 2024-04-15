import numpy as np
import gym
from gym import spaces


# Ego agent localisation
ego_home1, ego_home2 = np.array([0.0, 0.5]), np.array([0.0, 0.5])


class Circle(gym.Env):

    def __init__(self):
        self.action_space = spaces.Box(
            low=-0.2,
            high=+0.2,
            shape=(2,),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=+np.inf,
            shape=(2,),
            dtype=np.float32
        )
        self.action_space_other = spaces.Box(
            low = -np.pi,
            high = np.pi,
            shape = (1,),
            dtype = np.float32
        )

        self.radius = 1.0
        self.change_partner = 0.99
        self.reset_theta = 0.999
        self.ego1 = np.copy(ego_home1)
        self.ego2 = np.copy(ego_home2)
        self.step_size = np.random.random() * 2 * np.pi - np.pi
        self.other = np.array([self.radius, 0.])
        self.theta = 0.0
        self.partner = 0
        self.timestep = 0
        self.mode = 'SelfPlay'
        self.ego = np.copy(ego_home1)



    def set_params(self, change_partner, mode='NotSelfPlay'):
        self.change_partner = change_partner
        self.mode = mode


    def _get_obs(self):
        return np.copy(self.ego)

    def _get_obs1(self):
        return np.copy(self.ego1)

    
    def _get_obs2(self):
        return np.copy(self.ego2)



    def polar(self, theta):
        return self.radius * np.array([np.cos(theta), np.sin(theta)])


    def reset(self):
        state1 = self._get_obs1()
        state2 = self._get_obs2()
        return state1, state2


    def step(self, actions):
        if self.mode == "Selfplay":
            print('Selfplay')
            self.timestep += 1
            self.ego1 += actions[0]
            self.ego2 += actions[1]
            self.other = self.polar(actions[2])
            reward1 = -np.linalg.norm(self.other - self.ego1) * 100
            reward2 = -np.linalg.norm(self.other - self.ego2) * 100
            reward_other = - reward1
            if reward1 > reward2:
                reward2 -= 100
            elif reward1 < reward2:
                reward1 -= 100
            done = False
            if self.timestep == 10:
                self.timestep = 0
                if np.random.random() > self.change_partner:
                    self.partner += 1
                    self.step_size = np.random.random() * 2 * np.pi - np.pi
                self.theta += self.step_size
                # randomly reset the other agent
                # if np.random.random() > self.reset_theta:
                #     self.theta = np.random.uniform(0, 2*np.pi)
                # # choose a new partner from the options
                # if np.random.random() > self.change_partner:
                #     self.partner = np.random.choice(range(4))

                # # LILI
                # if self.partner == 0:
                #     if np.random.random()  > self.radius:
                #         self.theta += np.pi/10
                #     else:
                #         self.theta -= np.pi/10
                # # SILI
                # if self.partner == 1:
                #     if np.random.random() > self.radius:
                #         self.theta -= np.pi/8
                # # No influence
                # if self.partner == 2:
                #     self.theta += np.pi/4
                # # No influence
                # if self.partner == 3:
                #     self.theta -= np.pi/2

                self.ego1, self.ego2 = np.copy(ego_home1), np.copy(ego_home2)
                self.other = self.polar(self.theta)
            return [self._get_obs1(),self._get_obs2()], [reward1, reward2], done, {}
        else:
            print('Not')
            self.timestep += 1
            self.ego += actions
            reward = -np.linalg.norm(self.other - self.ego) * 100
            done = False
            if self.timestep == 10:
                self.timestep = 0
                # randomly reset the other agent
                if np.random.random() > self.reset_theta:
                    self.theta = np.random.uniform(0, 2*np.pi)
                # choose a new partner from the options
                if np.random.random() > self.change_partner:
                    self.partner = np.random.choice(range(4))

                # LILI
                if self.partner == 0:
                    if np.linalg.norm(self.ego) > self.radius:
                        self.theta += np.pi/10
                    else:
                        self.theta -= np.pi/10
                # SILI
                if self.partner == 1:
                    if np.linalg.norm(self.ego) > self.radius:
                        self.theta -= np.pi/8
                # No influence
                if self.partner == 2:
                    self.theta += np.pi/4
                # No influence
                if self.partner == 3:
                    self.theta -= np.pi/2

                self.ego = np.copy(ego_home1)
                self.other = self.polar(self.theta)
            return self._get_obs(), reward, done, {}