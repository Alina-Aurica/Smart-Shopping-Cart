import { Routes } from '@angular/router';
import {HomePageComponent} from "./page/home-page/home-page.component";
import {LogInPageComponent} from "./page/log-in-page/log-in-page.component";
import {RegisterPageComponent} from "./page/register-page/register-page.component";
import {ProductsPageComponent} from "./page/products-page/products-page.component";
import {ShoppingListComponent} from "./page/shopping-list/shopping-list.component";
import {AdminPageComponent} from "./page/admin-page/admin-page.component";
import {GuardsService} from "./authorization/auth/guards.service";
import {GuardsClientService} from "./authorization/authClient/guards-client.service";
import {GuardsAdminService} from "./authorization/authAdmin/guards-admin.service";

// realizarea path-ului pentru fiecare pagina
// adaugarea guard-urilor pentru shoppingListPage si adminPage - restrictii de access
export const routes: Routes = [
  {path: "homePage", component:HomePageComponent},
  {path: "logInPage", component:LogInPageComponent},
  {path: "registerPage", component:RegisterPageComponent},
  {path: "productsPage", component:ProductsPageComponent},
  {path: "shoppingListPage", component:ShoppingListComponent, canActivate: [GuardsService, GuardsClientService]},
  {path: "adminPage", component:AdminPageComponent, canActivate: [GuardsService, GuardsAdminService]}
];
