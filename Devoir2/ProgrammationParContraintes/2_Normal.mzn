%Zakaria Babahadji (2028025)
%NGOUNOU TCHAWE Armel (2238017)

include "globals.mzn";

% États possibles pour une case du terrain
% V = Vide
% B = Tour bleue
% R = Tour rouge
enum etat = {V, B, R};

% Dimension du terrain (carré)
int: n;
set of int: dim = 1..n;

% État du terrain
array[dim, dim] of var etat: terrain;

% Variable objectif à maximiser
var int: total_commun;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%

% Nombre égal de tour
constraint sum(i in 1..n, j in 1..n)(terrain[i,j] == R) == sum(i in 1..n, j in 1..n)(terrain[i,j] == B);

% Reflexion verticale
constraint forall(i in 1..n, j in 1..n where i <= j) (
    terrain[i, j] == terrain[j, i]
);

%Croisements horizontals 
constraint forall(i, j in dim where terrain[i, j] == R) (
              (forall(k in dim where k != j)(terrain[i, k] != B)) /\
              (forall(k in dim where k != j)(terrain[k, j] != B))
            );
%Croisements verticals
constraint forall(i,j in dim where terrain[i,j] == R) (
              (forall(k in dim where k != i)(terrain[i, k] != B)) /\
              (forall(k in dim where k != i)(terrain[k, j] != B))
              );
              
%Croisements Diagonals            
constraint forall(i, j in dim where terrain[i, j] == R) (
                  forall(d_i,d_j in dim where d_i !=i /\ d_j != j )(
                    let {
                          int: diff_i = abs(d_i - i);
                          int: diff_j = abs(d_j - j);
                    } in
                    (
                    terrain[d_i, d_j] != B) \/ (diff_i != diff_j)
                    
                  )
            );


total_commun = sum(i in 1..n, j in 1..n)(terrain[i,j] == R);

solve maximize total_commun;
%-----------------------------------------------------------------------------%
output 
["Terrain :\n"]
++
[if j = 1 then "["  endif ++ if fix(terrain[i,j]) == V then "_" else show(terrain[i,j]) endif ++ if j = n then "]\n" else "," endif | i in 1..n, j in 1..n]
++
["\n"]
++
["Total de tours commun: " ++ show(total_commun)]
