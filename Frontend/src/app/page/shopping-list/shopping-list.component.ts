import {Component, OnInit} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {MatAnchor} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {NgForOf, NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {ShoppingList} from "../../model/shoppingList";
import {ShoppingListService} from "../../service/shoppinglist/shopping-list.service";
import {ProductService} from "../../service/product/product.service";
import {MatSnackBar} from "@angular/material/snack-bar";
import {InferenceService} from "../../service/inference/inference.service";
import {AuthService} from "../../service/auth/auth.service";

@Component({
  selector: 'app-shopping-list',
  standalone: true,
  imports: [
    FormsModule,
    MatAnchor,
    MatIcon,
    MatToolbar,
    NgForOf,
    NgIf,
    RouterLink
  ],
  templateUrl: './shopping-list.component.html',
  styleUrl: './shopping-list.component.css'
})
export class ShoppingListComponent implements OnInit{
  logOutVisible: boolean = false;
  shoppingLists: ShoppingList[] = [];

  constructor(
    private router: Router,
    private shoppingListService: ShoppingListService,
    private authService: AuthService,
    private inferenceService: InferenceService,
    private snackBar: MatSnackBar
  ) {

  }

  ngOnInit() {
    var userId: any;
    userId = sessionStorage.getItem("userId");
    console.log(userId);
    if(userId !== null)
      this.logOutVisible = true;

    this.getAllShoppingListsByUserId(userId); // returneaza lista de cumparaturi a clientului
  }

  deleteProductFromShoppingList(shopping_list_id: any) { // stergere din lista de cumparaturi
    var userId: any;
    userId = sessionStorage.getItem("userId");
    this.shoppingListService.deleteShoppingList(shopping_list_id).subscribe(
      (shoppingListResult) => {
        this.snackBar.open("Successfully deleted from shopping list", "", {
          duration: 1000
        });
        this.getAllShoppingListsByUserId(userId);
      },
      (error: Error) => {
        console.error(error);
      }
    )
  }

  getAllShoppingListsByUserId(userId: any) {
    this.shoppingListService.getAllShoppingListsByUserId(userId).subscribe(
      (shoppingListsResult) => {
        this.shoppingLists = shoppingListsResult;
      },
      (error: Error) => {
        console.error(error);
      }
    );
  }

  scanProduct(){ // logica de inferente
    var userId: any;
    userId = sessionStorage.getItem("userId");
    this.inferenceService.startInference(userId).subscribe(
      (shoppingListResult) => {
        if (shoppingListResult === "Too many/less products"){
          this.snackBar.open("Too many/less products", "", {
            duration: 3000
          });
          this.inferenceService.closeServo().subscribe();
        }
        if (shoppingListResult === "No product found"){
          this.snackBar.open("No product found", "", {
            duration: 3000
          });
        }
        this.getAllShoppingListsByUserId(userId);
      },
      (error: Error) => {
        console.error(error)
      }
    )
  }

  // sterge lista de cumparaturi si greutatea din sesiunea curenta
  logOut(){
    var userId: any;
    userId = sessionStorage.getItem("userId")
    this.authService.logout(userId).subscribe(
      () => {
        sessionStorage.clear();
        this.logOutVisible = false;
        this.router.navigateByUrl("/homePage");
      }
    )
  }

}
