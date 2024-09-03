import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {BehaviorSubject, Observable} from "rxjs";
import {User} from "../../model/user";
import {API_CONFIG} from "../../app.config";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  baseURL: string = `${API_CONFIG.baseIP}/user`;
  ownerDataStream: any;

  constructor(private httpClient:HttpClient) {
    this.ownerDataStream = new BehaviorSubject<any>(null);
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + id (path variable), header
  getUserById(id: any): Observable<User> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<User>(this.baseURL + "/getUserByID/" + id, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + email (path variable), header
  getUserByEmail(email: any): Observable<User> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<User>(this.baseURL + "/getUserByEmail/" + email, {headers: header})
  }

  // header - pentru header-ul mesajului
  // credentials - name, email, password, role - pentru adaugare admin
  // metoda de post - URL, body, header
  addUser(name: any, email: any, password: any, role: any): any {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let credentials = {name: name, email: email, password: password, role: role};
    return this.httpClient.post(this.baseURL + "/addUser",
      JSON.stringify(credentials) ,{headers: header});
  }
}
