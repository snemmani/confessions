import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfessionsHomeComponent } from './confessions-home.component';

describe('ConfessionsHomeComponent', () => {
  let component: ConfessionsHomeComponent;
  let fixture: ComponentFixture<ConfessionsHomeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConfessionsHomeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfessionsHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
