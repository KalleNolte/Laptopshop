import { Component, OnInit } from "@angular/core";
import { NgForm } from "@angular/forms";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import { moveIn, fallIn } from "../routing.animations";
import data from "../../assets/dummyData.json";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
  providers: [DataService],
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class HomeComponent implements OnInit {
  state: string = "";
  laptops: Laptop[] = [];

  dummyData = (<any>data);

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.laptops= this.dummyData;
    // this.dataService.getSample();
    // .subscribe(data => (this.laptops = data));
  }
  onSubmit(form: NgForm) {
    console.log(form);
  }
}
