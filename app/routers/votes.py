from fastapi import HTTPException,status, Depends, APIRouter
from app import database, schemas, models, Oauth2, database
from sqlalchemy.orm import Session


router = APIRouter(prefix='/votes', tags=['Votes'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VotesBase, current_user:int = Depends(Oauth2.get_current_user), db: Session = Depends(database.get_db)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.direction == 1 ):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user_id:{current_user.id} Alredy voted on the post:{vote.post_id}')
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'voted successfully'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no post with the given_id:{vote.post_id} exists')
        vote_query.delete()
        db.commit()
        return {'message':'vote deleted successfully'}