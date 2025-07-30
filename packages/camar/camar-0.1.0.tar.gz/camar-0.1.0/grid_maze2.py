import jax
import jax.numpy as jnp
import chex
from flax import struct
from typing import Tuple, Dict, Optional
from functools import partial


class Box:
	"""
	Minimal jittable class for array-shaped gymnax spaces.
	TODO: Add unboundedness - sampling from other distributions, etc.
	"""
	def __init__(
		self,
		low: float,
		high: float,
		shape: Tuple[int],
		dtype: jnp.dtype = jnp.float32,
	):
		self.low = low
		self.high = high
		self.shape = shape
		self.dtype = dtype

	def sample(self, rng: chex.PRNGKey) -> chex.Array:
		"""Sample random action uniformly from 1D continuous range."""
		return jax.random.uniform(
			rng, shape=self.shape, minval=self.low, maxval=self.high
		).astype(self.dtype)

	def contains(self, x: jnp.int_) -> bool:
		"""Check whether specific object is within space."""
		# type_cond = isinstance(x, self.dtype)
		# shape_cond = (x.shape == self.shape)
		range_cond = jnp.logical_and(
			jnp.all(x >= self.low), jnp.all(x <= self.high)
		)
		return range_cond


@struct.dataclass
class State:

    agent_pos: chex.Array  # [num_entities, [x, y]]
    agent_vel: chex.Array  # [n, [x, y]]
    goal_pos: chex.Array  # [num_agents, [x, y]]
    obstacle_pos: chex.Array # [num_obstacles, [x, y]]
    landmark_pos: chex.Array # [num_landmarks, [x, y]]
    
    # agent_agent_dist: chex.Array # [num_agents, num_agents]
    # agent_landmark_dist: chex.Array # [num_agents, num_landmarks]

    done: chex.Array  # bool [num_agents, ]
    step: int  # current step


class Grid_Maze:
    def __init__(
        self,
        width: int = 19,
        height: int = 19,
        obstacle_density: float = 0.2,
        num_agents: int = 8,
        grain_factor: int = 4,
        obstacle_size: float = 0.4,
        goal_size: float = 0.04,
        window_rad: int = 2,
        placeholder: float = -100.0,
        max_steps: int = 100,
        dt: float = 0.02,
        damping: float = 0.25,
        contact_force: float|int = 500,
        contact_margin: float = 0.001,
        **kwargs,
    ):
        self.grain_factor = grain_factor
        self.obstacle_size = obstacle_size
        self.goal_size = goal_size
        self.window = obstacle_size * window_rad
        self.num_agents = num_agents

        self.num_obstacles = int(obstacle_density * width * height)

        self.obs_placeholder = jnp.full(shape=(self.num_obstacles, 2), fill_value=placeholder)

        self.num_landmarks = self.num_obstacles * 4 * (self.grain_factor - 1) + (width + height) * 2 * (self.grain_factor - 1)
        self.num_entities = self.num_agents + self.num_landmarks

        self.agent_range = jnp.arange(0, self.num_agents)
        self.landmark_range = jnp.arange(self.num_agents, self.num_entities)
        self.entity_range = jnp.arange(0, self.num_entities)

        half_width = width * self.obstacle_size / 2
        half_height = height * self.obstacle_size / 2

        x_coords = jnp.linspace(
            - half_width + self.obstacle_size / 2, # start
            half_width - self.obstacle_size / 2, # end
            width # map width
        )
        y_coords = jnp.linspace(
            - half_height + self.obstacle_size / 2, # start
            half_height - self.obstacle_size / 2, # end
            height # map height
        )

        self.map_coordinates = jnp.stack(jnp.meshgrid(x_coords, y_coords), axis=-1).reshape(-1, 2)
        self.border_landmarks = self.get_border_landmarks(width, height, half_width, half_height, self.grain_factor)

        self.landmark_rad = self.obstacle_size / (2 * (self.grain_factor - 1))
        self.agent_rad = (self.obstacle_size - 2 * self.landmark_rad) * 0.4

        self.rad = jnp.concatenate(
                [jnp.full((self.num_agents), self.agent_rad), 
                 jnp.full((self.num_landmarks), self.landmark_rad)]
            )
        
        self.action_spaces = Box(low=0.0, high=1.0, shape=(num_agents, 5))
        self.observation_spaces = Box(-jnp.inf, jnp.inf, (num_agents, 4))
        self.action_decoder = self._decode_continuous_action
        
        self.colour = [(115, 243, 115) for i in jnp.arange(self.num_agents)] + [(64, 64, 64) for i in jnp.arange(self.num_landmarks)]

        # Environment parameters
        self.max_steps = max_steps
        self.dt = dt

        self.mass = kwargs.get("mass", 1.0)
        self.accel = kwargs.get("accel", 5.0)
        self.max_speed = kwargs.get("max_speed", -1)
        self.u_noise = kwargs.get("u_noise", 0)

        self.damping = damping
        self.contact_force = contact_force
        self.contact_margin = contact_margin

    @property
    def name(self) -> str:
        """Environment name."""
        return type(self).__name__
    
    def get_border_landmarks(self, width, height, half_width, half_height, grain_factor):
        top_wall = jnp.stack(
            (
                jnp.linspace(- half_width, # start
                             half_width, # end
                             width * (grain_factor - 1), # num points
                             endpoint=False),
                jnp.full((width * (grain_factor - 1), ), # num points
                         half_height), # y coord of the top wall
            ),
            axis=-1
        )
        right_wall = jnp.stack(
            (
                jnp.full((height * (grain_factor - 1), ), # num points
                         half_width), # x coord of the right wall
                jnp.linspace(half_height, # start
                             - half_height, # end
                             height * (grain_factor - 1), # num points
                             endpoint=False),
            ),
            axis=-1
        )
        bottom_wall = jnp.stack(
            (
                jnp.linspace(half_width, # start
                             - half_width, # end
                             width * (grain_factor - 1), # num points
                             endpoint=False),
                jnp.full((width * (grain_factor - 1), ), # num points
                         - half_height), # y coord of the bottom wall
            ),
            axis=-1
        )
        left_wall = jnp.stack(
            (
                jnp.full((height * (grain_factor - 1), ), # num points
                         - half_width), # x coord of the left wall
                jnp.linspace(- half_height, # start
                             half_height, # end
                             height * (grain_factor - 1), # num points
                             endpoint=False),
            ),
            axis=-1
        )
        return jnp.concatenate([top_wall, right_wall, left_wall, bottom_wall])

    @partial(jax.jit, static_argnums=(0,))
    def step(
        self,
        key: chex.PRNGKey,
        state: State,
        actions: Dict[str, chex.Array],
        reset_state: Optional[State] = None,
    ) -> Tuple[Dict[str, chex.Array], State, Dict[str, float], Dict[str, bool], Dict]:
        """
        Performs step transitions in the environment. Resets the environment if done.
        To control the reset state, pass `reset_state`. Otherwise, the environment will reset randomly.
        """

        key, key_reset = jax.random.split(key)
        obs_st, states_st, rewards, dones, infos = self.step_env(key, state, actions)

        if reset_state is None:
            obs_re, states_re = self.reset(key_reset)
        else:
            states_re = reset_state
            obs_re = self.get_obs(states_re)

        # Auto-reset environment based on termination
        states = jax.tree.map(
            lambda x, y: jax.lax.select(dones["__all__"], x, y), states_re, states_st
        )
        obs = jax.tree.map(
            lambda x, y: jax.lax.select(dones["__all__"], x, y), obs_re, obs_st
        )
        return obs, states, rewards, dones, infos

    @partial(jax.jit, static_argnums=[0])
    def step_env(self, key: chex.PRNGKey, state: State, actions: dict):
        # actions (num_agents, 5)
        u = self._decode_continuous_action(actions)

        key, key_w = jax.random.split(key)
        agent_pos, agent_vel = self._world_step(key_w, state, u)

        done = jnp.full((self.num_agents, ), state.step >= self.max_steps)

        state = state.replace(
            agent_pos=agent_pos,
            agent_vel=agent_vel,
            done=done,
            step=state.step + 1,
        )

        reward = self.rewards(state)

        obs = self.get_obs(state)

        info = {}

        dones = {"__all__": jnp.all(done)}

        return obs, state, reward, dones, info

    @partial(jax.jit, static_argnums=[0])
    def reset(self, key: chex.PRNGKey) -> Tuple[chex.Array, State]:
        """Initialise with random positions"""
        permuted_pos = jax.random.permutation(key, self.map_coordinates)

        agent_pos = jax.lax.dynamic_slice(permuted_pos, # [0 : num_agents, 0 : 2]
                                          start_indices=(0,               0),
                                          slice_sizes=  (self.num_agents, 2))
        
        obstacle_pos = jax.lax.dynamic_slice(permuted_pos, # [num_agents : num_agents + num_obstacles, 0 : 2]
                                             start_indices=(self.num_agents,    0),
                                             slice_sizes=  (self.num_obstacles, 2))
        
        goal_pos = jax.lax.dynamic_slice(permuted_pos, # [num_agents + num_obstacles : 2 * num_agents + num_obstacles, 0 : 2]
                                         start_indices=(self.num_agents + self.num_obstacles, 0),
                                         slice_sizes=  (self.num_agents,                      2))

        @partial(jax.vmap, in_axes=[0, None, None], out_axes=1)
        def get_landmarks(obstacle, grain_factor, obstacle_size):
            left_x, down_y = obstacle - obstacle_size / 2
            right_x, up_y = obstacle + obstacle_size / 2
            
            up_landmarks = jnp.stack((jnp.linspace(left_x, right_x, grain_factor - 1, endpoint=False), jnp.full((grain_factor - 1, ), up_y)), axis=-1)
            right_landmarks = jnp.stack((jnp.full((grain_factor - 1, ), right_x), jnp.linspace(up_y, down_y, grain_factor - 1, endpoint=False)), axis=-1)
            down_landmarks = jnp.stack((jnp.linspace(right_x, left_x, grain_factor - 1, endpoint=False), jnp.full((grain_factor - 1, ), down_y)), axis=-1)
            left_landmarks = jnp.stack((jnp.full((grain_factor - 1, ), left_x), jnp.linspace(down_y, up_y, grain_factor - 1, endpoint=False)), axis=-1)

            return jnp.concatenate([up_landmarks, right_landmarks, down_landmarks, left_landmarks])
        
        landmark_pos = get_landmarks(obstacle_pos, self.grain_factor, self.obstacle_size).reshape(-1, 2)

        all_landmark_pos = jnp.concatenate(
            [
                landmark_pos,
                self.border_landmarks,
            ]
        )

        state = State(
            agent_pos=agent_pos,
            agent_vel=jnp.zeros((self.num_agents, 2)),
            goal_pos=goal_pos,
            obstacle_pos=obstacle_pos,
            landmark_pos=all_landmark_pos,
            done=jnp.full((self.num_agents), False),
            step=0,
        )

        return self.get_obs(state), state
    
    @partial(jax.vmap, in_axes=[None, 0, None])
    def get_dist(self, a_pos: chex.Array, p_pos: chex.Array):
        return jnp.linalg.norm(a_pos - p_pos, axis=-1)

    @partial(jax.jit, static_argnums=[0])
    def get_obs(self, state: State) -> Dict[str, chex.Array]:
        """Return dictionary of agent observations"""

        @partial(jax.vmap, in_axes=[0, None])
        def _observation(idx_a: int, state: State) -> jnp.ndarray:
            """Return observation for agent i."""
            relative_pos = state.agent_pos[idx_a] - state.obstacle_pos

            in_window = (jnp.abs(relative_pos) <= self.window).all(axis=-1)

            mask = jnp.stack((in_window, in_window), axis=-1)

            return jax.lax.select(mask, state.obstacle_pos, self.obs_placeholder)

        obs = _observation(self.agent_range, state)
        return obs

    def rewards(self, state: State) -> Dict[str, float]:
        """Assign rewards for all agents"""

        goal_dist = jnp.linalg.norm(state.agent_pos - state.goal_pos, axis=-1)
        on_goal = goal_dist < self.goal_size

        agent_dist = self.get_dist(state.agent_pos, jnp.vstack((state.landmark_pos, state.agent_pos)))

        collision = (jnp.min(agent_dist, axis=1) < 0.005).astype(jnp.float32)

        r = 100.0 * on_goal.all(axis=0).astype(jnp.float32) + 10.0 * on_goal.astype(jnp.float32) - 0.001 * goal_dist - 1 * collision
        return r

    @partial(jax.vmap, in_axes=[None, 0])
    def _decode_continuous_action(
        self, action: chex.Array
    ) -> Tuple[chex.Array, chex.Array]:
        u = jnp.array([action[2] - action[1], action[4] - action[3]])
        u = u * self.accel
        return u

    def _world_step(self, key: chex.PRNGKey, state: State, u: chex.Array):
        # apply agent physical controls
        key_noise = jax.random.split(key, self.num_agents)
        agent_force = self._apply_action_force(key_noise, u)

        # apply environment forces
        agent_force = self._apply_environment_force(agent_force, state)

        # integrate physical state
        agent_pos, agent_vel = self._integrate_state(agent_force, state.agent_pos, state.agent_vel)

        return agent_pos, agent_vel

    # gather agent action forces
    @partial(jax.vmap, in_axes=[None, 0, 0])
    def _apply_action_force(
        self,
        key: chex.PRNGKey,
        u: chex.Array,
    ):
        noise = jax.random.normal(key, shape=u.shape) * self.u_noise
        return u + noise

    @partial(jax.vmap, in_axes=[None, 0, 0, 0])
    def _integrate_state(self, force, pos, vel):
        """integrate physical state"""

        pos += vel * self.dt
        vel = vel * (1 - self.damping)

        vel += (force / self.mass) * self.dt

        speed = jnp.linalg.norm(vel, ord=2)
        over_max = vel / speed * self.max_speed

        vel = jax.lax.select((speed > self.max_speed) & (self.max_speed >= 0), over_max, vel)

        return pos, vel

    def _apply_environment_force(self, agent_force: chex.Array, state: State):

        # agent - agent
        agent_idx_i, agent_idx_j = jnp.triu_indices(self.num_agents, k=1)
        agent_forces = self._get_collision_force(state.agent_pos[agent_idx_i], state.agent_pos[agent_idx_j], self.agent_rad + self.agent_rad) # (num_agents * (num_agents - 1) / 2, 2)

        agent_force = agent_force.at[agent_idx_i].add(agent_forces)
        agent_force = agent_force.at[agent_idx_j].add(- agent_forces)

        # agent - landmark
        agent_idx = jnp.repeat(jnp.arange(self.num_agents), self.num_landmarks)
        landmark_idx = jnp.tile(jnp.arange(self.num_landmarks), self.num_agents)
        landmark_forces = self._get_collision_force(state.agent_pos[agent_idx], state.landmark_pos[landmark_idx], self.agent_rad + self.landmark_rad) # (num_agents * num_landmarks, 2)

        agent_force = agent_force.at[agent_idx].add(landmark_forces)

        return agent_force

    @partial(jax.vmap, in_axes=[None, 0, 0, None])
    def _get_collision_force(self, pos_a: chex.Array, pos_b: chex.Array, min_dist: float):
        delta_pos = pos_a - pos_b

        dist = jnp.linalg.norm(delta_pos, axis=-1)

        # softmax penetration
        k = self.contact_margin
        penetration = jnp.logaddexp(0, -(dist - min_dist) / k) * k
        force = self.contact_force * delta_pos / jax.lax.select(dist > 0, dist, jnp.full(dist.shape, 1e-8)) * penetration

        return force
