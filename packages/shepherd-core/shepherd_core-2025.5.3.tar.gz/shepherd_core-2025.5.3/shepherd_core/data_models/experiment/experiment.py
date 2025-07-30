"""Config for testbed experiments."""

from collections.abc import Iterable
from datetime import datetime
from datetime import timedelta
from typing import Annotated
from typing import Optional

from pydantic import Field
from pydantic import model_validator
from typing_extensions import Self
from typing_extensions import deprecated

from shepherd_core.data_models.base.content import IdInt
from shepherd_core.data_models.base.content import NameStr
from shepherd_core.data_models.base.content import SafeStr
from shepherd_core.data_models.base.content import id_default
from shepherd_core.data_models.base.shepherd import ShpModel
from shepherd_core.data_models.testbed.target import Target
from shepherd_core.data_models.testbed.testbed import Testbed
from shepherd_core.version import version

from .observer_features import SystemLogging
from .target_config import TargetConfig


class Experiment(ShpModel, title="Config of an Experiment"):
    """Config for experiments on the testbed emulating energy environments for target nodes."""

    # General Properties
    id: int = Field(description="Unique ID", default_factory=id_default)
    # ⤷ TODO: automatic ID is problematic for identification by hash

    name: NameStr
    description: Annotated[
        Optional[SafeStr], Field(description="Required for public instances")
    ] = None
    comment: Optional[SafeStr] = None
    created: datetime = Field(default_factory=datetime.now)

    # Ownership & Access
    owner_id: Optional[IdInt] = None

    # feedback
    email_results: bool = False

    sys_logging: SystemLogging = SystemLogging()  # = all active

    # schedule
    time_start: Optional[datetime] = None  # = ASAP
    duration: Optional[timedelta] = None  # = till EOF
    abort_on_error: Annotated[bool, deprecated("has no effect")] = False

    # targets
    target_configs: Annotated[list[TargetConfig], Field(min_length=1, max_length=128)]

    # debug
    lib_ver: Optional[str] = version

    @model_validator(mode="after")
    def post_validation(self) -> Self:
        # TODO: only do deep validation with active connection to TB-client
        #       or with cached fixtures
        testbed = Testbed()  # this will query the first (and only) entry of client
        self._validate_targets(self.target_configs)
        self._validate_observers(self.target_configs, testbed)
        if self.duration and self.duration.total_seconds() < 0:
            raise ValueError("Duration of experiment can't be negative.")
        return self

    @staticmethod
    def _validate_targets(configs: Iterable[TargetConfig]) -> None:
        target_ids: list[int] = []
        custom_ids: list[int] = []
        for _config in configs:
            for _id in _config.target_IDs:
                target_ids.append(_id)
                Target(id=_id)
                # ⤷ this can raise exception for non-existing targets
            if _config.custom_IDs is not None:
                custom_ids = custom_ids + _config.custom_IDs[: len(_config.target_IDs)]
            else:
                custom_ids = custom_ids + _config.target_IDs
        if len(target_ids) > len(set(target_ids)):
            raise ValueError("Target-ID used more than once in Experiment!")
        if len(target_ids) > len(set(custom_ids)):
            raise ValueError("Custom Target-ID are faulty (some form of id-collisions)!")

    @staticmethod
    def _validate_observers(configs: Iterable[TargetConfig], testbed: Testbed) -> None:
        target_ids = [_id for _config in configs for _id in _config.target_IDs]
        obs_ids = [testbed.get_observer(_id).id for _id in target_ids]
        if len(target_ids) > len(set(obs_ids)):
            raise ValueError(
                "Observer is used more than once in Experiment -> only 1 target per observer!"
            )

    def get_target_ids(self) -> list:
        return [_id for _config in self.target_configs for _id in _config.target_IDs]

    def get_target_config(self, target_id: int) -> TargetConfig:
        for _config in self.target_configs:
            if target_id in _config.target_IDs:
                return _config
        # gets already caught in target_config - but keep:
        msg = f"Target-ID {target_id} was not found in Experiment '{self.name}'"
        raise ValueError(msg)
