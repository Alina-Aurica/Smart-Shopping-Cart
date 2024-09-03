import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {BehaviorSubject} from "rxjs";
import {API_CONFIG} from "../../app.config";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // am creat o variabila globala pentru adresa backend-ului
  baseURL: string = `${API_CONFIG.baseIP}/auth`;
  ownerDataStream: any;

  constructor(private httpClient:HttpClient) { // httpClient - folosita pentru request-uri
    this.ownerDataStream = new BehaviorSubject<any>(null);
  }

  // header - pentru header-ul mesajului
  // credentials - email si parola - pentru logIn
  // metoda de post - URL, body, header
  public login(email: any, password: any): any {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let credentials = { email: email, password: password };
    return this.httpClient.post(this.baseURL + "/login",
      JSON.stringify(credentials), {headers: header});
  }

  // header - pentru header-ul mesajului
  // credentials - name, email si parola - pentru register
  // metoda de post - URL, body, header
  public register(name: any, email: any, password: any): any
  {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let credentials = {name: name, email: email, password: password}
    return this.httpClient.post(this.baseURL + "/register",
      JSON.stringify(credentials), {headers: header, observe:'response'});
  }

  // header - pentru header-ul mesajului
  // metoda de delete - URL + user_id (path variable), header
  public logout(user_id: any): any {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.delete(this.baseURL + "/logout/" + user_id, {headers: header});
  }
}
