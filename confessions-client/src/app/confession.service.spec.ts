import { TestBed } from '@angular/core/testing';

import { ConfessionService } from './confession.service';

describe('ConfessionService', () => {
  let service: ConfessionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConfessionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
