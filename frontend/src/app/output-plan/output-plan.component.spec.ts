import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OutputPlanComponent } from './output-plan.component';

describe('OutputPlanComponent', () => {
  let component: OutputPlanComponent;
  let fixture: ComponentFixture<OutputPlanComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OutputPlanComponent]
    });
    fixture = TestBed.createComponent(OutputPlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
