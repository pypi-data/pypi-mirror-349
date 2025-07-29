from dataclasses import dataclass
from functools import partial
from typing import ClassVar, TypedDict


class Registry:
    def __init__(self, cls):
        self.cls = cls
        self.instances: dict[str, cls] = {}

    def __getattr__(self, name):
        if name in self.instances:
            return self.instances[name]
        return partial(self.cls, self, name)

    def __str__(self):
        return self.cls._str


registries: dict[str, Registry] = {}


@dataclass
class RegisteredDataclass:
    _str: ClassVar[str]
    _registry: Registry
    _name: str

    def __post_init__(self):
        print(f'initializing {self._registry}.{self._name}')
        #registries[]
        self._registry.instances[self._name] = self


@dataclass
class NullResource(RegisteredDataclass):
    """
    The `null_resource` resource implements the standard resource lifecycle but takes no further action.
    On Terraform 1.4 and later, use the [terraform_data resource
    type](https://developer.hashicorp.com/terraform/language/resources/terraform-data) instead.  The
    `triggers` argument allows specifying an arbitrary set of values that, when changed, will cause
    the resource to be replaced.
    """

    _str: ClassVar[str] = 'null_resource'
    _registry: Registry
    _name: str
    #: A map of arbitrary strings that, when changed, will force the null resource to be replaced,
    #: re-running any associated provisioners.
    triggers: dict[str] | None = None

    @property
    def id(self) -> str:
        """This is set to a random value at create time."""


null_resource = Registry(NullResource)


