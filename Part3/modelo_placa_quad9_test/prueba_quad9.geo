// Gmsh project created on Tue May 25 14:43:06 2021
SetFactory("OpenCASCADE");
//+
Point(1) = {-1, -1, 0, 1.0};
//+
Point(2) = { 1, -1, 0, 1.0};
//+
Point(3) = { 1,  1, 0, 1.0};
//+
Point(4) = {-1,  1, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Plane Surface(1) = {1};
//+
Physical Curve("LINE CONSTRAIN", 5) = {4};
//+
Physical Curve("NATURAL BOUNDARY", 6) = {2};
//+
Physical Surface("MIDDLE PLATE", 7) = {1};
