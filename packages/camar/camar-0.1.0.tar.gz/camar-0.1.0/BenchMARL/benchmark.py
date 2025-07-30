import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

from glob import glob

from benchmarl.algorithms import MappoConfig, MasacConfig, QmixConfig
from benchmarl.benchmark import Benchmark
from benchmarl.environments import CamarTask
from benchmarl.experiment import ExperimentConfig
from benchmarl.models.mlp import MlpConfig

if __name__ == "__main__":
    # experiment aka algorithm config (rollout length, num_epochs, checkpoints, eval_episodes, etc)
    exp_yaml = glob("**/conf/experiment/mappo1.yaml", recursive=True)
    assert len(exp_yaml) == 1
    exp_yaml = exp_yaml[0]

    # Loads from "benchmarl/conf/experiment/base_experiment.yaml"
    experiment_config = ExperimentConfig.get_from_yaml(exp_yaml)

    # task aka map config
    task_yaml_name = "random_grid1"
    task_yaml = glob(f"**/conf/task/camar/{task_yaml_name}.yaml", recursive=True)
    assert len(task_yaml) == 1
    task_yaml = task_yaml[0]
    
    # Loads from "benchmarl/conf/task/vmas"
    tasks = [
        CamarTask.RANDOM_GRID.get_from_yaml(),
        CamarTask.SAMPLING.get_from_yaml()
    ]

    # Loads from "benchmarl/conf/algorithm"
    algorithm_configs = [
        MappoConfig.get_from_yaml(),
        QmixConfig.get_from_yaml(),
        MasacConfig.get_from_yaml(),
    ]

    # Loads from "benchmarl/conf/model/layers"
    model_config = MlpConfig.get_from_yaml()
    critic_model_config = MlpConfig.get_from_yaml()

    benchmark = Benchmark(
        algorithm_configs=algorithm_configs,
        tasks=tasks,
        seeds={0, 1},
        experiment_config=experiment_config,
        model_config=model_config,
        critic_model_config=critic_model_config,
    )
    benchmark.run_sequential()