import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {BehaviorSubject, Observable} from "rxjs";
import {Product} from "../../model/product";
import {API_CONFIG} from "../../app.config";

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  baseURL: string = `${API_CONFIG.baseIP}/product`;
  ownerDataStream: any;

  constructor(private httpClient:HttpClient) {
    this.ownerDataStream = new BehaviorSubject<any>(null);
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + id (path variable), header
  getProductById(id: any): Observable<Product> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<Product>(this.baseURL + "/getProductById/" + id, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + name (path variable), header
  getProductByName(name: any): Observable<Product> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<Product>(this.baseURL + "/getProductByName/" + name, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL, header
  // folosita in pagina de produse
  getAllProducts(): Observable<Product[]> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<Product[]>(this.baseURL + "/getAllProducts", {headers: header})
  }

  // header - pentru header-ul mesajului
  // infos - name, quantity_min, quantity_max, stock, image_url
  // metoda de post - URL, body, header
  addProduct(name: any, quantity_min: any, quantity_max: any, stock: any, image_url: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let infos = {name: name, quantity_min: quantity_min, quantity_max: quantity_max, stock: stock, image_url: image_url}
    return this.httpClient.post(this.baseURL + "/addProduct", JSON.stringify(infos), {headers: header})
  }

  // header - pentru header-ul mesajului
  // infos - name, quantity_min, quantity_max, stock, image_url
  // metoda de put - URL, body, header
  updateProduct(id: any, name: any, quantity_min: any, quantity_max: any, stock: any, image_url: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let infos = {name: name, quantity_min: quantity_min, quantity_max: quantity_max, stock: stock, image_url: image_url}
    return this.httpClient.put(this.baseURL + "/updateProduct/" + id, JSON.stringify(infos), {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de delete - URL + id (path variable), header
  deleteProduct(id: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.delete(this.baseURL + "/deleteProduct/" + id, {headers: header})
  }

}
