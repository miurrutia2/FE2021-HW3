# FE2021-HW3
# PART 1
## Mesh

![](Mesh1.png)


## Geometry

![](Geometry.png)

## New Mesh
![](New_mesh.png)


![](Deformada.png)

## Displacements

![](Desplazamientos.png)


## Sigma X

![](SigmaX.png)


# PART 2

### Nodal stress averaging post-processing:

To calculate the stresses, extrapolation from Gauss Points was used, in this method the stresses at the Gauss points are evaluated and then extrapolated to the corners of the quadrilateral element where the nodes are.

First, the natural coordinates of each element were obtained, these being:

![](Part2/Image/Natural_coordinates.png)

Once these coordinates are obtained, we can obtain N1, N2, N3 and N4, using the following equations:

![](Part2/Image/Ns.png)

With these values, we can assemble the matrix N of 4x4, which is as follows.

![](Part2/Image/N.png)

Finally, the equation ω = N∙ω' will be used, where ω' is equal to (σxx,σyy,σxy,εxy), previously calculated.

## Coarse mesh stress
![](Part2/plots/Coarse.png)

## Coarse mesh stress with nodal stress averaging post-processing
![](Part2/plots/Coarse_average.png)

## Medium mesh stress
![](Part2/plots/Medium.png)

## Medium mesh stress with nodal stress averaging post-processing
![](Part2/plots/Medium_average.png)

## Fine mesh stress
![](Part2/plots/Fine.png)

## Fine mesh stress with nodal stress averaging post-processing
![](Part2/plots/Fine_average.png)


The difference between both methods is quite noticeable in the plots that can be seen above. This is because the methods for obtaining stresses from displacements tend to be less accurate. In addition, the Nodal stress averaging post-processing method is usually more accurate, so it can be assumed that the results obtained by this method are closer to reality.


