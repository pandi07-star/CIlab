% =====================================
% SET OPERATIONS
% =====================================

% UNION
union([], L, L).
union([H|T], L, R) :-
    member(H, L),
    union(T, L, R).
union([H|T], L, [H|R]) :-
    \+ member(H, L),
    union(T, L, R).

% INTERSECTION
intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    member(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ member(H, L),
    intersection(T, L, R).

% DIFFERENCE
difference([], _, []).
difference([H|T], L, R) :-
    member(H, L),
    difference(T, L, R).
difference([H|T], L, [H|R]) :-
    \+ member(H, L),
    difference(T, L, R).

% =====================================
% ARITHMETIC OPERATIONS
% =====================================

add(X, Y, R) :-
    R is X + Y.

subtract(X, Y, R) :-
    R is X - Y.

multiply(X, Y, R) :-
    R is X * Y.

divide(X, Y, R) :-
    Y \= 0,
    R is X / Y.

% =====================================
% MENU (OPTIONAL HELPER)
% =====================================

show_menu :-
    nl, write('--- PROLOG OPERATIONS ---'), nl,
    write('SET OPERATIONS:'), nl,
    write('1. union([1,2,3],[2,3,4],R).'), nl,
    write('2. intersection([1,2,3],[2,3,4],R).'), nl,
    write('3. difference([1,2,3],[2,3,4],R).'), nl,
    write('ARITHMETIC OPERATIONS:'), nl,
    write('4. add(5,3,R).'), nl,
    write('5. subtract(10,4,R).'), nl,
    write('6. multiply(6,2,R).'), nl,
    write('7. divide(10,2,R).'), nl, nl.


?- show_menu.

--- PROLOG OPERATIONS ---
SET OPERATIONS:
1. union([1,2,3],[2,3,4],R).
2. intersection([1,2,3],[2,3,4],R).
3. difference([1,2,3],[2,3,4],R).
ARITHMETIC OPERATIONS:
4. add(5,3,R).
5. subtract(10,4,R).
6. multiply(6,2,R).
7. divide(10,2,R).
