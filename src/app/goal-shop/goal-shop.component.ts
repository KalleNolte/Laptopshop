import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-goal-shop',
  templateUrl: './goal-shop.component.html',
  styleUrls: ['./goal-shop.component.scss']
})
export class GoalShopComponent implements OnInit {
  @Input() tit: string;
  @Input() det: string;
  @Input() pri: number;
  constructor() { }

  ngOnInit() {
  }

}
