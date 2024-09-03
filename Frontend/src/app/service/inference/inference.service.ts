import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {BehaviorSubject} from "rxjs";
import {API_CONFIG} from "../../app.config";

@Injectable({
  providedIn: 'root'
})
export class InferenceService {
  baseURL: string = `${API_CONFIG.baseIP}/inference`;
  ownerDataStream: any;

  constructor(private httpClient:HttpClient) {
    this.ownerDataStream = new BehaviorSubject<any>(null);
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + user_id (path variable), header
  // folosita pentru scanarea unui produs
  startInference(user_id: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<any>(this.baseURL + "/runInference/" + user_id, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL, header
  // folosita pentru inchiderea capacului - in cazul 2 de test (nu se potriveste greutatea)
  closeServo(){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<any>(this.baseURL + "/closeServo", {headers: header})
  }

}
