import { Component, OnInit } from "@angular/core";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
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

  title: string ;




  constructor(private one_detail:DataService,
              private route:ActivatedRoute) { }
  ngOnInit() {
    //this.showDetails();
    const allData=this.route
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
