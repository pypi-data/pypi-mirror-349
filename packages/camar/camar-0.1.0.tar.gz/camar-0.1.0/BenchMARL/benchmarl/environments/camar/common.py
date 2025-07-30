import copy
from typing import Callable, Dict, List, Optional

from benchmarl.environments.common import Task, TaskClass
from benchmarl.utils import DEVICE_TYPING
from torchrl.data import Composite
from torchrl.envs import EnvBase

from camar.integrations import CamarEnv


class CamarClass(TaskClass):
    def get_env_fun(
        self,
        num_envs: int,
        continuous_actions: bool,
        seed: Optional[int],
        device: DEVICE_TYPING,
    ) -> Callable[[], EnvBase]:
        config = copy.deepcopy(self.config)
        return lambda: CamarEnv(
            map_generator=self.name.lower(),
            num_envs=num_envs,
            seed=seed,
            device=device,
            **config,
        )

    def supports_continuous_actions(self) -> bool:
        return True

    def supports_discrete_actions(self) -> bool:
        return False

    def has_render(self, env: EnvBase) -> bool:
        return False

    def max_steps(self, env: EnvBase) -> int:
        return self.config["max_steps"]

    def group_map(self, env: EnvBase) -> Dict[str, List[str]]:
        if hasattr(env, "group_map"):
            return env.group_map
        return {"agents": [agent.name for agent in env.agents]}

    def state_spec(self, env: EnvBase) -> Optional[Composite]:
        return None

    def action_mask_spec(self, env: EnvBase) -> Optional[Composite]:
        return None

    def observation_spec(self, env: EnvBase) -> Composite:
        observation_spec = env.full_observation_spec_unbatched.clone()
        for group in self.group_map(env):
            if "info" in observation_spec[group]:
                del observation_spec[(group, "info")]
        return observation_spec

    def info_spec(self, env: EnvBase) -> Optional[Composite]:
        # info_spec = env.full_observation_spec_unbatched.clone()
        # for group in self.group_map(env):
        #     del info_spec[(group, "observation")]
        # for group in self.group_map(env):
        #     if "info" in info_spec[group]:
        #         return info_spec
        # else:
        #     return None
        return None

    def action_spec(self, env: EnvBase) -> Composite:
        return env.full_action_spec_unbatched

    @staticmethod
    def env_name() -> str:
        return "camar"


class CamarTask(Task):
    """Enum for Camar tasks."""

    RANDOM_GRID = None
    STRING_GRID = None
    BATCHED_STRING_GRID = None
    LABMAZE_GRID = None
    MOVINGAI = None

    @staticmethod
    def associated_class():
        return CamarClass
