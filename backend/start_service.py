import time
from typing import Union
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fm_demo_process.fm_problem import *
from fm_demo_process.fm_process_base import get_all_objects_from_problem
from pydantic import BaseModel
from up_graphene_engine.engine import GrapheneEngine

app = FastAPI()

class Batch(BaseModel) :
   family: str
   quantity: int
   processedStock: int
   startingStockPinion: int
   startingStockGear: int

class BatchList(BaseModel):
    data: List[Batch]

class Action(BaseModel) :
    name: str
    startTime: str
    endTime: str

    def to_string(self):
        result = "[" + self.name + ", " + self.startTime + ", " + self.endTime + "]"

        return result

class Plan(BaseModel) :
    status: str = ""
    actions: List[Action] = []

    def to_string(self):
        result = "status : " + self.status + "\n" + "actions : ["
        for action in self.actions:
            result = result + action.to_string() + " ,"
        result = result[:-2] + "]"
        return result

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return  {"Hello":"World"}

# Function that returns all the existing families from the Meritor problem
@app.get("/family-list")
def get_families():
    print("received request for families")
    problem = create_fm_problem()
    (_, families, _, _) = get_all_objects_from_problem(problem)
    result = []
    for family in families:
        result.append(str(family))
    return result

# Function that calls the planner when requested and returns a plan
@app.post("/plan")
def trigger_planning(batchList: BatchList):
    print("received a planning request")
    engine = GrapheneEngine(port=8061)
    problem = create_fm_problem()
    planner = OneshotPlanner(name="tamer", params={"heuristic" : ""})
    for batch in batchList.data:
        # get the family fluent from name
        family = problem.object(batch.family)

        # We set the amount of pieces already available for this family
        print(batch.processedStock)
        print(batch.startingStockGear)
        print(batch.startingStockPinion)
        problem.set_initial_value(stock_lapped(family), batch.processedStock)

        # We set the amount of pieces we want
        problem.set_initial_value(expected_final_output(family), batch.quantity)

        # We set the starting buffer amount
        problem.set_initial_value(stock_after(step_annealing, family, piece_gear), batch.startingStockGear)
        problem.set_initial_value(stock_after(step_annealing, family, piece_pinion), batch.startingStockPinion)

        # we set the goal
        problem.add_goal(GE(stock_lapped(family), expected_final_output(family)))
        # we initialize the problem
        init_domain_from_initial_values(problem)

    # now everything is initialized, we create the plan!
    #print(mini_problem)
    #We solve the problem
    #result = engine.solve(problem, "solved_optimally")
    result = planner.solve(problem)

    # we return the plan!
    plan = Plan()
    plan.status = str(result.status)
    for a in result.plan.timed_actions:
        a_name = str(a[1])
        a_start = str(a[0])
        a_end = str(a[2])
        plan.actions.append(Action(name=a_name, startTime = a_start, endTime = a_end))

    return plan