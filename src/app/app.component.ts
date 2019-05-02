import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'my Blog';

  

  mypost=[
    {tel: 'Mon premier post',
    content:'Information : je vous conseille d utiliser Bootstrap pour cet exercice.  Si vous créez des list-group-item dans un list-group, vous avez les classes list-group-item-success et list-group-item-danger pour colorer les item.',
    loveIts: 5,
    create_at:'11/24/2017, 11:00 AM'
    },
    {
     tel: 'Mon deuxieme post',
    content:'Information : je vous conseille d utiliser Bootstrap pour cet exercice.  Si vous créez des list-group-item dans un list-group, vous avez les classes list-group-item-success et list-group-item-danger pour colorer les item.',
    loveIts: 3,
    create_at:'11/24/2017, 11:00 AM'
    },
    {tel: 'Encore post',
    content:'Information : je vous conseille d utiliser Bootstrap pour cet exercice.  Si vous créez des list-group-item dans un list-group, vous avez les classes list-group-item-success et list-group-item-danger pour colorer les item.',
    loveIts: 0,
    create_at:'11/24/2017, 11:00 AM'}
  ]
  

}
