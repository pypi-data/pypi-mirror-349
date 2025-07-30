from enum import Enum


class ServiceProviderEnum(Enum):
    FAL = "fal"
    REPLICATE = "replicate"


class IFalAdapter:
    def __init__(self, data: dict, skip_validation: bool = True):
        self.data = data
        self.skip_validation = skip_validation

    def convert_input(self) -> dict:
        pass
    
    def get_fal_model(self) -> str:
        pass


class IReplicateAdapter:
    def __init__(self, data: dict, skip_validation: bool = True):
        self.data = data
        self.skip_validation = skip_validation

    def convert_input(self) -> dict:
        pass
    
    def get_replicate_model(self) -> str:
        pass
