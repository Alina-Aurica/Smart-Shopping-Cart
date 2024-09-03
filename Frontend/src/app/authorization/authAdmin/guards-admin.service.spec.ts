import { TestBed } from '@angular/core/testing';

import { GuardsAdminService } from './guards-admin.service';

describe('GuardsAdminService', () => {
  let service: GuardsAdminService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GuardsAdminService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
