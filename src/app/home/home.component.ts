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

  processorTypes =['Intel Pentium','Intel Celeron', 'Intel Core M','Intel Core i3','Intel Core i5','Intel Core i7','Intel Core i9',
                    'AMD Ryzen 3','AMD Ryzen 5','AMD Ryzen 7'
  ]

  processorSpeeds=[0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. , 1.1, 1.2,
       1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2. , 2.1, 2.2, 2.3, 2.4, 2.5,
       2.6, 2.7, 2.8, 2.9, 3. , 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8,
       3.9, 4. , 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5. ]

  processorCounts=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
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
    this.dataService.search(JSON.stringify(form.value)).subscribe(laptops => (this.laptops = laptops));

  }
}
