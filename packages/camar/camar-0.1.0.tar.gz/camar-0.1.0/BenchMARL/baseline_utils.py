import dataclasses
from glob import glob
import os

import torch
from benchmarl.experiment.callback import Callback
from torchrl.envs.utils import ExplorationType, set_exploration_type

from camar.render import SVG_Visualizer
import pandas as pd


def get_state_from_envs(state, env_id):
    state_data = {
        field.name: getattr(state, field.name)[env_id]
        for field in dataclasses.fields(state)
    }
    return type(state)(**state_data)


def rendering_callback(env, td):
    env.state_seq.append(get_state_from_envs(env._state, 0))


def visualize_experiment(experiment, task_yaml_name, seed=5):
    # visualize
    video_folder = glob(f"{experiment.folder_name}/**/videos/")
    assert len(video_folder) == 1
    video_folder = video_folder[0]

    with set_exploration_type(
        ExplorationType.DETERMINISTIC
        if experiment.config.evaluation_deterministic_actions
        else ExplorationType.RANDOM
    ):
        vis_env = experiment.task.get_env_fun(
            num_envs=2,
            continuous_actions=True,
            seed=seed,
            device=experiment.config.sampling_device,
        )()

        with torch.no_grad():
            vis_env.state_seq = []
            vis_env.rollout(
                auto_reset=True,
                max_steps=vis_env.max_steps + 1,
                policy=experiment.policy,
                callback=rendering_callback,
                auto_cast_to_device=True,
                break_when_any_done=False,
            )

            SVG_Visualizer(vis_env._env, vis_env.state_seq).save_svg(
                f"{video_folder}/{task_yaml_name}_{seed}.svg"
            )

class LogMetricsCallback(Callback):
    def on_evaluation_end(self, rollouts):
        # Cut rollouts at first done
        max_length_rollout_0 = 0
        for i in range(len(rollouts)):
            r = rollouts[i]
            next_done = r.get(("next", "done")).squeeze(-1)

            # First done index for this traj
            done_index = next_done.nonzero(as_tuple=True)[0]
            if done_index.numel() > 0:
                done_index = done_index[0]
                r = r[: done_index + 1]
            if i == 0:
                max_length_rollout_0 = max(r.batch_size[0], max_length_rollout_0)
            rollouts[i] = r

        mean_flowtime = []
        mean_makespan = []
        mean_coordination = []
        mean_success_rate = []
        for rollout in rollouts:

            flowtime = rollout.get(("next", "flowtime"))[-1]
            makespan = rollout.get(("next", "makespan"))[-1]
            coordination = rollout.get(("next", "coordination"))[-1]
            on_goal = rollout.get(("next", "agents", "on_goal"))[-1, :, :].squeeze(-1).to(torch.float32)

            mean_flowtime.append(flowtime)
            mean_makespan.append(makespan)
            mean_coordination.append(coordination)
            mean_success_rate.append(on_goal)

        mean_flowtime = torch.stack(mean_flowtime).nanmean()
        mean_makespan = torch.stack(mean_makespan).nanmean()
        mean_coordination = torch.stack(mean_coordination).nanmean()
        mean_success_rate = torch.stack(mean_success_rate).mean()

        self.experiment.logger.log(
            {
                "eval/mean_flowtime": mean_flowtime,
                "eval/mean_makespan": mean_makespan,
                "eval/mean_coordination": mean_coordination,
                "eval/mean_success_rate": mean_success_rate,
            },
            step=self.experiment.n_iters_performed,
        )

def evaluate_experiment(experiment, task_yaml_name, num_envs, seed):
    metric_folder = f"{experiment.folder_name}/metrics/"
    if not os.path.exists(metric_folder):
        os.makedirs(metric_folder)

    with set_exploration_type(
        ExplorationType.DETERMINISTIC
        if experiment.config.evaluation_deterministic_actions
        else ExplorationType.RANDOM
    ):
        eval_env = experiment.task.get_env_fun(
            num_envs=num_envs,
            continuous_actions=True,
            seed=seed,
            device=experiment.config.sampling_device,
        )()

        with torch.no_grad():
            eval_env.state_seq = []
            rollouts = eval_env.rollout(
                auto_reset=True,
                max_steps=eval_env.max_steps + 1,
                policy=experiment.policy,
                callback=rendering_callback,
                auto_cast_to_device=True,
                break_when_any_done=False,
            )

            SVG_Visualizer(eval_env._env, eval_env.state_seq).save_svg(
                "test3.svg"
            )

            rollouts = list(rollouts.unbind(0))

            flowtime_s = []
            makespan_s = []
            coordination_s = []
            success_rate_s = []

            # Cut rollouts at first done
            max_length_rollout_0 = 0
            for i in range(len(rollouts)):
                r = rollouts[i]
                next_done = r.get(("next", "done")).squeeze(-1)

                # First done index for this traj
                done_index = next_done.nonzero(as_tuple=True)[0]
                if done_index.numel() > 0:
                    done_index = done_index[0]
                    r = r[: done_index + 1]
                if i == 0:
                    max_length_rollout_0 = max(r.batch_size[0], max_length_rollout_0)
                rollouts[i] = r

                flowtime = r.get(("next", "flowtime"))[-1]
                makespan = r.get(("next", "makespan"))[-1]
                coordination = r.get(("next", "coordination"))[-1]
                on_goal = r.get(("next", "agents", "on_goal"))[-1, :, :].squeeze(-1).to(torch.float32)

                flowtime_s.append(flowtime.item())
                makespan_s.append(makespan.item())
                coordination_s.append(coordination.item())
                success_rate_s.append(on_goal.mean().item())

            metrics_df = pd.DataFrame({
                "flowtime": flowtime_s,
                "makespan": makespan_s,
                "coordination": coordination_s,
                "success_rate": success_rate_s,
            })
            metrics_df.to_csv(f"{metric_folder}/{task_yaml_name}.csv")
