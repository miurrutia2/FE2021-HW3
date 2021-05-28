// Gmsh project created on Wed May 05 21:40:48 2021
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {200, 0, 0, 1.0};
//+
Point(3) = {200, 40, 0, 1.0};
//+
Point(4) = {0, 40, 0, 1.0};
//+
Point(5) = {20, 0, 0, 1.0};
//+
Point(6) = {20, 40, 0, 1.0};
//+
Point(7) = {180, 0, 0, 1.0};
//+
Point(8) = {180, 40, 0, 1.0};
//+
Circle(1) = {100, 20, 0, 10, 0, 2*Pi};
//+
Line(2) = {1, 5};
//+
Line(3) = {5, 6};
//+
Line(4) = {6, 4};
//+
Line(5) = {4, 1};
//+
Line(6) = {5, 7};
//+
Line(7) = {7, 8};
//+
Line(8) = {8, 6};
//+
Line(9) = {7, 2};
//+
Line(10) = {2, 3};
//+
Line(11) = {3, 8};
//+
Curve Loop(1) = {5, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {6, 7, 8, -3};
//+
Curve Loop(3) = {1};
//+
Plane Surface(2) = {2, 3};
//+
Curve Loop(4) = {9, 10, 11, -7};
//+
Plane Surface(3) = {4};
//+
Physical Surface("FIXED PLATE", 12) = {1, 3};
//+
Physical Surface("MIDDLE PLATE", 13) = {2};
//+
Physical Curve("LINE CONSTRAINT", 14) = {5};
//+
Physical Curve("NATURAL BOUNDARY", 15) = {10};
