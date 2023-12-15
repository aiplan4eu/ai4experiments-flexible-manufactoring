import {Component, OnInit, ViewChild} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, FormGroupDirective, Validators} from "@angular/forms";
import {MatTableDataSource} from "@angular/material/table";
import {Batch, InputService, PlanningExample} from "../input.service";


@Component({
  selector: 'app-input-info',
  templateUrl: './input-info.component.html',
  styleUrls: ['./input-info.component.css']
})
export class InputInfoComponent implements OnInit {

  inputForm : FormGroup;

  inputFormInitialValues : any;

  familyList: string[] = [];

  batchSource = new MatTableDataSource<Batch>(this.inputService.batchList)

  displayedColumns = ["family", "quantity", "stock", "startingStockPinion", "startingStockGear", "actions"]


  exampleSource = new MatTableDataSource<PlanningExample>(this.inputService.examples)
  exampleDisplayedColumns = ["exampleName", "exampleDescription", "exampleActions"]

  // TODO it seems that I have two variables for "batches", one in the service and one in the component, and it’s ugly
  // TODO see if I can make the "batch source" as an observable

  constructor(
    private inputService : InputService
  ) {
    this.inputForm = new FormGroup( {
      batchFamily : new FormControl("", [
        Validators.required,
      ]),
      quantity : new FormControl(null, [
        Validators.required,
        Validators.min(1),
      ]),
      processedStock : new FormControl(null),
      startingStockPinion : new FormControl(null, [
        Validators.required,
        Validators.min(1),
      ]),
      startingStockGear : new FormControl(null, [
        Validators.required,
        Validators.min(1),
      ])
    });

    this.inputFormInitialValues = this.inputForm.value;
  }

  onSubmit(formDirective: FormGroupDirective) : void {
    if(this.inputForm.valid) {
        // Process Batch data here
        // TODO add them in the summary element
        let processedStock = 0;
        let starting = 0;
        if (this.inputForm.value.processedStock != null) {
          processedStock = this.inputForm.value.processedStock;
        }
        if (this.inputForm.value.startingMaterialStock != null) {
          starting = this.inputForm.value.startingMaterialStock
        }

        this.inputService.addBatch(new Batch(
            this.inputForm.value.batchFamily!,
            this.inputForm.value.quantity!,
            processedStock,
            this.inputForm.value.startingStockPinion!,
            this.inputForm.value.startingStockGear!,

        )).subscribe(
          (data: Batch[]) => {
            this.batchSource.data = data;
          }
        )

        this.inputForm.reset(this.inputFormInitialValues);
        formDirective.resetForm();
    }
  }
    ngOnInit(): void {
      this.inputService.getFamilyList().subscribe((families : string[]) => {
        this.familyList = families;
      })
    }

  clearTable() {
    this.inputService.clearBatch();
    this.batchSource.data = [];
  }

  deleteRow(row: Batch) {
    this.inputService.removeBatch(row).subscribe((data: Batch[]) => {
      this.batchSource.data = data;
    });
  }

  addExample(row: PlanningExample) {
    let batch = this.inputService.addExample(row).subscribe(
      (data: Batch[] | undefined) => {
        if(data != undefined) {
          this.batchSource.data = data;
        }
      });
  }
}


