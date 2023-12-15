import { Component } from '@angular/core';
import {PlannerService} from "../planner.service";
import {InputService} from "../input.service";

@Component({
  selector: 'app-planer',
  templateUrl: './planer.component.html',
  styleUrls: ['./planer.component.css']
})
export class PlanerComponent {

  logMessages : string[] = []

  constructor(
      protected plannerService: PlannerService,
      protected inputService: InputService
  ) {
  }

  onClick() {
    this.logMessages = []
    this.logMessages.push("Planning...")
    for(let b of this.inputService.batchList) {
      console.log(b.toString())
      this.logMessages.push(b.toString())
    }
    this.plannerService.startPlanningProcess(this.inputService.batchList);
  }
}
