import {Component, OnInit} from '@angular/core';
import {User} from "../../model/user";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatAnchor} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {NgIf} from "@angular/common";
import {RouterLink} from "@angular/router";
import {AuthService} from "../../service/auth/auth.service";

@Component({
  selector: 'app-register-page',
  standalone: true,
  imports: [
    FormsModule,
    MatAnchor,
    MatIcon,
    MatToolbar,
    NgIf,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './register-page.component.html',
  styleUrl: './register-page.component.css'
})
export class RegisterPageComponent implements OnInit {
  user: User = new User();

  constructor(
    private authService: AuthService
  ) {
  }

  ngOnInit(): void {
  }

  // un client nou se inregistreaza
  register() {
    console.log(this.user)
    this.authService.register(this.user.name, this.user.email, this.user.password).subscribe(
      (userRegistered: User) => {
        this.user = userRegistered
        alert("Registration successfully")
      },
      (error: any) => { // mesajele de eroare
        console.error(error)
        const errorMessage = error.error.message
        if(errorMessage === "User already registered")
          alert("User already registered")
        else
          alert("Registration failed - some fields are null or incorrect completed!")
      }
    )
  }

}
