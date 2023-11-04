include "globals.mzn";

var 1000..9999: nombre;

array[1..4] of var 1..9: chiffres;

constraint nombre mod 2 == 0;
constraint all_different(chiffres);
constraint chiffres[1] > chiffres[2];
constraint chiffres[3] < chiffres[4];
constraint chiffres[2] > chiffres[4];
constraint sum(chiffres) > 15;
solve minimize chiffres[2]*chiffres[3]*chiffres[4];

nombre = chiffres[1]*10^3+chiffres[2]*10^2+chiffres[3]*10+chiffres[4];

output [
  show(nombre)
];

