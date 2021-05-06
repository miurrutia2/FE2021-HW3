// Gmsh project created on Wed May  5 17:49:16 2021
SetFactory("OpenCASCADE");


//+
Point(1) = {-80, -20, 0, 1.0};
//+
Point(2) = {80, -20, 0, 1.0};
//+
Point(3) = {80, 20, 0, 1.0};
//+
Point(4) = {-80, 20, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Extrude {-20, 0, 0} {
	Curve{4};
}
//+
Extrude {20, 0, 0} {
	Curve{2};
}//+
Circle(11) = {0, 0, 0, 10, 0, 2*Pi};
//+
Curve Loop(4) = {11};
//+
Plane Surface(4) = {4};

BooleanDifference{ Surface{1}; Delete; }{ Surface{4}; Delete; }
//+
Physical Curve("Fixed") = {7};
//+
Physical Curve("Traction") = {10};
//+
Physical Surface("5mm") = {2, 3};
//+
Physical Surface("4mm") = {1};
//+
Transfinite Curve {11} = 50 Using Progression 1;

//+
MeshSize {3, 2, 7, 8} = 4;
//+
MeshSize {5, 4, 1, 6} = 4;
//+
MeshSize {1, 3, 2, 4} = 4;
//+
MeshSize {9} = 1;

//+
Extrude {0, 0, 2} {
  Surface{1}; Layers {5}; Recombine;
}
//+
Extrude {0, 0, -2} {
  Surface{1}; Layers {5}; Recombine;
}
//+
Extrude {0, 0, 2.5} {
  Surface{2}; Surface{3}; Layers {5}; Recombine;
}
//+
Extrude {0, 0, -2.5} {
  Surface{2}; Surface{3}; Layers {5}; Recombine;
}
