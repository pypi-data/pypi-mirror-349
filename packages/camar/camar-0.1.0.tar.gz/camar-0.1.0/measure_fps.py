import time
import jax
import wandb

from grid_maze2 import Grid_Maze


def make_benchmark(config):
	env = Grid_Maze(**config["ENV_KWARGS"])
	config["NUM_ACTORS"] = env.num_agents * config["NUM_ENVS"]

	def benchmark(rng):
		def init_runner_state(rng):

			# INIT ENV
			rng, _rng = jax.random.split(rng)
			reset_rng = jax.random.split(_rng, config["NUM_ENVS"])
			obsv, env_state = jax.vmap(env.reset)(reset_rng)

			return (env_state, obsv, rng)

		def env_step(runner_state, unused):
			env_state, last_obs, rng = runner_state

			# SELECT ACTION
			rng, _rng = jax.random.split(rng)
			rngs = jax.random.split(_rng, config["NUM_ENVS"]).reshape((config["NUM_ENVS"], -1))
			actions = jax.vmap(env.action_spaces.sample)(rngs)

			# STEP ENV
			rng, _rng = jax.random.split(rng)
			rng_step = jax.random.split(_rng, config["NUM_ENVS"])
			obsv, env_state, _, _, info = jax.vmap(env.step)(
				rng_step, env_state, actions
			)
			runner_state = (env_state, obsv, rng)
			return runner_state, None

		rng, init_rng = jax.random.split(rng)
		runner_state = init_runner_state(init_rng)
		runner_state = jax.lax.scan(env_step, runner_state, None, config["NUM_STEPS"])
		return runner_state

	return benchmark

for obstacle_density in range(5, 60, 5):
	obstacle_density = obstacle_density / 100
	config = {
	"NUM_STEPS": 100,
	"NUM_ENVS": 1000,
	"ACTIVATION": "relu",
	"ENV_NAME": "grid_maze",
	"NUM_SEEDS": 1,
	"SEED": 0,
	}

	config["ENV_KWARGS"] = {
	"width": 18,
	"height": 18,
	"obstacle_density": obstacle_density,
	"num_agents": 32,
	"grain_factor": 4,
	"obstacle_size": 0.4,
	"contact_force": 500,
	"contact_margin": 1e-3,
	"dt": 0.015,
	"max_steps": 100,
	}

	wandb.init(
	project="jaxmarl_fps",
	config={
		"n_runs": 5,
		"rollout_length": config["NUM_STEPS"],
		"device": str(jax.devices()[0]),
		"benchamrk_config": config
	},
	name=f"rl2/grid_maze2_a{config['ENV_KWARGS']['num_agents']}_od{config['ENV_KWARGS']['obstacle_density']}_docker"
	)

	### JAXMARL BENCHMARK
	num_envs = [1, 100, 400, 1000, 2000, 3000, 4000, 5000, 10000]
	for num in num_envs:
		try:
			config["NUM_ENVS"] = num

			total_time = 0.
			for run in range(wandb.config.n_runs):
				jax.clear_caches()
				benchmark_fn = jax.jit(make_benchmark(config))
				rng = jax.random.PRNGKey(config["SEED"])
				rng, _rng = jax.random.split(rng)\

				benchmark_jit = jax.jit(benchmark_fn).lower(_rng).compile()

				before = time.perf_counter_ns()
				runner_state = jax.block_until_ready(benchmark_jit(_rng))
				after = time.perf_counter_ns()

				total_time += (after - before) / 1e9
				
			env = Grid_Maze(**config["ENV_KWARGS"])
			# env = jaxmarl.make(config["ENV_NAME"], **config["ENV_KWARGS"])

			sps = wandb.config.n_runs * config['NUM_STEPS'] * config['NUM_ENVS'] / total_time
			ops = sps * env.num_agents

			wandb.log({"num_envs": config["NUM_ENVS"], "SPS": sps, "OPS": ops, "n_agents": env.num_agents, "n_objects": env.num_entities, "n_obstacles": env.num_obstacles})
		except:
			break

	wandb.finish()
	