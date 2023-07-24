import models
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)