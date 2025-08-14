from typing import Optional
from sqlalchemy import Column,Integer,String,Boolean,DateTime,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from datetime import datetime
from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel

app=FastAPI()
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

class Todo(Base):
    __tablename__='todo'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(200),nullable=False)
    description=Column(String(500),nullable=True)
    completed=Column(Boolean,nullable=False,default=False)
    date_created=Column(DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"Todo {self.id}"

Base.metadata.create_all(bind=engine)

class TodoBase(BaseModel):
    #This define what data structure is accepted and return in API request/response
    name:str
    description:str
    completed:bool=False

class TodoCreate(TodoBase):
    pass

class TodoDelete(BaseModel):
    Success:str

class TodoUpdate(BaseModel):
    #Use for partial update 
    name:Optional[str]=None
    description:Optional[str]=None
    completed:Optional[bool]=None

class TodoResponse(TodoBase):
    id:int
    date_created:datetime
    class config:
        orm_mode=True

@app.get('/')
def testFunc():
    return "Hello world"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/",response_model=TodoResponse)
def CreateTodo(todo:TodoCreate,db:Session=Depends(get_db)):  #receive json payload validated againts Todocreate
    todo=Todo(name=todo.name,description=todo.description,completed=todo.completed)
    db.add(todo)
    db.commit()
    db.refresh(todo) #refresh db to get generated field
    return todo

@app.get("/todos",response_model=list[TodoResponse])
def GetTodo(db:Session=Depends(get_db)):
    todo_all=db.query(Todo).all()  
    return todo_all

@app.get("/todo/{todo_id}",response_model=TodoResponse)
def getTodoById(todo_id:int,db:Session=Depends(get_db)):
        todo=db.query(Todo).get(todo_id)
        if todo is None:
            raise HTTPException(status_code=404,detail='todo not found')
        return todo

@app.delete("/todos/{todo_id}",response_model=TodoDelete)
def DeleteTodo(todo_id:int,db:Session=Depends(get_db)):
    try:
        todo=db.query(Todo).get(todo_id)
        db.delete(todo)
        db.commit()
        return {"Success":"Todo deleted"}
    except:
        raise HTTPException(status_code=404,detail='todo not found')   

@app.put("/todos/{todo_id}",response_model=TodoResponse)
def UpdateTodo(todo_id:int,todo_data:TodoUpdate,db:Session=Depends(get_db)):
        todo=db.query(Todo).get(todo_id)
        print(todo)
        if todo is None:
            raise HTTPException(status_code=404,detail='todo not found')  
        for key, value in todo_data.dict(exclude_unset=True).items(): 
            #exclude_unset=True means only fields provided in the request are updated
            setattr(todo, key, value)
        db.commit()
        db.refresh(todo)
        return todo    
         
