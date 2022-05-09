from app import oauth2
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

# Order of the get methods matters



@router.get("/", response_model=List[schemas.PostOut])  # List stuff is cool
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
            limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''INSERT INTO posts (title, content, published) Values (%s, %s, %s) RETURNING *''',
    #     (post.title,post.content, post.published))  #   Done like this to avoid Sequel hack
    # post_to_return = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id= current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   # int is used to check for valid id
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist")    
    return post

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id :int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform this action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user = Depends(oauth2.get_current_user)):

    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''',
    #     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    check_post = post_query.first()

    if check_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    if check_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform this action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()