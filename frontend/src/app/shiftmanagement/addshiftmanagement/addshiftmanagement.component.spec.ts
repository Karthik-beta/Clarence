import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddshiftmanagementComponent } from './addshiftmanagement.component';

describe('AddshiftmanagementComponent', () => {
  let component: AddshiftmanagementComponent;
  let fixture: ComponentFixture<AddshiftmanagementComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddshiftmanagementComponent]
    });
    fixture = TestBed.createComponent(AddshiftmanagementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
