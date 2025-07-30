import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

from glob import glob

from baseline_utils import visualize_experiment
from benchmarl.algorithms import MappoConfig
from benchmarl.environments import CamarTask
from benchmarl.experiment import Experiment, ExperimentConfig
from benchmarl.models.mlp import MlpConfig

if __name__ == "__main__":
    # experiment aka algorithm config (rollout length, num_epochs, checkpoints, eval_episodes, etc)
    exp_yaml = glob("**/conf/experiment/mappo1.yaml", recursive=True)
    assert len(exp_yaml) == 1
    exp_yaml = exp_yaml[0]

    experiment_config = ExperimentConfig.get_from_yaml(exp_yaml)

    # task aka map config
    task_yaml_name = "random_grid1"
    task_yaml = glob(f"**/conf/task/camar/{task_yaml_name}.yaml", recursive=True)
    assert len(task_yaml) == 1
    task_yaml = task_yaml[0]

    task = CamarTask.RANDOM_GRID.get_from_yaml(task_yaml)

    # algorithm config (loss coeffs, gae lambda, num qnets)
    # Loads from "benchmarl/conf/algorithm/mappo.yaml"
    algorithm_config = MappoConfig.get_from_yaml()

    # models configs (num_layers, activation func, dropout)
    # Loads from "benchmarl/conf/model/layers/mlp.yaml"
    model_config = MlpConfig.get_from_yaml()
    critic_model_config = MlpConfig.get_from_yaml()

    experiment = Experiment(
        task=task,
        algorithm_config=algorithm_config,
        model_config=model_config,
        critic_model_config=critic_model_config,
        seed=0,
        config=experiment_config,
    )
    experiment.run()

    visualize_experiment(experiment, task_yaml_name, seed=5)