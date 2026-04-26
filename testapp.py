
from database import Expense, Group
from fastapi import FastAPI
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Expense


app = FastAPI()

engine = create_engine("sqlite:///ppm.db")
Session = sessionmaker(bind=engine)


class GroupInput(BaseModel):
    name: str



class ExpenseInput(BaseModel):
    payer: str
    amount: int
    description: str

@app.get("/groups")
def get_groups():

    session = Session()

    groups = session.query(Group).all()

    result = []

    for g in groups:
        result.append({
            "id": g.id,
            "name": g.name
        })

    return result

@app.post("/add-group")
def add_group(group: GroupInput):

    session = Session()

    new_group = Group(
        name=group.name
    )

    session.add(new_group)
    session.commit()

    return {"message":"Grupo creado"}

@app.get("/")
def root():
    return {"message":"PPM funcionando"}


@app.get("/expenses")
def get_expenses():

    session = Session()

    expenses = session.query(Expense).all()

    result = []

    for e in expenses:
        result.append({
            "payer": e.payer,
            "amount": e.amount,
            "description": e.description
        })

    return result


@app.post("/add-expense")
def add_expense(expense: ExpenseInput):

    session = Session()

    new_expense = Expense(
        payer=expense.payer,
        amount=expense.amount,
        description=expense.description
    )

    session.add(new_expense)
    session.commit()

    return {"message":"Gasto guardado"}


@app.get("/balance/{total}/{people}")
def balance(total:int, people:int):

    share = total / people

    return {
        "payer":"Edgar",
        "Diego_owes":share,
        "Fernando_owes":share
    }
    
    
    
    
    #lllllll
    #putito 
    #jonapiton
    