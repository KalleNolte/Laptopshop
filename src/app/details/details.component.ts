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
  hardDriveType: string;
  displaySize: number;
  operatingSystem: string;
  screenResoultionSize: screenResolutionSize;
  imagePath: string;



  constructor(private one_detail:DataService,
              private route:ActivatedRoute,
              private  homeFeatures:HomeComponent) { }
  ngOnInit() {
    //this.showDetails();
    //const allData=this.route
    const asin=this.route.snapshot.params['asin'];
    this.productTitle= this.homeFeatures.getLaptopByAsin(asin).productTitle;
    this.brandName=this.homeFeatures.getLaptopByAsin(asin).brandName;
    this.ram=this.homeFeatures.getLaptopByAsin(asin).ram;
    this.hardDriveType=this.homeFeatures.getLaptopByAsin(asin).hardDriveType;
    this.displaySize=this.homeFeatures.getLaptopByAsin(asin).displaySize;
    this.operatingSystem=this.homeFeatures.getLaptopByAsin(asin).operatingSystem;
    this.imagePath=this.homeFeatures.getLaptopByAsin(asin).imagePath;
    this.screenResoultionSize=this.homeFeatures.getLaptopByAsin(asin).screenResoultionSize;

    //console.log( this.homeFeatures.getLaptopByAsin(id).productTitle);
  }

   showDetails(){
    this.one_detail.getLaptop_details()
      .subscribe(data => this.laptop= data);
      error=> this.error=error;
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
