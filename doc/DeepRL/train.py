from world import World
import sys
sys.path.append("../")
from base_web import start, inputDict, outputDict
import base_web
import time
import random
from robot import SENSOR_MAX_RANGE, SENSOR_MIN_RANGE
from point import Pt

start("viz.html", "viz.js", {"l": 0, "r": 0}, None)

#### Simulator Setup ^^^^^
from gym.spaces import Box, Discrete
import numpy as np

TIMESTEP = 0.05
SPEED = 1.5

class RobotEnv(object):
    reward_range = (-np.inf, np.inf)
    action_space = Discrete(3)
    observation_space = Box(low=np.array([SENSOR_MIN_RANGE] * 2), high=np.array([SENSOR_MAX_RANGE * 2] * 2))

    def __init__(self):
        self.world = World(1000, 1000, 0)
        self.startPoint = Pt(-16, 0)
        self.time = 0


    def step(self, action):
        l, r = 0, 0
        if action == 0:
            l = SPEED
            r = -SPEED
        elif action == 1:
            l = SPEED
            r = SPEED
        elif action == 2:
            l = -SPEED
            r = SPEED
        elif action == 3:
            l = -SPEED
            r = -SPEED

        self.world.simulate(l, r, TIMESTEP)

        self.time = self.time + 1

        closestObstacle = sorted(self.world.obstacles, key=lambda obs: Pt(obs.x, obs.y).dist(Pt(self.world.robot.x, self.world.robot.y)))[-1]

        dist = Pt(closestObstacle.x, closestObstacle.y).dist(Pt(self.world.robot.x, self.world.robot.y))

        reward = Pt(self.world.robot.x, self.world.robot.y).dist(self.startPoint) * 100 - (10000 if self.world.checkCollision() else 0) 
        if dist < 3:
            reward = reward - ((3 - dist) * 350)

        proxL = self.world.proxL if self.world.proxL is not None else SENSOR_MAX_RANGE * 2
        proxR = self.world.proxR if self.world.proxR is not None else SENSOR_MAX_RANGE * 2
        return (np.array([proxL, proxR]), reward, self.time > 1000 or self.world.checkCollision(), {})

    def reset(self):
        self.time = 0
        self.world.robot.x = -16.5

        self.world.robot.y = 0.0
        self.world.robot.theta = 0.0
        self.world.obstacles.clear()
        def createObstacle(xRange, yRange, widthRange, heightRange):
            self.world.addObstacle(random.randint(xRange[0], xRange[1]),
                    random.randint(yRange[0], yRange[1]),
                    random.randint(widthRange[0], widthRange[1]),
                    random.randint(heightRange[0], heightRange[1]))

        for i in range(random.randint(15, 25)):
            createObstacle((-14, 20), (-16, 16), (2, 2), (2, 2))

        # Walls
        self.world.addObstacle(0, 14.5, 40, 1)
        self.world.addObstacle(0, -14.5, 40, 1)
        self.world.addObstacle(-19.5, 0, 1, 30)
        self.world.addObstacle(19.5, 0, 1, 30)

        self.world.simulate(0.0, 0.0, TIMESTEP)

        proxL = self.world.proxL if self.world.proxL is not None else SENSOR_MAX_RANGE * 2
        proxR = self.world.proxR if self.world.proxR is not None else SENSOR_MAX_RANGE * 2
        return np.array([proxL, proxR])

    def render(self, mode="human", close=False):
        world = self.world
        base_web.outputDict = {
            "worldWidth": world.width,
            "worldHeight": world.height,
            "timestamp": world.timestamp,
            "proxL": world.proxL,
            "proxR": world.proxR,
            "pointL": world.pointL.serialize() if world.pointL else None,
            "pointR": world.pointR.serialize() if world.pointR else None,
            "robotX": world.robot.x,
            "robotY": world.robot.y,
            "robotTheta": world.robot.theta,
            "robotWidth": world.robot.robotSize[0],
            "robotHeight": world.robot.robotSize[1],
            "robotLeftSensorPos": world.robot.getLeftSensorPos().serialize(),
            "robotRightSensorPos": world.robot.getRightSensorPos().serialize(),
            "obstacles": [obs.serialize() for obs in world.obstacles]
        }



from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


env = RobotEnv()
nb_actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(3, activation='linear'))
print(model.summary())

memory = SequentialMemory(limit=500000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, enable_dueling_network=True, dueling_type='avg', nb_steps_warmup=1000, target_model_update=1e-2, policy=policy)

dqn.compile(Adam(lr=1e-2), metrics=['mae'])

dqn.fit(env, nb_steps=500000, visualize=True, verbose=2)

dqn.save_weights('dqnweights.h5f', overwrite=True)

dqn.test(env, nb_episodes=5, visualize=True)
