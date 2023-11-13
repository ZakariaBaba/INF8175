%Zakaria Babahadji (2028025)
%NGOUNOU TCHAWE Armel (2238017)

include "globals.mzn";

% Énumérations des équipes participant au tournoi
enum equipes = {CO, TA, HO, DA, NA, MU, AL, UT};

% Lieux de rencontres des equipes (0 = pas de rencontre).
% Tout lieu i, tel que 0 < i <= card(equipes), 
% est designé comme le domicile de l'équipe associée par la relation to_enum(equipe, i)
set of int: terrains = 0..card(equipes);

% Étendue du tournoi (en jours)
int: d = 16;
set of int: jours = 1..d;

% Calendrier de placement des matchs
array[equipes, jours] of var terrains: calendrier;

% Nombres de rencontres entre deux equipes
array[equipes, equipes] of var 0..2: rencontres;

% Tuples des dates de match entre deux équipes
array[equipes, equipes] of var tuple (0..d, 0..d): dates;

% Variable objectif à maximiser
var int: objectif_match_espaces;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%


%Contrainte 1 et 2 Pour effectuer une rencontre, deux équipe doivent être présente sur le même terrain  
% et un match doit avoir lieu sur le terrain désigné comme le domicile de l’une des deux équipes:
constraint forall(e1, e2 in equipes where e1 < e2) (
    (calendrier[e1, dates[e1, e2].1] = to_enum(equipes, e1) \/ calendrier[e1, dates[e1, e2].1] = to_enum(equipes, e2)) /\
    (calendrier[e1, dates[e1, e2].2] = to_enum(equipes, e1) \/ calendrier[e1, dates[e1, e2].2] = to_enum(equipes, e2) )
);    
             
%Contrainte 3 Un terrain ne peut accueillir plus de deux équipes:
constraint forall(j in jours, e in equipes) (
  sum(k in equipes) (calendrier[k, j] = e) <=2
);


%Contrainte 4 Si une équipe ne joue pas lors d’une période elle est placée sur le terrain n°0:
constraint forall(j in jours, e in equipes)(
  calendrier[e,j] == 0 \/ calendrier[e,j]>0 
);

%Contrainte 5 Une équipe ne doit pas jouer plus de 7 jours sur son propre terrain (à domicile)
constraint forall(e in equipes) (
    count(j in jours)(calendrier[e, j] = to_enum(equipes, e)) = 7 /\
    all_different([dates[e, e2].1 | e2 in equipes where e != e2]) /\
    all_different([dates[e, e2].2 | e2 in equipes where e != e2]) 
  
);

% %Contrainte 7 Les deux rencontres de deux équipes doivent être espacées de 3 jours au minimum :
constraint forall(e1, e2 in equipes where e1 < e2) (
  abs(dates[e1, e2].2 - dates[e1, e2].1) >= 3 /\
  %Contrainte 6 Les équipes doivent jouer deux fois l’une contre l’autre. :
   dates[e1, e2] = dates[e2, e1]
);


%Contrainte 8 Les deux rencontres de deux équipes doivent avoir lieu sur des terrains différents:
constraint forall(e1 in equipes, e2 in equipes where e1 < e2)(
    calendrier[e1, dates[e1, e2].1] != calendrier[e1, dates[e1, e2].2]
);

objectif_match_espaces = sum(e1, e2 in equipes where e1 < e2) (
    abs(dates[e1, e2].2 - dates[e1, e2].1)  >=  6
);
solve maximize objectif_match_espaces;



%-----------------------------------------------------------------------------%

% Affichage du calendrier par equipes et par jours puis du résultat de la fonction objectif.
% Lorsqu'une équipe ne joue pas, l'emplacement de match reste vide sinon elle contient le nom de l'équipie adverse.
% Si une équipe ne joue pas à domicile, un "@" précède le nom de l'équipe adverse.
output 
["Calendrier:\n"]
++
[if j = 1 then "   " else "" endif ++ if j < 10 then "  j" ++ show(j) else " j" ++ show(j) endif ++ if j = d then "\n" else "" endif | j in jours ]
++
[if j = 1 then show(e1) ++ ":" else "" endif ++ if fix(calendrier[e1,j]) = 0 then "    " else if fix(calendrier[e1,j]) = e1 then "  " ++ concat([if e1 != e2 /\ fix(calendrier[e2,j]) = e1 then show(e2) else "" endif | e2 in equipes])  else " @" ++ show(to_enum(equipes, calendrier[e1,j])) endif endif ++ if j = d then "\n" else "" endif | e1 in equipes, j in jours ]
++
["\nMatchs retour espacés de 6 jours ou plus = " ++ show(objectif_match_espaces) ++ "\n"]
;
