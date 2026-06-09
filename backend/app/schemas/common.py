from pydantic import BaseModel, ConfigDict


class CortexSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

