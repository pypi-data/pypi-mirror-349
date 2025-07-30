import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

from glob import glob

from baseline_utils import visualize_experiment, LogMetricsCallback
from benchmarl.algorithms import (
    IddpgConfig,
    IppoConfig,
    IqlConfig,
    IsacConfig,
    MaddpgConfig,
    MappoConfig,
    MasacConfig,
    QmixConfig,
    VdnConfig,
)
from benchmarl.environments import CamarTask
from benchmarl.experiment import Experiment, ExperimentConfig
from benchmarl.models.mlp import MlpConfig

if __name__ == "__main__":
    exp_yaml_names = [
        "mappo1",
        # "vmas_finetuned",
        # "base_experiment",
    ]

    task_configs = [
        # ("random_grid1", CamarTask.RANDOM_GRID),
        ("random_grid_h20_w20_a32_o20", CamarTask.RANDOM_GRID),
        # ("random_grid3", CamarTask.RANDOM_GRID),
        # ("random_grid4", CamarTask.RANDOM_GRID),
        # ("labmaze_grid1", CamarTask.LABMAZE_GRID),
        ("labmaze_grid_h21_w21_a8", CamarTask.LABMAZE_GRID),
        # ("labmaze_grid4", CamarTask.LABMAZE_GRID),
    ]

    # algorithm config (loss coeffs, gae lambda, num qnets)
    # Loads from "benchmarl/conf/algorithm/*"
    algorithm_configs = [
        # IqlConfig.get_from_yaml(),
        # QmixConfig.get_from_yaml(),
        # VdnConfig.get_from_yaml(),
        MappoConfig.get_from_yaml(),
        # IppoConfig.get_from_yaml(),
        # MasacConfig.get_from_yaml(),
        # IsacConfig.get_from_yaml(),
        # MaddpgConfig.get_from_yaml(),
        # IddpgConfig.get_from_yaml(),
    ]

    train_seeds = [
        0,
        # 1,
    ]

    vis_seeds = [
        4,
        5,
    ]

    num_exps = (
        len(exp_yaml_names)
        * len(task_configs)
        * len(train_seeds)
        * len(algorithm_configs)
    )
    print("Total number of experiments =", num_exps)
    print("Total number of visualizations =", num_exps * len(vis_seeds))

    # models configs (num_layers, activation func, dropout)
    # Loads from "benchmarl/conf/model/layers/mlp.yaml"
    model_config = MlpConfig.get_from_yaml()
    critic_model_config = MlpConfig.get_from_yaml()

    for exp_i, exp_yaml_name in enumerate(exp_yaml_names):
        # experiment aka algorithm config (rollout length, num_epochs, checkpoints, eval_episodes, etc)
        exp_yaml = glob(f"**/conf/experiment/{exp_yaml_name}.yaml", recursive=True)
        assert len(exp_yaml) == 1
        exp_yaml = exp_yaml[0]

        experiment_config = ExperimentConfig.get_from_yaml(exp_yaml)

        for task_i, (task_yaml_name, task_config) in enumerate(task_configs):
            # task aka map config
            task_yaml = glob(
                f"**/conf/task/camar/{task_yaml_name}.yaml", recursive=True
            )
            assert len(task_yaml) == 1
            task_yaml = task_yaml[0]

            task = task_config.get_from_yaml(task_yaml)

            for algo_i, algorithm_config in enumerate(algorithm_configs):
                for train_i, train_seed in enumerate(train_seeds):
                    current = (
                        exp_i * len(task_configs) * len(algorithm_configs) * len(train_seeds)
                        + task_i * len(algorithm_configs) * len(train_seeds)
                        + algo_i * len(train_seeds)
                        + train_i
                        + 1
                    )
                    experiment = Experiment(
                        task=task,
                        algorithm_config=algorithm_config,
                        model_config=model_config,
                        critic_model_config=critic_model_config,
                        seed=train_seed,
                        config=experiment_config,
                        callbacks=[LogMetricsCallback()],
                    )
                    try:
                        print(
                            f"{current}/{num_exps}. Run an experiment ({exp_yaml_name=}, {task_yaml_name=}, algorithm={algorithm_config.__class__.__name__}, {train_seed=})"
                        )
                        experiment.run()

                        for vis_i, vis_seed in enumerate(vis_seeds):
                            try:
                                visualize_experiment(
                                    experiment, task_yaml_name, seed=vis_seed
                                )
                            except (Exception, KeyboardInterrupt) as e:
                                print(
                                    f"The visualization ({vis_seed=}) of the experiment ({exp_yaml_name=}, {task_yaml_name=}, algorithm={algorithm_config.__class__.__name__}, {train_seed=}) has been interrupted. {e}"
                                )
                    except (Exception, KeyboardInterrupt) as e:
                        print(
                            f"The experiment ({exp_yaml_name=}, {task_yaml_name=}, algorithm={algorithm_config.__class__.__name__}, {train_seed=}) has been interrupted. {e}"
                        )
                        experiment.close()
