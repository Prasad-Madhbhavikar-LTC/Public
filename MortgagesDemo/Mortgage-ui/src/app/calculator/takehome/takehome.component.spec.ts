import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TakehomeComponent } from './takehome.component';

describe('TakehomeComponent', () => {
  let component: TakehomeComponent;
  let fixture: ComponentFixture<TakehomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TakehomeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TakehomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
