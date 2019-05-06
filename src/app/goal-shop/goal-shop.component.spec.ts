import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GoalShopComponent } from './goal-shop.component';

describe('GoalShopComponent', () => {
  let component: GoalShopComponent;
  let fixture: ComponentFixture<GoalShopComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GoalShopComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GoalShopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
