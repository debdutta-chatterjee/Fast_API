from typing import List
from fastapi import FastAPI
from pydantic import BaseModel


class Employee(BaseModel):
    lst_num :List[int]


app = FastAPI()

@app.post('/employee/{id}',response_model=Employee)
def employee(emp: Employee,id:int):
    nums = emp.lst_num
    return {f'message {id}':f'{sum(nums)}'}
