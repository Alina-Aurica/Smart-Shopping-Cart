import {Component, OnInit, Pipe, PipeTransform} from '@angular/core';
import {MatAnchor} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {NgForOf, NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {Product} from "../../model/product";
import {FormsModule} from "@angular/forms";
import {ProductService} from "../../service/product/product.service";
import {ShoppingListService} from "../../service/shoppinglist/shopping-list.service";
import {error} from "@angular/compiler-cli/src/transformers/util";
import {ShoppingList} from "../../model/shoppingList";
import {MatSnackBar} from "@angular/material/snack-bar";
import {AuthService} from "../../service/auth/auth.service";

@Component({
  selector: 'app-products-page',
  standalone: true,
  imports: [
    MatAnchor,
    MatIcon,
    MatToolbar,
    NgIf,
    RouterLink,
    NgForOf,
    FormsModule,
  ],
  templateUrl: './products-page.component.html',
  styleUrl: './products-page.component.css',
})
export class ProductsPageComponent implements OnInit{
  logOutVisible: boolean = false;
  adminVisible: boolean = false;
  clientVisible: boolean = false;
  productName: string = '';
  products: Product[] = [];

  constructor(
    private router: Router,
    private productService: ProductService,
    private shoppingListService: ShoppingListService,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {
  }

  ngOnInit(): void {
    var userRole: any;
    userRole = sessionStorage.getItem("userRole");
    console.log(userRole);
    if(userRole !== null) { // pentru vizibilitatea paginilor si a butoanelor
      this.logOutVisible = true;
      if(userRole === "ADMIN")
        this.adminVisible = true;
      else
        this.clientVisible = true;
    }

    this.productService.getAllProducts().subscribe( // returneaza toate produsele
      (productsResult: Product[]) => {
        productsResult.forEach(function(product: Product){
          if(product.quantity_min !== undefined && product.quantity_max !== undefined) // cantitatea medie
            product.quantity_mean = (product.quantity_min + product.quantity_max) / 2;
          if(product.stock !== undefined) // numarul de produse din care poti alege
            product.interval = Array.from({length: product.stock}, (_, i) => i + 1);
        })
        this.products = productsResult
      },
      (error: Error) => {
        console.error(error)
    }
    )
  }

  searchProduct(){ // filtrare pentru bara de cautare
    this.products = this.products.filter(productAux => productAux.name?.toLowerCase().includes(this.productName.toLowerCase()));
  }

  // adaugare produs in lista de cumparaturi
  addProductInShoppingList(product_id: any, product_name: any, number_of_products: any){
    var user_id : any;
    user_id = sessionStorage.getItem("userId")
    this.shoppingListService.addShoppingList(user_id, product_id, product_name, number_of_products).subscribe(
      (shoppingListResult) => {
        this.snackBar.open("Successfully add in shopping list", "", {
          duration: 1000
        });
      },
      (error: Error) => {
        this.snackBar.open("Failed to add in shopping list", "", {
          duration: 1000
        });
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
        this.adminVisible = false;
        this.clientVisible = false;
        this.router.navigateByUrl("/homePage");
      }
    )
  }
}
