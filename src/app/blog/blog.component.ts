import { Component, OnInit,Input } from '@angular/core';
import { Content } from '@angular/compiler/src/render3/r3_ast';
import { nbind } from 'q';

@Component({
  selector: 'app-blog',
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.scss']
})
export class BlogComponent implements OnInit {
  @Input() titre: string;
  @Input() cont: string;
  @Input() loveIt:number;
  @Input() dat: string;
  /*
  @Input() tit: string;
   @Input() cont: string;
    @Input() nbLove: number;
     @Input() datum: Date;
  
  getTit(){
    return this.tit;
  } */
 

  constructor() { }

  ngOnInit() {
  }

 compteur(){
  this.loveIt= this.loveIt-1;
  return this.loveIt;
 }

}
