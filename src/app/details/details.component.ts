import { Component, OnInit } from "@angular/core";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import { moveIn, fallIn } from "../routing.animations";
import { HttpClient } from 'selenium-webdriver/http';
import { HttpResponse } from '@angular/common/http';
@Component({
  selector: "app-details",
  templateUrl: "./details.component.html",
  styleUrls: ["./details.component.scss"],
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class DetailsComponent implements OnInit {
  constructor(private one_detail: DataService) {}

  //artikel: string[];
    public laptop= {};
   // productTitle= this.laptop.productTitle;
  //arttikel: any;
  error;

  ngOnInit() {
    this.one_detail.getLaptop_details()
      .subscribe(data => this.laptop= 1data);
      error=> this.error=error;
  }
  
}
