import {Component, Input, OnInit} from "@angular/core";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import {HomeComponent} from "../home/home.component";
import { moveIn, fallIn } from "../routing.animations";

import { HttpClient } from 'selenium-webdriver/http';
import { HttpResponse } from '@angular/common/http';
import {FormsModule, NgForm} from '@angular/forms';
import { NgModule }      from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: "app-details",
  templateUrl: "./details.component.html",
  styleUrls: ["./details.component.scss"],
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class DetailsComponent implements OnInit {

  laptop: Laptop[]=[];
  error;
  var;

  productTitle: string ;
  brandName: string;
  ram: number;
  rec:any;
  laptops: Laptop[]=[];
  private item:any=[];

  constructor(private one_detail:DataService,
              private route:ActivatedRoute,
              private  homeFeatures:HomeComponent) { }
  ngOnInit() {
    //this.showDetails();
    //const allData=this.route
    const asin=this.route.snapshot.params['asin'];
    //this.getSample();
    console.log(asin);
    this.getByAsin(asin);
    console.log(this.homeFeatures.getSample())

  }
  getSample(){
    this.one_detail.getSample().subscribe(laptops => { (this.laptops = laptops);  console.log(this.laptops) });

  }

   showDetails(){
    this.one_detail.getLaptop_details()
      .subscribe(data => this.laptop= data);
      error=> this.error=error;
  }

  getByAsin(asin:string) {
   this.one_detail.getSample().subscribe(laptops =>
   {

     (this.laptops = laptops);
     this.item=
         this.laptops.find(
          laptopObject =>{

            return laptopObject.asin === asin;


          } )
            console.log(this.item)
 /*
     (this.laptops = laptops);
     this.item
       .push(
         this.laptops.filter(
          laptopObject =>{

            laptopObject.asin === asin
            console.log(this.item)
          }))
      */
    } );

    }

getByAsin_1(asin:string) {
    //console.log(this.one_detail.search(this.item) )
   this.one_detail.array_laptops.subscribe(laptops =>
   {

     (this.laptops = laptops);
     this.item=
         this.laptops.find(
          laptopObject =>{

            return laptopObject.asin === asin;


          } )
            console.log(this.item)
 /*
     (this.laptops = laptops);
     this.item
       .push(
         this.laptops.filter(
          laptopObject =>{

            laptopObject.asin === asin
            console.log(this.item)
          }))
      */
    } );

    }

}


 /*
 laptop :Laptop[]= [];

  public lap={};

  showDetails(){
    this.one_detail.getLaptop_details()
      .subscribe(data => this.laptop= data);
      error=> this.error=error;
  }
  searchD(formDetails: NgForm){
    this.one_detail.setLaptop_details(JSON.stringify(formDetails.value))
      .subscribe(data => (this.lap = data));
  }
 * */
