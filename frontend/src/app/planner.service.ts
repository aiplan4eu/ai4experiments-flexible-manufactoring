import {Inject, Injectable, Input} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {combineLatest, Observable, of} from "rxjs";
import {Batch, InputService} from "./input.service";


class Plan {
  status: string = "";
  actions: Action[] = [];
}

class Action {
  name: string="";
  startTime: string="";
  endTime: string="";

  constructor(name: string, startTime: string, endTime: string) {
    this.name = name;
    this.startTime = startTime;
    this.endTime = endTime;
  }

  toString() : string {
    return "[" + this.name + ", " + this.startTime + ", " + this.endTime + "]";
  }
}

@Injectable({
  providedIn: 'root'
})
export class PlannerService {

  constructor(private http : HttpClient, private inputService : InputService) { }

  public plan : Plan = new Plan();
  public planStatus$ = of(this.plan.status)
  public planActions$ = of(this.plan.actions);
  public isPlanningOngoing$: Observable<boolean> = of(false)

  startPlanningProcess(batchList: Batch[]) {
    // first we reset the output
    this.plan = new Plan();

    // then we call the planner
    console.log("Calling the planner")
    this.isPlanningOngoing$ = of(true);

    let plannerUrl = "http://127.0.0.1:12345/plan";
    let body = {
      "data": batchList
    }
    const req = this.http.post<Plan>(plannerUrl, body);
    req.subscribe((answer : Plan) =>
    {
      console.log("Received an answer")

      this.plan.status = answer.status;
      for(let a of answer.actions) {
        this.plan.actions.push(new Action(a.name, a.startTime, a.endTime))
      }

      this.planStatus$ = of(this.plan.status);
      this.planActions$ = of(this.plan.actions);
      this.isPlanningOngoing$ = of(false)
    });
  }

  isPlanningAvailable(){
    let batchList$ = this.inputService.getBatchList();
    return combineLatest([this.isPlanningOngoing$, batchList$],
      (isPlanning, bList) => {
      return !isPlanning && bList.length > 0;
    })
  }
}
