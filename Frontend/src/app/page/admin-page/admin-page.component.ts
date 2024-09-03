import {Component, OnInit} from '@angular/core';
import {MatToolbar} from "@angular/material/toolbar";
import {MatAnchor} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {NgForOf, NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {Product} from "../../model/product";
import {FormsModule} from "@angular/forms";
import {ProductService} from "../../service/product/product.service";

@Component({
  selector: 'app-admin-page',
  standalone: true,
  imports: [
    MatToolbar,
    MatAnchor,
    MatIcon,
    NgIf,
    RouterLink,
    FormsModule,
    NgForOf
  ],
  templateUrl: './admin-page.component.html',
  styleUrl: './admin-page.component.css'
})
export class AdminPageComponent implements OnInit{
  logOutVisible: boolean = false;
  product: Product = new Product();
  products: Product[] = [];

  constructor(
    private router: Router,
    private productService: ProductService
  ) {
  }

  ngOnInit(): void {
    var userRole: any;
    userRole = sessionStorage.getItem("userRole");
    console.log(userRole);
    if(userRole !== null) // pentru aparitia butonului de logOut
      this.logOutVisible = true;

    this.getAllProducts(); // returneaza toate produsele din BD
  }

  addProduct(){ // adauga un produs in baza de date
    console.log(this.product);
    this.productService.addProduct(this.product.name, this.product.quantity_min, this.product.quantity_max, this.product.stock, this.product.image_url).subscribe(
        (productResult) => {
          alert("Successfully add product!")
          this.getAllProducts();
        },
        (error: Error) => {
          alert("Failed add product!");
          console.error(error);
        }
    );
  }

  updateProduct(productAux: any) { // face update la un produs in baza de date
    this.productService.updateProduct(productAux.id, productAux.name, productAux.quantity_min, productAux.quantity_max, productAux.stock, productAux.image_url).subscribe(
      (productResult) => {
        alert("Successfully update product!")
        this.getAllProducts();
      },
      (error: Error) => {
        alert("Failed update product!");
        console.error(error);
      }
    );
  }

  deleteProduct(product_id: any){ // sterge un produs din baza de date
    this.productService.deleteProduct(product_id).subscribe(
      (productResult) => {
          alert("Successfully delete product!")
          this.getAllProducts();
        },
        (error: Error) => {
          alert("Failed delete product!");
          console.error(error);
        }
    );
  }

  setEditable(productAux: any){ // marcheaza un produs ca putand fi editabil
    productAux.editable = true;
  }

  getAllProducts(){ // listeaza toate produsele
    this.productService.getAllProducts().subscribe(
      (productsResult) => {
        this.products = productsResult.sort((p1, p2) => {
          if (p1.id === undefined && p2.id === undefined) { // sortare creascatoare a listei in functie de id-uri
            return 0;
          } else if (p1.id === undefined) {
            return 1;
          } else if (p2.id === undefined) {
            return -1;
          }
          return p1.id - p2.id;
        });
        console.log("Refresh mode!")
      },
      (error: Error) => {
        console.error(error)
      }
    );
  }

  logOut(){
    sessionStorage.clear();
    this.logOutVisible = false;
    this.router.navigateByUrl("/homePage");
  }
}
