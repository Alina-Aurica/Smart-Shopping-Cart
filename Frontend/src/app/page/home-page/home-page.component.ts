import {Component, OnInit} from '@angular/core';
import {NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {MatToolbar} from "@angular/material/toolbar";
import {MatIcon} from "@angular/material/icon";
import {MatAnchor} from "@angular/material/button";
import {ShoppingListService} from "../../service/shoppinglist/shopping-list.service";
import {AuthService} from "../../service/auth/auth.service";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    NgIf,
    RouterLink,
    MatToolbar,
    MatIcon,
    MatAnchor,
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent implements OnInit{
  logOutVisible: boolean = false; // face vizibil butonul de logOut
  adminVisible: boolean = false; // face vizibila pagina de admin
  clientVisible: boolean = false; // face vizibila pagina de shopping list

  constructor(
    private router: Router,
    private authService: AuthService
  ) {
  }

  ngOnInit(): void {
    var userRole: any;
    userRole = sessionStorage.getItem("userRole");
    console.log(userRole);
    if(userRole !== null) { // daca avem un user logat
      this.logOutVisible = true;
      if(userRole === "ADMIN") // daca are rol de admin
        this.adminVisible = true;
      else
        this.clientVisible = true;
    }
  }

  // sterge lista de cumparaturi si greutatea din sesiunea curenta
  logOut(){
    var userId: any;
    userId = sessionStorage.getItem("userId")
    this.authService.logout(userId).subscribe(
      () => {
        sessionStorage.clear();
        this.logOutVisible = false;
        this.adminVisible = false;
        this.clientVisible = false;
        this.router.navigateByUrl("/homePage");
      }
    )
  }
}
