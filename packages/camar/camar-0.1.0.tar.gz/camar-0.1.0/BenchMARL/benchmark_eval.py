import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["WANDB_MODE"] = "offline" # evaluation without wandb logs

from glob import glob

from baseline_utils import visualize_experiment, evaluate_experiment
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
from benchmarl.models.gru import GruConfig

if __name__ == "__main__":
    folder_name = "mappo_random_grid_mlp__899feb79_25_05_04-14_19_53"
    exp_yaml_name = (
        "mappo1"
        # "vmas_finetuned"
        # "base_experiment"
    )
    algorithm_config = (
        # IqlConfig.get_from_yaml()
        # QmixConfig.get_from_yaml()
        # VdnConfig.get_from_yaml()
        MappoConfig.get_from_yaml()
        # IppoConfig.get_from_yaml()
        # MasacConfig.get_from_yaml()
        # IsacConfig.get_from_yaml()
        # MaddpgConfig.get_from_yaml()
        # IddpgConfig.get_from_yaml()
    )
    model_config = (
        MlpConfig.get_from_yaml()
        # GruConfig.get_from_yaml()
    )
    eval_tasks_configs = [
        ("random_grid_h20_w20_a8_o0", CamarTask.RANDOM_GRID),
        ("random_grid_h20_w20_a8_o20", CamarTask.RANDOM_GRID),
        ("random_grid_h20_w20_a8_o60", CamarTask.RANDOM_GRID),
        # ("random_grid1", CamarTask.RANDOM_GRID),
        # ("random_grid2", CamarTask.RANDOM_GRID),
        # ("random_grid3", CamarTask.RANDOM_GRID),
        # ("random_grid4", CamarTask.RANDOM_GRID),
        # ("random_grid1_2", CamarTask.RANDOM_GRID),
        ("labmaze_grid_h21_w21_a8_r4-9_c0.65", CamarTask.LABMAZE_GRID),
        # ("labmaze_grid1", CamarTask.LABMAZE_GRID),
        # ("labmaze_grid3", CamarTask.LABMAZE_GRID),
        # ("labmaze_grid4", CamarTask.LABMAZE_GRID),
    ]
    vis_seeds = [
        6,
        7,
    ]

    # load exp config
    exp_yaml = glob(f"**/conf/experiment/{exp_yaml_name}.yaml", recursive=True)
    assert len(exp_yaml) == 1
    exp_yaml = exp_yaml[0]

    experiment_config = ExperimentConfig.get_from_yaml(exp_yaml)

    # add restore file
    checkpoint_names = glob(f"*/{folder_name}/checkpoints/*.pt")
    last_checkpoint_name = max(checkpoint_names,
                               key=lambda checkpoint_name: int(checkpoint_name.split("/")[-1].rstrip(".pt").split("_")[-1])
    )
    print(f"checkpoint: {last_checkpoint_name}")
    experiment_config.restore_file = last_checkpoint_name

    # save folder would be the same as for restoring
    experiment_config.save_folder = None

    for task_i, (task_yaml_name, task_config) in enumerate(eval_tasks_configs):
        print(f"evaluate: {task_yaml_name}")
        task_yaml = glob(
            f"**/conf/task/camar/{task_yaml_name}.yaml", recursive=True
        )
        assert len(task_yaml) == 1
        task_yaml = task_yaml[0]

        task = task_config.get_from_yaml(task_yaml)

        # load the entire experiment
        experiment = Experiment(
            algorithm_config=algorithm_config,
            model_config=model_config,
            seed=0, # only for training not for evalutaion
            config=experiment_config,
            task=task,
        )

        evaluate_experiment(experiment, task_yaml_name, num_envs=1000, seed=4)

        for vis_i, vis_seed in enumerate(vis_seeds):
            print(f"visualize: {task_yaml_name}, seed={vis_seed}")
            visualize_experiment(
                experiment, task_yaml_name, seed=vis_seed
            )
