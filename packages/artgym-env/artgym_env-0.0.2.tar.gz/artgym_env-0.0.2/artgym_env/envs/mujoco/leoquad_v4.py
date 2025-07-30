import numpy as np
from os import path

from gymnasium import utils
from gymnasium.envs.mujoco import MujocoEnv
from gymnasium.spaces import Box


DEFAULT_CAMERA_CONFIG = {
    "trackbodyid": 0,
    "distance": 2.04,
}


class LeoQuadEnv(MujocoEnv, utils.EzPickle):
    """
    ## Description

    This environment is the quadruped walking robot, LeoQuad, environment
    The goal is to balance the robot on the plane.

    ## Action Space
    The agent take a 12-elements vector for actions.

    The action space is a continuous `(action)` in `[-3, 3]`, where `action` represents
    the numerical torque applied to each joint.

    | Num | Action                           | Control Min | Control Max | Name (in corresponding XML file) | Joint    | Unit        |
    |-----|----------------------------------|-------------|-------------|----------------------------------|----------|-------------|
    | 0   | Torque applied on FL roll joint  | -3          | 3           | FL_Roll                          | hinge    | Torque (Nm) |
    | 1   | Torque applied on FL pitch joint | -3          | 3           | FL_Pitch                         | hinge    | Torque (Nm) |
    | 2   | Torque applied on FL knee joint  | -3          | 3           | FL_Knee                          | hinge    | Torque (Nm) |
    | 3   | Torque applied on BL roll joint  | -3          | 3           | BL_Roll                          | hinge    | Torque (Nm) |
    | 4   | Torque applied on BL pitch joint | -3          | 3           | BL_Pitch                         | hinge    | Torque (Nm) |
    | 5   | Torque applied on BL knee joint  | -3          | 3           | BL_Knee                          | hinge    | Torque (Nm) |
    | 6   | Torque applied on FR roll joint  | -3          | 3           | FR_Roll                          | hinge    | Torque (Nm) |
    | 7   | Torque applied on FR pitch joint | -3          | 3           | FR_Pitch                         | hinge    | Torque (Nm) |
    | 8   | Torque applied on FR knee joint  | -3          | 3           | FR_Knee                          | hinge    | Torque (Nm) |
    | 9   | Torque applied on BR roll joint  | -3          | 3           | BR_Roll                          | hinge    | Torque (Nm) |
    | 10  | Torque applied on BR pitch joint | -3          | 3           | BR_Pitch                         | hinge    | Torque (Nm) |
    | 11  | Torque applied on BR knee joint  | -3          | 3           | BR_Knee                          | hinge    | Torque (Nm) |

    ## Observation Space

    The state space consists of positional values of all joints, followed by the velocities of those joints
    with all the positions ordered before all the velocities.

    The observation is a `ndarray` with shape `(24,)` where the elements correspond to the following:

    | Num | Observation                                            | Min  | Max | Name (in corresponding XML file) | Joint | Unit                      |
    | --- | ------------------------------------------------------ | ---- | --- | -------------------------------- | ----- | ------------------------- |
    |     | x-coordinate of the base body                          | -Inf | Inf | BODY                             |       | position (m)              | 
    |     | y-coordinate of the base body                          | -Inf | Inf | BODY                             |       | position (m)              | 
    | 0   | z-coordinate of the base body                          | -Inf | Inf | BODY                             |       | position (m)              | 
    | 1   | w-element of quaternion(orientation) of the base body  | -Inf | Inf | BODY                             |       |                           | 
    | 2   | x-element of quaternion(orientation) of the base body  | -Inf | Inf | BODY                             |       |                           |  
    | 3   | y-element of quaternion(orientation) of the base body  | -Inf | Inf | BODY                             |       |                           |  
    | 4   | z-element of quaternion(orientation) of the base body  | -Inf | Inf | BODY                             |       |                           |  
    | 5   | angle of the FL roll joint                             | -Inf | Inf | FL_Roll                          | hinge | angle (rad)               |
    | 6   | angle of the FL pitch joint                            | -Inf | Inf | FL_Pitch                         | hinge | angle (rad)               |
    | 7   | angle of the FL knee joint                             | -Inf | Inf | FL_Knee                          | hinge | angle (rad)               |
    | 8   | angle of the BL roll joint                             | -Inf | Inf | BL_Roll                          | hinge | angle (rad)               |
    | 9   | angle of the BL pitch joint                            | -Inf | Inf | BL_Pitch                         | hinge | angle (rad)               |
    | 10  | angle of the BL knee joint                             | -Inf | Inf | BL_Knee                          | hinge | angle (rad)               |
    | 11  | angle of the FR roll joint                             | -Inf | Inf | FR_Roll                          | hinge | angle (rad)               |
    | 12  | angle of the FR pitch joint                            | -Inf | Inf | FR_Pitch                         | hinge | angle (rad)               |
    | 13  | angle of the FR knee joint                             | -Inf | Inf | FR_Knee                          | hinge | angle (rad)               |
    | 14  | angle of the BR roll joint                             | -Inf | Inf | BR_Roll                          | hinge | angle (rad)               |
    | 15  | angle of the BR pitch joint                            | -Inf | Inf | BR_Pitch                         | hinge | angle (rad)               |
    | 16  | angle of the BR knee joint                             | -Inf | Inf | BR_Knee                          | hinge | angle (rad)               |
    | 17  | x-velocity of the base body                            | -Inf | Inf | BODY                             |       | position (m/s)            | 
    | 18  | y-velocity of the base body                            | -Inf | Inf | BODY                             |       | position (m/s)            | 
    | 19  | z-velocity of the base body                            | -Inf | Inf | BODY                             |       | position (m/s)            | 
    | 20  | x-angular velocity of the base body                    | -Inf | Inf | BODY                             |       | position (rad/s)          | 
    | 21  | y-angular velocity of the base body                    | -Inf | Inf | BODY                             |       | position (rad/s)          | 
    | 22  | z-angular velocity of the base body                    | -Inf | Inf | BODY                             |       | position (rad/s)          | 
    | 23  | angular velocity of the FL roll joint                  | -Inf | Inf | FL_Roll                          | hinge | angular velocity (rad/s)  |
    | 24  | angular velocity of the FL pitch joint                 | -Inf | Inf | FL_Pitch                         | hinge | angular velocity (rad/s)  |
    | 25  | angular velocity of the FL knee joint                  | -Inf | Inf | FL_Knee                          | hinge | angular velocity (rad/s)  |
    | 26  | angular velocity of the BL roll joint                  | -Inf | Inf | BL_Roll                          | hinge | angular velocity (rad/s)  |
    | 27  | angular velocity of the BL pitch joint                 | -Inf | Inf | BL_Pitch                         | hinge | angular velocity (rad/s)  |
    | 28  | angular velocity of the BL knee joint                  | -Inf | Inf | BL_Knee                          | hinge | angular velocity (rad/s)  |
    | 29  | angular velocity of the FR roll joint                  | -Inf | Inf | FR_Roll                          | hinge | angular velocity (rad/s)  |
    | 30  | angular velocity of the FR pitch joint                 | -Inf | Inf | FR_Pitch                         | hinge | angular velocity (rad/s)  |
    | 31  | angular velocity of the FR knee joint                  | -Inf | Inf | FR_Knee                          | hinge | angular velocity (rad/s)  |
    | 32  | angular velocity of the BR roll joint                  | -Inf | Inf | BR_Roll                          | hinge | angular velocity (rad/s)  |
    | 33  | angular velocity of the BR pitch joint                 | -Inf | Inf | BR_Pitch                         | hinge | angular velocity (rad/s)  |
    | 34  | angular velocity of the BR knee joint                  | -Inf | Inf | BR_Knee                          | hinge | angular velocity (rad/s)  |
    
    If `use_contact_forces` is `True` then the observation space is extended by 14*6 = 84 elements, which are contact forces
    (external forces - force x, y, z and torque x, y, z) applied to the
    center of mass of each of the body parts. The 14 body parts are:
    
    | id | body parts |
    |  ---  |  ------------  |
    | 0  | worldbody (note: forces are always full of zeros) |
    | 1  | BODY |
    | 2  | FL_Roll |
    | 3  | FL_Pitch |
    | 4  | FL_Knee |
    | 5  | BL_Roll |
    | 6  | BL_Pitch |
    | 7  | BL_Knee |
    | 8  | FR_Roll |
    | 9  | FR_Pitch |
    | 10 | FR_Knee |
    | 11 | BR_Roll |
    | 12 | BR_Pitch |
    | 13 | BR_Knee |


    ## Rewards
    The total reward is reward = healthy_reward + forward_reward - ctrl_cost - contact_cost.
    
    - *healthy_reward*: Every timestep that the robot is healthy (see definition in section "Episode Termination"), it gets a reward of fixed value `healthy_reward`
    - *forward_reward*: A reward of moving forward which is measured as
    *(x-coordinate before action - x-coordinate after action)/dt*. *dt* is the time
    between actions and is dependent on the `frame_skip` parameter (default is 5),
    where the frametime is 0.001 - making the default *dt = 5 * 0.001 = 0.005*.
    This reward would be positive if the robot moves forward (in positive x direction).
    - *ctrl_cost*: A negative reward for penalising the robot if it takes actions
    that are too large. It is measured as *`ctrl_cost_weight` * sum(action<sup>2</sup>)*
    where *`ctr_cost_weight`* is a parameter set for the control and has a default value of 0.5.
    - *contact_cost*: A negative reward for penalising the robot if the external contact
    force is too large. It is calculated *`contact_cost_weight` * sum(clip(external contact
    force to `contact_force_range`)<sup>2</sup>)*.

    The total reward returned is ***reward*** *=* *healthy_reward + forward_reward - ctrl_cost*.

    But if `use_contact_forces=True`
    The total reward returned is ***reward*** *=* *healthy_reward + forward_reward - ctrl_cost - contact_cost*.

    In either case `info` will also contain the individual reward terms.
    

    ## Starting State
    All observations start in state
    (0.0, ) with a uniform noise in the range
    of [-0.01, 0.01] added to the values for stochasticity.

    ## Episode End
    The episode ends when any of the following happens:

    1. Truncation: The episode duration reaches 1000 timesteps.
    2. Termination: Any of the state space values is no longer finite.
    3. Termination: The absolute value of the vertical angle between the base body and the floor is greater than 0.2 radian.

    ## Arguments

    No additional arguments are currently supported.

    ```python
    import gymnasium as gym
    import artgym_env
    env = gym.make('artgym_env/LeoQuad-v4')
    ```

    ## Version History

    * v4: Initial versions release
    """

    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps": 200, # int(np.round(1.0 / self.dt)) == self.metadata["render_fps"], where self.dt := self.model.opt.timestep * self.frame_skip
    }

    def __init__(
        self, 
        xml_file="LeoQuad.xml",
        ctrl_cost_weight=0.5,
        use_contact_forces=False,
        contact_cost_weight=5e-4,
        healthy_reward=1.0,
        terminate_when_unhealthy=True,
        healthy_z_range=(0.2, 1.0),
        contact_force_range=(-1.0, 1.0),
        reset_noise_scale=0.1,
        exclude_current_positions_from_observation=True,
        **kwargs,
    ):
        utils.EzPickle.__init__(
            self,
            xml_file,
            ctrl_cost_weight,
            use_contact_forces,
            contact_cost_weight,
            healthy_reward,
            terminate_when_unhealthy,
            healthy_z_range,
            contact_force_range,
            reset_noise_scale,
            exclude_current_positions_from_observation,
            **kwargs,
        )
        
        self._ctrl_cost_weight = ctrl_cost_weight
        self._contact_cost_weight = contact_cost_weight

        self._healthy_reward = healthy_reward
        self._terminate_when_unhealthy = terminate_when_unhealthy
        self._healthy_z_range = healthy_z_range

        self._contact_force_range = contact_force_range

        self._reset_noise_scale = reset_noise_scale

        self._use_contact_forces = use_contact_forces

        self._exclude_current_positions_from_observation = (
            exclude_current_positions_from_observation
        )
        
        obs_shape = 35
        if not exclude_current_positions_from_observation:
            obs_shape += 2
        if use_contact_forces:
            obs_shape += 84

        observation_space = Box(
            low=-np.inf, high=np.inf, shape=(obs_shape,), dtype=np.float64
        )

        xml_fullpath = path.join(path.dirname(__file__), "assets", xml_file)
        print(f"loading mujoco model... {xml_fullpath}")
        MujocoEnv.__init__(
            self,
            xml_fullpath,
            5,
            observation_space=observation_space,
            default_camera_config=DEFAULT_CAMERA_CONFIG,
            **kwargs,
        )
        
    @property
    def healthy_reward(self):
        return (
            float(self.is_healthy or self._terminate_when_unhealthy)
            * self._healthy_reward
        )

    def control_cost(self, action):
        control_cost = self._ctrl_cost_weight * np.sum(np.square(action))
        return control_cost

    @property
    def contact_forces(self):
        raw_contact_forces = self.data.cfrc_ext
        min_value, max_value = self._contact_force_range
        contact_forces = np.clip(raw_contact_forces, min_value, max_value)
        return contact_forces

    @property
    def contact_cost(self):
        contact_cost = self._contact_cost_weight * np.sum(
            np.square(self.contact_forces)
        )
        return contact_cost

    @property
    def is_healthy(self):
        state = self.state_vector()
        min_z, max_z = self._healthy_z_range
        is_healthy = np.isfinite(state).all() and min_z <= state[2] <= max_z
        return is_healthy

    @property
    def terminated(self):
        terminated = not self.is_healthy if self._terminate_when_unhealthy else False
        return terminated
    
    def step(self, action):
        xy_position_before = self.get_body_com("BODY")[:2].copy()
        self.do_simulation(action, self.frame_skip)
        xy_position_after = self.get_body_com("BODY")[:2].copy()

        xy_velocity = (xy_position_after - xy_position_before) / self.dt
        x_velocity, y_velocity = xy_velocity

        forward_reward = x_velocity
        healthy_reward = self.healthy_reward

        rewards = forward_reward + healthy_reward
        # rewards = healthy_reward

        costs = ctrl_cost = self.control_cost(action)

        terminated = self.terminated
        observation = self._get_obs()
        info = {
            "reward_forward": forward_reward,
            "reward_ctrl": -ctrl_cost,
            "reward_survive": healthy_reward,
            "x_position": xy_position_after[0],
            "y_position": xy_position_after[1],
            "distance_from_origin": np.linalg.norm(xy_position_after, ord=2),
            "x_velocity": x_velocity,
            "y_velocity": y_velocity,
            "forward_reward": forward_reward,
        }
        if self._use_contact_forces:
            contact_cost = self.contact_cost
            costs += contact_cost
            info["reward_ctrl"] = -contact_cost

        reward = rewards - costs
        # reward = rewards

        if self.render_mode == "human":
            self.render()
        return observation, reward, terminated, False, info

    def _get_obs(self):
        position = self.data.qpos.flat.copy()
        velocity = self.data.qvel.flat.copy()

        if self._exclude_current_positions_from_observation:
            position = position[2:]

        if self._use_contact_forces:
            contact_force = self.contact_forces.flat.copy()
            return np.concatenate((position, velocity, contact_force))
        else:
            return np.concatenate((position, velocity))
        
    def reset_model(self):
        noise_low = -self._reset_noise_scale
        noise_high = self._reset_noise_scale

        qpos = self.init_qpos + self.np_random.uniform(
            low=noise_low, high=noise_high, size=self.model.nq
        )
        qvel = (
            self.init_qvel 
            + self._reset_noise_scale * self.np_random.standard_normal(self.model.nv)
        )
        self.set_state(qpos, qvel)
        return self._get_obs()