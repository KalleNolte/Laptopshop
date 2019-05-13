import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Laptop } from "./laptop";
import { Observable } from 'rxjs';
import { map } from "rxjs/operators";

@Injectable({
  providedIn: "root"
})
export class DataService {
  //sampleUrl = "../assets/amazonDataSample.json";
 
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      // 'Authorization': 'my-auth-token'
    })
  };

  constructor(private http: HttpClient) {}

  getSample(): Observable<Laptop[]>{
    return this.http.get<Laptop[]>('/api/sample')
  }

  search(file:any): Observable<Laptop[]>{
    return this.http.post<Laptop[]>('/api/search', file, this.httpOptions);
  }
  // getSample(){
  //   return this.http.get(this.sampleUrl)
  //   .pipe(map((resp: Response) => resp.json()));
  // }
}
