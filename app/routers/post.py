from pyexpat import model
from statistics import mode
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get('/', response_model=List[schemas.postOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              search: Optional[str] = '', limit: int = 10, skip: int = 0):
    # Cursor.execute("""SELECT * FROM posts """)
    # post = Cursor.fetchall()
    # post = db.query(models.post).filter(models.post.owner_id == current_user.id).all()
    # print(search)
    # post = db.query(models.post).filter(
    #     models.post.title.contains(search)).limit(limit).offset(skip).all()
    post = db.query(models.post,
                    func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                                                         models.Vote.post_id == models.post.id,
                                                                         isouter=True).group_by(models.post.id).filter(
        models.post.title.contains(search)).limit(limit).offset(skip).all()
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.post)
def create_post(post: schemas.postCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # Cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # post = Cursor.fetchone()
    # conn.commit()
    new_post = models.post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.postOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # Cursor.execute("""SELECT * FROM posts where id = %s """, (str(id)))
    # post_search = Cursor.fetchone()
    post_search = db.query(models.post,
                           func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                                                                models.Vote.post_id == models.post.id,
                                                                                isouter=True).group_by(models.post.id).filter(models.post.id == id).first()
    if not post_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id}, record not found')
    # if post_search.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail='not authorized')
    return post_search


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # Cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = Cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.post).filter(models.post.id == id)
    post_delete = deleted_post.first()
    if post_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id}, record not found')
    if post_delete.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='not authorized')
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.post)
def update_post(id: int, post: schemas.postCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # Cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = Cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.post).filter(models.post.id == id)
    updated_post = update_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{id}, record not found')
    if updated_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='not authorized')
    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()
