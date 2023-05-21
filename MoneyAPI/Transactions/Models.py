from pydantic import BaseModel

class TransactionShema(BaseModel):
    amount: int
    sender_id: int
    receiver_id: int
    sender_password: str