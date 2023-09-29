import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShiftstrengthComponent } from './shiftstrength.component';

describe('ShiftstrengthComponent', () => {
  let component: ShiftstrengthComponent;
  let fixture: ComponentFixture<ShiftstrengthComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShiftstrengthComponent]
    });
    fixture = TestBed.createComponent(ShiftstrengthComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
