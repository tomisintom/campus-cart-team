"""
Cart Engine Module

This module provides tools for managing carts, adding to cart, removing from cart, checking out cart
"""
import time
# Border Function
def box(text, padding=2):
    length = len(text) + (padding * 2)
    
    print("+" + "-" * length + "+")
    print("|" + " " * length + "|")
    print(f"|{' ' * padding}{text}{' ' * padding}|")
    print("|" + " " * length + "|")
    print("+" + "-" * length + "+")


# Add to cart section
cart_list = []

#Function 
def add_to_cart(inventory):
  while True:
    print()
    print("-"*20)
    item = input("Enter the name of the item: (or enter exit to quit ) ").strip().lower()
    print("-"*20)
    print()
    if item == "exit":
      break
    else:
      for item_id, product_details in inventory.items():
        if item == product_details["name"].lower():
          product_id = item_id
          product_price = product_details["price"]
          product_stock = product_details["stock"]

          

          # Getting quantity to purchase
          
          if product_stock == 0:
              print()
              print("-"*20)
              print(f"Sorry, {product_details['name']} is out of stock.")
              print("-"*20)
              print()
              break  

          item_qty = None  

          while True:
              print()
              print("-"*20)
              qty_input = input(
                  f"How many? ({product_stock} available, or type 'back' to return) "
              ).strip().lower()
              print("-"*20)
              print()

              if qty_input == "back":
                  break  

              if not qty_input.isdecimal():
                  print()
                  print("-"*20)
                  print("Please enter a whole number.")
                  print("-"*20)
                  print("-"*20)
                  continue

              qty = int(qty_input)

              if qty <= 0:
                  print()
                  print("-"*20)
                  print("Quantity must be greater than zero.")
                  print("-"*20)
                  print()
                  continue

              if qty > product_stock:
                  print()
                  print("-"*20)
                  print(
                      f"Not enough stock. Only {product_stock} "
                      f"{product_details['name']}(s) are available."
                  )
                  print("-"*20)
                  print()
                  continue

              item_qty = qty
              break

          if item_qty is None:
              break  

          
          
          for cart_item in cart_list:
              if cart_item["product_id"] == item_id:
                  new_quantity = cart_item["qty"] + item_qty

                  if new_quantity > product_stock:
                      print()
                      print("-"*20)
                      print(
                          f"You already have {cart_item['qty']} in your cart. "
                          f"Only {product_stock} {product_details["name"]}(s) are available."
                      )
                      print("-"*20)
                      print()
                  else:
                      cart_item["qty"] = new_quantity
                      cart_item["subtotal"] = product_price * new_quantity
                      print()
                      print("="*20)
                      print()
                      print(f"{item} cart quantity updated successfully")
                      print()
                      print("="*20)
                      print()

                  break
          else:
              to_purchase = {
                  "product_id": item_id,
                  "name": product_details["name"],
                  "qty": item_qty,
                  "subtotal": product_price * item_qty
              }

              cart_list.append(to_purchase)
              print()
              print("="*20)
              print()
              print(f"{item} added to cart successfully")
              print()
              print("="*20)
              print()
          
          break

      else: 
          item != product_details["name"].lower()
          print()
          print("="*20)
          print (f"{item} not available, check back later.")
          print("="*20)
          print()



# View cart section
def view_cart():
  if not cart_list:
    print()
    print("=" * 55)
    print("Your cart is empty. Please add items from the catalogue.")
    print("=" * 55)
    return

  total = 0

  border = (
    "+"
    + "-" * 8
    + "+"
    + "-" * 26
    + "+"
    + "-" * 10
    + "+"
    + "-" * 14
    + "+"
  )

  print()
  print("YOUR SHOPPING CART")
  print(border)
  print(
    f"| {'ID':<6} "
    f"| {'PRODUCT':<24} "
    f"| {'QUANTITY':>8} "
    f"| {'SUBTOTAL':>12} |"
  )
  print(border)

  for cart_item in cart_list:
    product_id = cart_item["product_id"]
    name = cart_item["name"]
    quantity = cart_item["qty"]
    subtotal = f"${cart_item['subtotal']:.2f}"

    print(
      f"| {product_id:<6} "
      f"| {name:<24} "
      f"| {quantity:>8} "
      f"| {subtotal:>12} |"
    )

    total += cart_item["subtotal"]

  total_text = f"${total:.2f}"

  print(border)
  print(
    f"| {'':<6} "
    f"| {'':<24} "
    f"| {'TOTAL':>8} "
    f"| {total_text:>12} |"
  )
  print(border)



# Checkout Section
def checkout(inventory):

  if not cart_list:
    print()
    print("="*20)
    print("Your cart is empty. Please add items before checking out.")
    print("="*20)
    return

  # Keep only the items that can be sold
  valid_items = []

  for cart_item in cart_list:
    product = inventory.get(cart_item["product_id"])

    if product is not None and cart_item["qty"] <= product["stock"]:
      valid_items.append(cart_item)

  if not valid_items:
    print()
    print("="*20)
    print("None of the items in your cart can be checked out.")
    print("="*20)
    cart_list.clear()
    return

  total_list = []

  def generate_receipt():
    yield None
    yield "="*20
    yield "YOUR RECEIPT"
    yield "-"*20
    yield None

    for item_dict in valid_items:
      product_id = item_dict["product_id"]
      name = item_dict["name"]
      qty = item_dict["qty"]
      subtotal = item_dict["subtotal"]

      inventory[product_id]["stock"] -= qty
      total_list.append(subtotal)

      yield f"{name:<22} | Quantity: {qty:>3} | Subtotal: ${subtotal:>8.2f}"

    yield "-" * 65

    total = sum(total_list)

    if total > 20:
      discounted_total = total - (total * 0.1)

      yield f"{'Total before discount:':<45}${total:>10.2f}"
      yield f"{'Discount (10%):':<45}-${total * 0.1:>9.2f}"
      yield "-" * 65
      yield f"{'Total after discount:':<45}${discounted_total:>10.2f}"
    else:
      yield f"{'Total:':<45}${total:>10.2f}"

    yield None
    yield "="*20
    yield None

  # To stream the receipt
  for line in generate_receipt():
    if line is None:
      print()
    else:
      print(line)
    time.sleep(0.15)

  box("Thank you for your patronage. See you again")

  cart_list.clear()





#  CLI Testing

campus_inventory = {
"101": {"name": "Notebook", "price": 2.50, "stock": 15},
"102": {"name": "Campus Hoodie", "price": 25.00, "stock": 4},
"103": {"name": "Scientific Calculator", "price": 15.00, "stock": 8},
"104": {"name": "Ballpoint Pens (10-pack)", "price": 4.75, "stock": 40},
"105": {"name": "Highlighter Set", "price": 6.25, "stock": 22},
"106": {"name": "Backpack", "price": 32.99, "stock": 6},
"107": {"name": "USB Flash Drive 64GB", "price": 11.50, "stock": 18},
"108": {"name": "Water Bottle", "price": 9.99, "stock": 12},
"109": {"name": "Desk Lamp", "price": 19.95, "stock": 3},
"110": {"name": "Sticky Notes", "price": 1.99, "stock": 55},
"111": {"name": "Graph Paper Pad", "price": 3.25, "stock": 9},
"112": {"name": "Campus T-Shirt", "price": 14.00, "stock": 25},
"113": {"name": "Laptop Sleeve", "price": 17.50, "stock": 7},
"114": {"name": "Stapler", "price": 7.80, "stock": 14},
"115": {"name": "Ruler Set", "price": 2.10, "stock": 30},
}


while True:
    print("\n1. Add to cart  2. View cart  3. Checkout  4. Quit")
    choice = input("Choose: ").strip()

    if choice == "1":
        add_to_cart(campus_inventory)
    elif choice == "2":
        view_cart()
    elif choice == "3":
        checkout(campus_inventory)
    elif choice == "4":
        break
    else:
        print("Invalid choice.")
