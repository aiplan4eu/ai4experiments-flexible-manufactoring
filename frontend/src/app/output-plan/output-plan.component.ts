import { Component } from '@angular/core';
import {PlannerService} from "../planner.service";

@Component({
  selector: 'app-output-plan',
  templateUrl: './output-plan.component.html',
  styleUrls: ['./output-plan.component.css']
})
export class OutputPlanComponent {

  constructor(
    public planner : PlannerService
  ) { }



}
