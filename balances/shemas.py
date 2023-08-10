import pydantic

class BalanceCreateShema(pydantic.BaseModel):
    user_id: int