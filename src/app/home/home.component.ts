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
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class HomeComponent implements OnInit, AfterViewInit {
  // dummyData = <any>data;
  state: string = "";
  laptops: Laptop[] = [];
  firstTime = true;
  displayedColumns: string[] = ["name", "price"];
  dataSource : MatTableDataSource<Laptop>;
  brands = [
    { id: "acer", name: "Acer" },
    { id: "apple", name: "Apple" },
    { id: "dell", name: "DELL" }
  ];

  chipsetBrands = [{ id: "amd", name: "AMD" }, { id: "intel", name: "Intel" }];

  screenSizes = [
    { id: 1, name: "< 25 cm (10'')" },
    { id: 2, name: "28 - 30 cm (11''-12'')" },
    { id: 3, name: "33 - 36 cm (13''-14'')" },
    { id: 4, name: "38 - 41 cm (15''-16'')" },
    { id: 5, name: "> 43 cm (17'')" }
  ];

  processorTypes = [
    { id: 2, name: "2 Cores" },
    { id: 4, name: "4 Cores" },
    { id: 6, name: "6 Cores" },
    { id: 8, name: "8 Cores" }
  ];

  processorSpeeds = [
    { id: 2, name: "< 2 GHz" },
    { id: 3, name: "< 3 GHZ" },
    { id: 4, name: "< 4 GHz" },
    { id: 5, name: "< 5 GHz" }
  ];

  hardDriveTypes = [
    { id: "hdd", name: "HDD" },
    { id: "ssd", name: "SSD" },
    { id: "hybrid", name: "Hybrid" }
  ];

  hardDriveSizes = [
    { id: 128, name: "up to 128 GB" },
    { id: 256, name: "128 - 256 GB" },
    { id: 512, name: "256 - 512 GB" },
    { id: 1, name: "512 - 1 TB" },
    { id: 2, name: "1 - 2 TB" }
  ];

  operatingSystems = [
    { id: "windows", name: "Windows" },
    { id: "macos", name: "MacOS" },
    { id: "linux", name: "Linux" }
  ];

  ramOptions = [
    { id: 2, name: "2 GB" },
    { id: 4, name: "4 GB" },
    { id: 8, name: "8 GB" },
    { id: 16, name: "16 TB" },
    { id: 32, name: "32 TB" }
  ];

  weights = [
    { id: 1, name: "< 1 kg" },
    { id: 2, name: "1 - 1.5 kg" },
    { id: 3, name: "1.5 - 2 kg" },
    { id: 4, name: "2 - 2.5 kg" },
    { id: 5, name: "> 2.5 kg" }
  ];

  widgetForm = this.fb.group({
    brandName: this.fb.group({
      brandNameValue: this.fb.array([]),
      weight: [1]
    }),
    chipsetBrand: this.fb.group({
      chipsetBrandValue: this.fb.array([]),
      weight: [1]
    }),
    screenSize: this.fb.group({
      screenSizeValue: this.fb.array([]),
      weight: [1]
    }),
    processorType: this.fb.group({
      processorTypeValue: this.fb.array([]),
      weight: [1]
    }),
    processorSpeed: this.fb.group({
      processorSpeedValue: this.fb.array([]),
      weight: [1]
    }),
    processorCount: this.fb.group({
      processorCountValue: this.fb.array([]),
      weight: [1]
    }),
    hardDriveType: this.fb.group({
      hardDriveTypeValue: this.fb.array([]),
      weight: [1]
    }),
    hardDriveSize: this.fb.group({
      hardDriveSizeValue: this.fb.array([]),
      weight: [1]
    }),
    operatingSystem: this.fb.group({
      operatingSystemValue: this.fb.array([]),
      weight: [1]
    }),
    ramSize: this.fb.group({
      ramSizeValue: this.fb.array([]),
      weight: [1]
    }),
    weight: this.fb.group({
      weightValue: this.fb.array([]),
      weight: [1]
    })
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
    if (this.dataService.firstTime) {
      this.getSample();
      this.dataService.firstTime = false;
    }else{
      this.getLaptops();
    }
    // Clear empty fields in FormArray

    // const i = this.brandNames.controls.findIndex(x => x.value === "");
    // this.brandNames.removeAt(i);
  }

  ngAfterViewInit() {
    // this.dataSource.sort = this.sort;
  }

  get brandNames() {
    return this.widgetForm.get("brandNames") as FormArray;
  }

  get processorManufacturers() {
    return this.widgetForm.get("processorManufacturers") as FormArray;
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  // touchFormFields(formGroup: FormGroup) {
  //   Object.keys(formGroup.controls).forEach(field => {
  //     const control = formGroup.get(field);
  //     if (control instanceof FormControl) {
  //       control.markAsTouched({ onlySelf: true });
  //     } else if (control instanceof FormGroup) {
  //       this.touchFormFields(control);
  //     }
  //   });
  // }

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
    this.dataService.getSample().subscribe(data => {
      this.laptops = data;
      this.dataSource = new MatTableDataSource(this.laptops);
      this.dataSource.sort = this.sort;
      });
  }

  search(form: NgForm) {
    console.log(form.value);
    this.dataService
      .search(JSON.stringify(form.value))
      .subscribe(laptops => {
        this.laptops = laptops;
        this.dataSource = new MatTableDataSource(this.laptops);
        this.dataSource.sort = this.sort;
      });
  }

  onChange(event, groupName, fieldName) {
    let field = (<FormArray>(
      this.widgetForm.controls[groupName].get(fieldName)
    )) as FormArray;

    if (event.checked) {
      field.push(new FormControl(event.source.value));
      field.markAsTouched();
      console.log("Field:" + fieldName);
    } else {
      const i = field.controls.findIndex(x => x.value === event.source.value);
      field.removeAt(i);
    }
  }

  getLaptops(){
    this.dataService.retriveLaptops().subscribe(data => {

      if (!data){
        this.getLaptops();
      }
      this.laptops = data;
      this.dataSource = new MatTableDataSource(this.laptops);
      this.dataSource.sort = this.sort;
    });
  }
}
