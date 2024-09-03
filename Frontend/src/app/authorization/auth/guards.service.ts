import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree} from "@angular/router";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class GuardsService implements CanActivate {
  routeURL: String;
  constructor(private router: Router) {
    this.routeURL = router.url // initializare cu pagina curenta
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    // verificam sa vedem daca user-ul este logat (are date salvate in session storage)
    const userEmail: any = sessionStorage.getItem("userEmail")
    if(userEmail != null) {
      return true;
    }
    else { // daca nu e, i se blicheaza accesul la pagina si e redirectionat pe HomePage
      return this.router.navigateByUrl("/homePage");
    }
  }
}
