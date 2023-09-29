import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShiftskillComponent } from './shiftskill.component';

describe('ShiftskillComponent', () => {
  let component: ShiftskillComponent;
  let fixture: ComponentFixture<ShiftskillComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShiftskillComponent]
    });
    fixture = TestBed.createComponent(ShiftskillComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
