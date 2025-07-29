from jaqpot_api_client import Dataset
from pydantic import field_validator


class PatchedDataset(Dataset):
    @field_validator('result_types', mode='before')
    def set_default_result_types(cls, value):
        return value if value is not None else {}
