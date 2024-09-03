export class Product {
  id: number | undefined;
  name: string | undefined;
  quantity_min: number | undefined;
  quantity_max: number | undefined;
  quantity_mean: number | undefined; // pentru afisarea gramajului unui produs
  stock: number | undefined;
  image_url: string | undefined;
  number_of_products: number | undefined; // numarul de produse selectat - pt introducere in shopping list
  editable: boolean | undefined; // pentru editarea produselor - la update
  interval: number[] = []; // pentru a stabili cate produse putem sa selectam
}
