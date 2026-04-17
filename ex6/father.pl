:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.
:- dynamic married/2.

% =====================================
% GENDER
% =====================================

male(karamchand).
male(mahatma).
male(harilal).
male(manilal).
male(ramdas).
male(devdas).
male(kantilal).
male(rasik).
male(arun).
male(kanu).
male(ramchandra).
male(rajmohan).
male(gopalkrishna).

female(putlibai).
female(kasturba).
female(gulab).
female(sushila).
female(nirmala).
female(lakshmi).
female(rami).
female(manuben).
female(sita).
female(sumitra).
female(usha).
female(tara).

% =====================================
% MARRIAGE
% =====================================

married(karamchand, putlibai).
married(mahatma, kasturba).
married(harilal, gulab).
married(manilal, sushila).
married(ramdas, nirmala).
married(devdas, lakshmi).

spouse(X,Y):- married(X,Y).
spouse(X,Y):- married(Y,X).

husband(X,Y):- spouse(X,Y), male(X).
wife(X,Y):- spouse(X,Y), female(X).

% =====================================
% PARENTS
% =====================================

parent(karamchand, mahatma).
parent(putlibai, mahatma).

parent(mahatma, harilal).
parent(kasturba, harilal).

parent(mahatma, manilal).
parent(kasturba, manilal).

parent(mahatma, ramdas).
parent(kasturba, ramdas).

parent(mahatma, devdas).
parent(kasturba, devdas).

parent(harilal, rami).
parent(gulab, rami).
parent(harilal, manuben).
parent(gulab, manuben).
parent(harilal, rasik).
parent(gulab, rasik).

parent(manilal, arun).
parent(sushila, arun).
parent(manilal, sita).
parent(sushila, sita).

parent(ramdas, sumitra).
parent(nirmala, sumitra).
parent(ramdas, kanu).
parent(nirmala, kanu).
parent(ramdas, usha).
parent(nirmala, usha).

parent(devdas, tara).
parent(lakshmi, tara).
parent(devdas, ramchandra).
parent(lakshmi, ramchandra).
parent(devdas, rajmohan).
parent(lakshmi, rajmohan).
parent(devdas, gopalkrishna).
parent(lakshmi, gopalkrishna).

% =====================================
% BASIC RELATIONS
% =====================================

father(X,Y):- parent(X,Y), male(X).
mother(X,Y):- parent(X,Y), female(X).

child(X,Y):- parent(Y,X).
son(X,Y):- child(X,Y), male(X).
daughter(X,Y):- child(X,Y), female(X).

% =====================================
% SIBLINGS
% =====================================

sibling(X,Y):-
    parent(P,X),
    parent(P,Y),
    X \= Y.

brother(X,Y):- sibling(X,Y), male(X).
sister(X,Y):- sibling(X,Y), female(X).

% =====================================
% GRAND RELATIONS
% =====================================

grandparent(X,Y):-
    parent(X,Z),
    parent(Z,Y).

grandfather(X,Y):- grandparent(X,Y), male(X).
grandmother(X,Y):- grandparent(X,Y), female(X).

grandchild(X,Y):- grandparent(Y,X).
grandson(X,Y):- grandchild(X,Y), male(X).
granddaughter(X,Y):- grandchild(X,Y), female(X).

% =====================================
% UNCLE / AUNT
% =====================================

uncle(X,Y):-
    brother(X,P),
    parent(P,Y).

aunt(X,Y):-
    sister(X,P),
    parent(P,Y).

% =====================================
% COUSIN
% =====================================

cousin(X,Y):-
    parent(P1,X),
    parent(P2,Y),
    sibling(P1,P2),
    X \= Y.

% =====================================
% ANCESTOR / DESCENDANT
% =====================================

ancestor(X,Y):- parent(X,Y).
ancestor(X,Y):- parent(X,Z), ancestor(Z,Y).

descendant(X,Y):- ancestor(Y,X).

% =====================================
% IN-LAW RELATIONS
% =====================================

father_in_law(X,Y):-
    spouse(Y,Z),
    father(X,Z).

mother_in_law(X,Y):-
    spouse(Y,Z),
    mother(X,Z).

son_in_law(X,Y):-
    male(X),
    spouse(X,Z),
    parent(Y,Z).

daughter_in_law(X,Y):-
    female(X),
    spouse(X,Z),
    parent(Y,Z).

brother_in_law(X,Y):-
    male(X),
    (spouse(Y,Z), brother(X,Z));
    (spouse(X,Z), sibling(Z,Y)).

sister_in_law(X,Y):-
    female(X),
    (spouse(Y,Z), sister(X,Z));
    (spouse(X,Z), sibling(Z,Y)).
