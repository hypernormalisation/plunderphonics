from typing import List

from sqlalchemy.orm import Session

from . import models


def get_tracks_by_user_id(db: Session, user_id: int) -> List[models.OriginalTrack]:
    return db.query(
        models.OriginalTrack
    ).filter(models.OriginalTrack.user_id == user_id).all()
