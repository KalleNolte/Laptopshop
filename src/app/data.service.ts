import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Laptop } from "./laptop";
import { Observable } from 'rxjs';
import * as io from 'socket.io-client';
import {Router} from '@angular/router';

@Injectable({
  providedIn: "root"
})
export class DataService {
  //sampleUrl = "../assets/amazonDataSample.json";
  private url = 'http://localhost:5004/';
  private socket;
  laptops : Observable<Laptop[]>;
  firstTime = true ;
  laptop : Laptop;
 
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      // 'Authorization': 'my-auth-token'
    })
  };

  constructor(private http: HttpClient) {
    this.socket = io.connect(this.url);
  }

  getSample(): Observable<Laptop[]>{
    this.saveLaptops(this.http.get<Laptop[]>('/api/sample'));
    return this.http.get<Laptop[]>('/api/sample');
  }

  search(file:any): Observable<Laptop[]>{
    this.saveLaptops(this.http.post<Laptop[]>('/api/search', file, this.httpOptions));
    return this.http.post<Laptop[]>('/api/search', file, this.httpOptions);
  }

  searchText(file:any): Observable<Laptop[]>{
    return this.http.post<Laptop[]>('/api/searchText', file, this.httpOptions);
  }

  getLaptop_details(asin:String){
    return this.http.get<Laptop>('/api/' + asin,this.httpOptions);
  }

  setLaptop(laptop): Observable<Laptop>{
    return this.http.post<Laptop>('/alexa/setter', laptop, this.httpOptions);
  }
  getCritizedResult(): Observable<Laptop[]> {
    
    // if (result != null) {
      this.saveLaptops(this.http.get<Laptop[]>('/alexa/getQuery'));
      return this.http.get<Laptop[]>('/alexa/getQuery')
    // }
    
  }

  saveLaptops(laptops:Observable<Laptop[]>){
    this.laptops = laptops;
  }

  retrieveLaptops():Observable<Laptop[]>{
    if(this.laptops) {
      console.log(this.laptops);
      this.laptops.subscribe(data=>console.log(data));
      return this.laptops;
    }
  }

  // public getResult = () => {
    // this.saveLaptops(Observable.create((observer) => {
    //         this.socket.on('result', (message) => {
    //             observer.next(message);
    //         });
    //     }));
    // return Observable.create((observer) => {
    //         this.socket.on('result', (message) => {
    //             observer.next(message);
    //         });
    //     });
  // }

  public getResult(): Observable<Laptop[]> {
        this.socket.emit('getResult');
        this.saveLaptops(new Observable<Laptop[]>(observer => {
                this.socket.on('result', (data) => observer.next(data));
            }));
        return new Observable<Laptop[]>(observer => {
            this.socket.on('result', (data) => observer.next(data));
        });
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
