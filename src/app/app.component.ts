import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title_1='Lenovo Yoga 530'
    manufacturer_1='Lenovo'
     details_1='(14,0 Zoll Full HD IPS Touch) Slim Convertible Notebook (Intel Core i5-8250U, 8 GB RAM, 256 GB SSD, Intel UHD Grafik 620, Windows 10 Home) schwarz'
    price_1='699'

    title_2='Apple MacBook Air '
    manufacturer_2='Apple'
     details_2='(13 Zoll, 1.8GHz dual-core Intel Core i5 Prozessor, 128 GB) - Silber'
    price_2='855'

    title_3='Microsoft Surface Book 2 34,29 cm'
    manufacturer_3='Mcirsoft'
     details_3= '(13,5 Zoll) Laptop (Intel Core i5, 8GB RAM, 256GB SSD, Intel HD Graphics 620, Win 10) silber'
    price_3='1749'


  machines=[
    {title:'Lenovo Yoga 530',
    manufacturer:'Lenovo',
     details:'(14,0 Zoll Full HD IPS Touch) Slim Convertible Notebook (Intel Core i5-8250U, 8 GB RAM, 256 GB SSD, Intel UHD Grafik 620, Windows 10 Home) schwarz',
    price:'699'
    },
    {title:'Apple MacBook Air ',
    manufacturer:'Apple',
     details:'(13 Zoll, 1.8GHz dual-core Intel Core i5 Prozessor, 128 GB) - Silber',
    price:'855'
    },
    {title:'Microsoft Surface Book 2 34,29 cm',
     manufacturer:'Microsoft',
     details:'(13,5 Zoll) Laptop (Intel Core i5, 8GB RAM, 256GB SSD, Intel HD Graphics 620, Win 10) silber',
    price:'1749'
    },
    {title:' Dell E7240',
    manufacturer:'Dell',
     details:' E7240 i5 1,9 GHz 8GB 128GB SSD Windows10 Pro Camera 12Zoll Gebraucht Mobile ',
    price:'400'
    },
  ]

  title = 'my GoalShop';
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
 
 constructor(){}

}
