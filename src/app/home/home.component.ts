import { Component, OnInit, ViewChild, AfterViewInit, HostListener, ElementRef } from "@angular/core";
import { NgForm } from "@angular/forms";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import { moveIn, fallIn } from "../routing.animations";
import data from "../../assets/dummyData.json";
import { MatTableDataSource, MatSort } from "@angular/material";
import { DataSource } from "@angular/cdk/table";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
  providers: [DataService],
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class HomeComponent implements OnInit, AfterViewInit {
  dummyData = <any>data;
  state: string = "";
  laptops: Laptop[] = [];
  displayedColumns: string[] = ["name", "price"];
  dataSource = new MatTableDataSource(this.dummyData);

  //laptop = new Laptop();

  @ViewChild(MatSort) sort: MatSort;

  sticky: boolean = false;
  elementPosition: any;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    //this.laptops = this.dummyData;
    this.getSample();
    // this.dataService.getSample();
    // .subscribe(data => (this.laptops = data));
    // this.dataSource = this.laptops;
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  onSubmit(form: NgForm) {
    console.log(form);
  }
  
  getSample(){
    this.dataService.getSample().subscribe(laptops => (this.laptops = laptops) );
  }
  search(form: NgForm){
    //this.brand = form['brand'];
    console.log(form.value);
    this.dataService.search(JSON.stringify(form.value)).subscribe(laptops => (this.laptops = laptops));

  }
}
