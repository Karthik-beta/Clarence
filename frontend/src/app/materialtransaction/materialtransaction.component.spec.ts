import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaterialtransactionComponent } from './materialtransaction.component';

describe('MaterialtransactionComponent', () => {
  let component: MaterialtransactionComponent;
  let fixture: ComponentFixture<MaterialtransactionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MaterialtransactionComponent]
    });
    fixture = TestBed.createComponent(MaterialtransactionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
