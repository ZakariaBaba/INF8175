% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)

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
array[1..card(equipes)] of equipes: equipe_du_terrain = to_enum(equipes, 1..card(equipes));


%Contrainte 1 Pour effectuer une rencontre, deux équipe doivent être présente sur le même terrain:
constraint forall(j in jours, i in equipes) (
  calendrier[i, j] > 0 ->
  (sum(k in equipes) (calendrier[k, j] > 0) = 2)
);



% Contrainte 2 :

% constraint forall(i in equipes) (
%   count(j in jours) (calendrier[i, j] = equipe_du_terrain[i]) >= 7
% );
             
%Contrainte 3 :

constraint forall(j in jours, i in equipes) (
  sum(k in equipes) (calendrier[k, j] = i) <= 2
);
%Contrainte 4 :
constraint forall(j in jours, i in equipes) (
  (sum(k in equipes) (calendrier[k, j] = i) = 0) -> (calendrier[i, j] = 0)
);


constraint forall(i in equipes) (
    sum([calendrier[i, j] == i | j in jours]) <= 7
);

%Contrainte 6 :
constraint forall(i, k in equipes where i != k) (
  rencontres[i, k] = 2
);
  
%Contrainte 7 :
constraint forall(i, k in equipes where i != k) (
  dates[i, k].2 - dates[i, k].1 >= 3 /\
  (sum(j in jours) (calendrier[i, j] = k) > 0 \/ sum(j in jours) (calendrier[k, j] = i) > 0) ->
  (dates[i, k].2 - dates[i, k].1 >= 3 /\ dates[i, k].2 - dates[i, k].1 <= min([j | j in jours where (sum(l in jours) (calendrier[i, l] = k /\ l > j) > 0)]))
);


%Contrainte 8 :
constraint forall(e1 in equipes, e2 in equipes where e1 != e2)(
    calendrier[e1, dates[e1, e2].1] != calendrier[e1, dates[e1, e2].2]
);

objectif_match_espaces =sum([if abs(dates[e1, e2].1 - dates[e1, e2].2) >= 6 then 1 else 0 endif | e1 in equipes, e2 in equipes where e1 != e2]);
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
