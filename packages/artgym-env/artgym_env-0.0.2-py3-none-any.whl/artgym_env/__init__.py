__version__ = "0.0.2"

from gymnasium.envs.registration import (
    register
)

register(
    id="artgym_env/GridWorld-v0",
    entry_point="artgym_env.envs:GridWorldEnv",
    max_episode_steps=1000,
)

register(
    id="artgym_env/LeoQuad-v4",
    entry_point="artgym_env.envs.mujoco.leoquad_v4:LeoQuadEnv",
    max_episode_steps=5000,
)
