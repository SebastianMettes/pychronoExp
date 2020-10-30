from gym.envs.registration import register

register(
    id='multiarm-v0',
    entry_point='gym_multiarm.envs:Multi_armEnv',
)