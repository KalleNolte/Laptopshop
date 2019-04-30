import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Laptop } from "./laptop";
import { Observable } from 'rxjs';
import { map } from "rxjs/operators";

@Injectable({
  providedIn: "root"
})
export class DataService {
  sampleUrl = "../assets/amazonDataSample.json";
 

  constructor(private http: HttpClient) {}

  getSample(){
    return this.http.get(this.sampleUrl)
    .pipe(map((resp: Response) => resp.json()));
  }
}
