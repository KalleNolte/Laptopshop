import { Component, OnInit } from "@angular/core";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import { moveIn, fallIn } from "../routing.animations";

@Component({
  selector: "app-details",
  templateUrl: "./details.component.html",
  styleUrls: ["./details.component.scss"],
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class DetailsComponent implements OnInit {
  constructor() {}

  ngOnInit() {}
}
