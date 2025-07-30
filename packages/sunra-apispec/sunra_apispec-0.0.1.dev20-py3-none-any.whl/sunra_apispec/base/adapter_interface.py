from enum import Enum


class ServiceProviderEnum(Enum):
    FAL = "fal"
    REPLICATE = "replicate"
    MINIMAX = "minimax"


class IFalAdapter:
    def __init__(self):
       pass

    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        pass
    
    def get_fal_model(self) -> str:
        pass


class IReplicateAdapter:
    def __init__(self):
        pass

    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        pass
    
    def get_replicate_model(self) -> str:
        pass


class IMinimaxAdapter:
    def __init__(self):
        pass

    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        pass

    def get_request_url(self) -> str:
        pass

    def get_status_url(self, task_id: str) -> str:
        pass


BaseAdapter = IFalAdapter | IReplicateAdapter | IMinimaxAdapter
