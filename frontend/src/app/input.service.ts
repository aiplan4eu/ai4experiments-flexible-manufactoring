import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of, throwError} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InputService {

  examples: PlanningExample[] = [];
  batchList : Batch[];

  constructor(private http : HttpClient) {

    this.batchList = [];
    // Initializing the planning examples
    this.examples.push(new PlanningExample(
      "One Family",
      "A full planning problem for one family only. Demonstrate the full process.",
      35));

    this.examples.push(new PlanningExample(
      "Parallel Actions",
      "A problem that demonstrate the use of parallel actions",
      10
    ));

  }

  getFamilyList() : Observable<string[]>{
    const req = this.http.get<string[]>("http://127.0.0.1:12345/family-list");
    return req;
  }

  getBatchList() {
    return of(this.batchList)
  }

  addBatch(batch: Batch) : Observable<Batch[]> {
    this.batchList.push(batch)
    console.log(this.batchList)
    return of(this.batchList)
  }

  clearBatch() {
    this.batchList = [];
  }

  getBatchListAsString() : string {
    let ret = "";
    this.batchList.forEach((element) =>
      ret = ret + element.toString() + '<br />'
    )
    return ret
  }

  removeBatch(batch: Batch) : Observable<Batch[]> {
    let index = this.batchList.findIndex(b => b == batch)
    console.log(index)
    this.batchList.splice(index, 1)
    console.log(this.batchList)
    return of(this.batchList);
  }


  addExample(example : PlanningExample) : Observable<Batch[] | undefined> {
    //First we remove existing examples
    this.batchList = [];
    switch(example.name) {
      case "One Family" :
        return this.addOneFamilyFull();
      case "Parallel Actions" :
        return this.addParallelActions();
    }

    return of(undefined);

  }
  private addOneFamilyFull(): Observable<Batch[]> {
    let batch: Batch = new Batch("F1", 1, 0, 300, 300);
    return this.addBatch(batch);
  }

  private addParallelActions() : Observable<Batch[]> {
    let batch1: Batch = new Batch("F1", 10, 0, 200, 250);
    let batch2: Batch = new Batch("F2", 10, 0, 200, 150);
    this.addBatch(batch1);
    this.addBatch(batch2);
    return of(this.batchList)
  }
}

export class Batch {
  family: string;
  quantity: number;
  processedStock: number;
  startingStockPinion: number;
  startingStockGear: number;

  constructor(family: string, quantity: number, processedStock: number, startingStockPinion: number, startingStockGear: number) {
    this.family = family;
    this.quantity = quantity;
    this.processedStock = processedStock;
    this.startingStockPinion = startingStockPinion;
    this.startingStockGear = startingStockGear;
  }

  public toString(): string {
    return `Family: ${this.family}, Quantity: ${this.quantity}, Stock: ${this.processedStock}, Starting stock pinion: ${this.startingStockPinion}, Starting stock gear: ${this.startingStockGear}`;
  }
}

export class PlanningExample {
  name: string = "";
  description: string = "";
  planningTime: number = 0;

  constructor(name:string, description: string, planningTime: number) {
    this.name = name;
    this.description = description;
    this.planningTime = planningTime
  }
}
