import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {BehaviorSubject, Observable} from "rxjs";
import {ShoppingList} from "../../model/shoppingList";
import {API_CONFIG} from "../../app.config";

@Injectable({
  providedIn: 'root'
})
export class ShoppingListService {
  baseURL: string = `${API_CONFIG.baseIP}/shoppinglist`;
  ownerDataStream: any;

  constructor(private httpClient:HttpClient) {
    this.ownerDataStream = new BehaviorSubject<any>(null);
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + id (path variable), header
  getShoppingListById(id: any): Observable<ShoppingList> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<ShoppingList>(this.baseURL + "/getShoppingListById/" + id, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL + user_id (path variable), header
  // returneaza lista de cumparaturi a clientului
  getAllShoppingListsByUserId(user_id: any): Observable<ShoppingList[]> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<ShoppingList[]>(this.baseURL + "/getAllShoppingListsByUserId/" + user_id, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de get - URL, header
  // returneaza toate listele de cumparaturi
  getAllShoppingLists(): Observable<ShoppingList[]> {
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.get<ShoppingList[]>(this.baseURL + "/getAllShoppingLists", {headers: header})
  }

  // header - pentru header-ul mesajului
  // infos - id_user, id_product, name_product, number_of_products
  // metoda de post - URL, body, header
  // adauga in lista un produs
  addShoppingList(id_user: any, id_product: any, name_product: any, number_of_products: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let infos = {id_user: id_user, id_product: id_product, name_product: name_product, number_of_products: number_of_products}
    return this.httpClient.post(this.baseURL + "/addShoppingList", JSON.stringify(infos), {headers: header})
  }

  // header - pentru header-ul mesajului
  // infos - id, id_user, id_product, name_product, number_of_products
  // metoda de put - URL, body, header
  updateShoppingList(id: any, id_user: any, id_product: any, name_product: any, number_of_products: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    let infos = {id_user: id_user, id_product: id_product, name_product: name_product, number_of_products: number_of_products}
    return this.httpClient.put(this.baseURL + "/updateShoppingList/" + id, JSON.stringify(infos), {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de delete - URL + id (path variable), header
  // sterge un produs din lista de cumparaturi
  deleteShoppingList(id: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.delete(this.baseURL + "/deleteShoppingList/" + id, {headers: header})
  }

  // header - pentru header-ul mesajului
  // metoda de delete - URL + id_user (path variable), header
  // sterge lista de cumparaturi a unui client
  deleteShoppingListByUserId(id_user: any){
    let header = new HttpHeaders()
      .set('Content-Type', 'application/json')
    return this.httpClient.delete(this.baseURL + "/deleteShoppingListByUserId/" + id_user, {headers: header})
  }

}
