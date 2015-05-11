arc(m,p,8).
arc(q,p,11).
arc(q,m,5).
arc(k,q,3).

path(A,B,[A,B],P):-arc(A,B,P).
path(A,B,[A|D],Q):-arc(A,Z,P), path(Z,B,D,G), Q is P+G.


compare(CP1,CC1,CP2,CC2,Path,Cost):- 
        CC1>CC2,
        Path = CP2,
        Cost = CC2.

compare(CP1,CC1,CP2,CC2,Path,Cost):-
        Path = CP1,
        Cost = CC1.

        
choosepath(Y,CP,CC,Path,Cost):-
        Y=[_|_],
        [K|M] = Y,
        [C|P] = K,
        choosepath(M,P,C,Path1,Cost1),
        compare(CP,CC,Path1,Cost1,Path,Cost).

choosepath([],CP,CC,Path,Cost):-
        Path = CP,
        Cost = CC.
        
shortestpath(A,B,Path,Cost):-
        /*After I wrote out these codes, I known that the compound elements in a set which is obtained by the function "setof" are ordered.
        In this case, the term in a set is combined by Cost and Path. The compound terms in a set are ordered by their first arguments which 
        are costs of all the paths, Hence, we could directly extract the first term in the solution set and output its first path. As you see
        in my programe, I realized compare function to choose the minimum pathcost and its correponding shortest path. What I want by writing
        these comments here is to say we could realize what we want not like what I did in this program. But actually, I have learned a lot by
        realizing this programe. */
        setof([L,P],path(A,B,P,L),Set),
        Set = [_|_],
        [X|Y]=Set,
        [CC|CP]= X,
        choosepath(Y,CP,CC,Path,Cost).
