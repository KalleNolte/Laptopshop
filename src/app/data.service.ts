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
  private for_detailsExample="../assets/jsonExample.json";
  private for_sendD='https://console.firebase.google.com/u/0/project/laptop-fc91e/database/firestore/data~2Flaptop~2FblCnfbhPDMjMEUNnFp4W';
  array_laptops: Observable<Laptop[]>

 
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
    this.array_laptops= this.http.post<Laptop[]>('/api/search', file, this.httpOptions);
    return this.http.post<Laptop[]>('/api/search', file, this.httpOptions);
  }
  // getSample(){
  //   return this.http.get(this.sampleUrl)
  //   .pipe(map((resp: Response) => resp.json()));
  // }

  getLaptop_details():Observable<Laptop[]>{
    return this.http.get<Laptop[]>(this.for_detailsExample);
  }
   getLaptop_details_2():Observable<Laptop[]>{
    return this.http.get<Laptop[]>('/api/search');
  }

}



  // here i only use one Laptop info for the view page
 /* getLaptop_details():Observable<Laptop[]>{
    return this.http.get<Laptop[]>(this.for_detailsExample);
  }
  setLaptop_details(lap: any):Observable<Laptop>{
    return this.http.post<Laptop>(this.for_sendD,lap,this.httpOptions);
  }
  */
