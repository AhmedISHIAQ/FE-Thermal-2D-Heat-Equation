nbele = 1;
nbpt = nbele+1;

size= 2.;

ta = 2.*size/nbele;
/* Point      1 */
Point(newp) = {.0,.0,0.0,ta};
/* Point      2 */
Point(newp) = {size,.0,0.0,ta};
/* Point      3 */
Point(newp) = {0.0,size,0.0,ta};

Line(9)  = {1,2};
Line(10) = {2,3};
Line(11) = {3,1};
  
Line Loop(18) = {9,10,11};
Ruled Surface(21) = {18};
/*Plane Surface(21) = {18};*/ 


Physical Surface (1000)  = {21} ;











