:- dynamic pizza/2.
:- dynamic order/3.

% -------------------------------
% Initial Menu
% -------------------------------
pizza(margherita, 150).
pizza(pepperoni, 250).
pizza(veggie_supreme, 200).

% -------------------------------
% Show Menu
% -------------------------------
show_menu :-
    write('--- PIZZA MENU ---'), nl,
    pizza(Name, Price),
    write(Name), write(' - Rs.'), write(Price), nl,
    fail.
show_menu.

% -------------------------------
% Add Pizza
% -------------------------------
add_pizza(Name, Price) :-
    assertz(pizza(Name, Price)),
    write('Pizza added successfully!'), nl.

% -------------------------------
% Update Price
% -------------------------------
update_price(Name, NewPrice) :-
    retract(pizza(Name, _)),
    assertz(pizza(Name, NewPrice)),
    write('Price updated successfully!'), nl.

% -------------------------------
% Delete Pizza
% -------------------------------
delete_pizza(Name) :-
    retract(pizza(Name, _)),
    write('Pizza deleted successfully!'), nl.

% -------------------------------
% Place Order
% -------------------------------
place_order(Customer, PizzaName, Qty) :-
    pizza(PizzaName, Price),
    Total is Price * Qty,
    assertz(order(Customer, PizzaName, Qty)),
    write('Order placed! Total = Rs.'), write(Total), nl.

% -------------------------------
% Show Orders
% -------------------------------
show_orders :-
    write('--- ORDERS ---'), nl,
    order(C, P, Q),
    write(C), write(' ordered '), write(Q),
    write(' x '), write(P), nl,
    fail.
show_orders.

% -------------------------------
% Generate Bill
% -------------------------------
generate_bill(Customer) :-
    write('--- BILL ---'), nl,
    order(Customer, Pizza, Qty),
    pizza(Pizza, Price),
    Cost is Qty * Price,
    write(Pizza), write(' x '), write(Qty),
    write(' = Rs.'), write(Cost), nl,
    fail.
generate_bill(Customer) :-
    total_bill(Customer, Total),
    write('TOTAL = Rs.'), write(Total), nl.

% -------------------------------
% Calculate Total
% -------------------------------
total_bill(Customer, Total) :-
    findall(Cost,
        (order(Customer, Pizza, Qty),
         pizza(Pizza, Price),
         Cost is Qty * Price),
        List),
    sum_list(List, Total).?- show_menu.
