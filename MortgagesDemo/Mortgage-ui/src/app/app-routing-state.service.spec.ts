import { TestBed } from '@angular/core/testing';

import { AppRoutingStateService } from './app-routing-state.service';

describe('AppRoutingStateService', () => {
  let service: AppRoutingStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AppRoutingStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
