import { TestBed } from '@angular/core/testing';

import { GuardsClientService } from './guards-client.service';

describe('GuardsClientService', () => {
  let service: GuardsClientService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GuardsClientService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
