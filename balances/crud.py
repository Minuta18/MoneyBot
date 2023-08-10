from sqlalchemy.orm import Session

import init 
import models

def create_balance(db: Session, user_id: int, points: int=0):
    new_balance = models.Balance(
        points=points,
        user_id=user_id,
    )

    db.add(new_balance)
    db.commit()
    db.refresh(new_balance)
    
    return new_balance