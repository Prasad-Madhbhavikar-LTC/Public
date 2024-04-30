import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StampdutyComponent } from './stampduty.component';

describe('StampdutyComponent', () => {
  let component: StampdutyComponent;
  let fixture: ComponentFixture<StampdutyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [StampdutyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StampdutyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
