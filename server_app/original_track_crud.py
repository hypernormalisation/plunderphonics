from typing import List
from tempfile import SpooledTemporaryFile
from sqlalchemy.orm import Session

from . import models, schemas
from uuid import uuid4

#########################################################################
# Create.
#########################################################################
def create_track(
    db: Session, 
    track_metadata: schemas.UserTrack, 
    track_binary: SpooledTemporaryFile) -> models.OriginalTrack:
    print(track_binary)
    file_name = f'/tmp/{str(uuid4())}'
    with open(file_name, 'wb') as f:
        f.write(track_binary.read())

    db_track = models.OriginalTrack(
        user_id = track_metadata["user_id"],
        url = file_name,
        name = track_metadata["name"],
        date_modified = track_metadata["date_modified"],
        date_created = track_metadata["date_created"],
    )
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def get_tracks_by_user_id(db: Session, user_id: int) -> List[models.OriginalTrack]:
    return db.query(
        models.OriginalTrack
    ).filter(models.OriginalTrack.user_id == user_id).all()
