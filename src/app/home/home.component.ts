import { Component, OnInit } from "@angular/core";
import { NgForm } from "@angular/forms";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import "../../assets/amazonDataSample.json";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
  providers: [DataService]
})
export class HomeComponent implements OnInit {
  laptops: Laptop[] = [
    {
      productTitle: "Dell XPS 13",
      price: 1000
    },
    { productTitle: "Apple Mac Book Pro"
    , price: 1000 }
  ];

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.dataService.getSample();
    // .subscribe(data => (this.laptops = data));
  }
  onSubmit(form: NgForm) {
    console.log(form);
  }
}
