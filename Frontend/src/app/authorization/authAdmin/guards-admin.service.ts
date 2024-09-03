import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree} from "@angular/router";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class GuardsAdminService implements CanActivate{
  routeURL: String;
  constructor(private router: Router) {
    this.routeURL = router.url
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    // verificam daca user-ul curent e client
    // daca da, nu are acces la pagina de admin
    // si e redirectionat pe Home Page
    const userRole: any = sessionStorage.getItem("userRole")
    if(userRole === "CLIENT"){
      return this.router.navigateByUrl("/homePage")
    }
    else {
      return true;
    }
  }
}
