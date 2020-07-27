import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfessionHomeComponent } from './confession-home.component';

describe('ConfessionHomeComponent', () => {
  let component: ConfessionHomeComponent;
  let fixture: ComponentFixture<ConfessionHomeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConfessionHomeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfessionHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
