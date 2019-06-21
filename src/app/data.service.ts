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
  laptops : Observable<Laptop[]>;
  firstTime = true;
 
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

  searchText(file:any): Observable<Laptop[]>{
    return this.http.post<Laptop[]>('/api/searchText', file, this.httpOptions);
  }

  getLaptop_details(asin:String){
    return this.http.get<Laptop>('/api/' + asin,this.httpOptions);
  }

  getCritizedResult(laptop): Observable<Laptop[]> {
    let result = this.http.post<Laptop[]>('/alexa/setter', laptop, this.httpOptions);
    if (result != null) {
      this.saveLaptops(this.http.get<Laptop[]>('/alexa/getQuery'));
      return this.http.get<Laptop[]>('/alexa/getQuery')
    }
  }

  saveLaptops(laptops:Observable<Laptop[]>){
    this.laptops = laptops;
  }

  retriveLaptops():Observable<Laptop[]>{
    if(this.laptops) {
      console.log(this.laptops);
      return this.laptops;
    }
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
