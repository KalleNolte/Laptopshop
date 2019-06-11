import {
  Component,
  OnInit,
  ViewChild,
  AfterViewInit,
  HostListener,
  ElementRef
} from "@angular/core";
import { FormBuilder, FormGroup, FormControl, FormArray } from "@angular/forms";
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
  brands = [
    { id: "acer", name: "Acer" },
    { id: "apple", name: "Apple" },
    { id: "dell", name: "DELL" }
  ];

  manufacturers = [{ id: "intel", name: "Intel" }, { id: "amd", name: "AMD" }];

  widgetForm = this.fb.group({
    brandSlider: ["1"],
    brandNames: this.fb.array([]),
    processorManufacturerSlider: ["1"],
    processorManufacturers: this.fb.array([]),
  });
   globalForm = new FormGroup({
    globalSearch: new FormControl()
  });

  @ViewChild(MatSort) sort: MatSort;

  sticky: boolean = false;
  elementPosition: any;

  constructor(private dataService: DataService, private fb: FormBuilder) {}

  ngOnInit() {
    //this.laptops = this.dummyData;
    this.getSample();

    // Clear empty fields in FormArray

    // const i = this.brandNames.controls.findIndex(x => x.value === "");
    // this.brandNames.removeAt(i);
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  get brandNames() {
    return this.widgetForm.get("brandNames") as FormArray;
  }

  get processorManufacturers() {
    return this.widgetForm.get("processorManufacturers") as FormArray;
  }

  addBrandName() {
    this.brandNames.push(this.fb.control("Acer"));
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  touchFormFields(formGroup: FormGroup) {
    Object.keys(formGroup.controls).forEach(field => {
      const control = formGroup.get(field);
      if (control instanceof FormControl) {
        control.markAsTouched({ onlySelf: true });
      } else if (control instanceof FormGroup) {
        this.touchFormFields(control);
      }
    });
  }

  submitFormControls(formGroup: FormGroup) {
    console.log(formGroup.controls);
  }

  onSubmit() {
    if (this.widgetForm.touched) {
      console.log(this.widgetForm.value);
    }

    if (this.globalForm.touched) {
      console.log(this.globalForm.value);
    }
  }
  getSample() {
    this.dataService.getSample().subscribe(data => (this.laptops = data));
  }

  search(form: NgForm) {
    console.log(form.value);
    this.dataService
      .search(JSON.stringify(form.value))
      .subscribe(laptops => (this.laptops = laptops));
  }

  onChange(event, fieldName) {
    let field = (<FormArray>this.widgetForm.get(fieldName)) as FormArray;

    if (event.checked) {
      field.push(new FormControl(event.source.value));
      this.widgetForm.get(fieldName).markAsTouched();
      console.log("Field:" + fieldName);
    } else {
      const i = field.controls.findIndex(x => x.value === event.source.value);
      field.removeAt(i);
    }
  }
}
