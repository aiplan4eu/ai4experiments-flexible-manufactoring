import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlanerComponent } from './planer.component';

describe('PlanerComponent', () => {
  let component: PlanerComponent;
  let fixture: ComponentFixture<PlanerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PlanerComponent]
    });
    fixture = TestBed.createComponent(PlanerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
