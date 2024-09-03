import {Component, OnInit} from '@angular/core';
import {MatAnchor} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {FormsModule} from "@angular/forms";
import {User} from "../../model/user";
import {AuthService} from "../../service/auth/auth.service";

@Component({
  selector: 'app-log-in-page',
  standalone: true,
  imports: [
    MatAnchor,
    MatIcon,
    MatToolbar,
    NgIf,
    RouterLink,
    FormsModule
  ],
  templateUrl: './log-in-page.component.html',
  styleUrl: './log-in-page.component.css'
})
export class LogInPageComponent implements OnInit {
  user: User = new User();

  constructor(
    private router: Router,
    private authService: AuthService
  ){

  }

  ngOnInit(): void {
  }

  // salvam in session storage userId, userEmail si userRole - daca logIn-ul a fost realizat corespunzator
  logIn(){
    this.authService.login(this.user.email, this.user.password).subscribe(
      (userLogged: any) => {
        console.log(userLogged)
        sessionStorage.setItem("userId", userLogged.id)
        sessionStorage.setItem("userEmail", userLogged.email);
        sessionStorage.setItem("userRole", userLogged.role);
        alert("Login successfully");

        this.router.navigateByUrl("/productsPage");
      },
      (error: any) => { // afisare mesaje de eroare corespunzatoare
        console.error(error)
        const errorMessage = error.error.message
        if(errorMessage === "Missing email")
          alert("Missing email")
        if(errorMessage === "Missing password")
          alert("Missing password")
        if(errorMessage === "Invalid email or password")
          alert("Email and/or password are incorrect. Please, rewrite them.");
      }
    );
  }

}
