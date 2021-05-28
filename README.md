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



# PART 3

The quad9 element is a 2-dimensional quadrilateral element that is made up of 9 nodes, unlike the quad4 element, which is made up of only 4. Despite this difference, quad9 works in the same way as quad4 does, but with arrays of different dimensions, due to the increased number of nodes.
Quad9 type elements can be very useful, since by presenting a greater number of nodes, they can describe curves, and the stiff behavior of quad4 elements is avoided.

For both quad9 and quad4, 3 different meshes were created, a fine (h = 0.25), a medium (h = 0.5) and a thick (h = 1).
### Maximum absolute stresses quad4
![](Part3/plots/Quad4plot.png)

### Maximum absolute stresses quad9
![](Part3/plots/Quad9plot.png)

As can be seen in the plots above, in both cases the stresses decrease as the size of the mesh increases. However, with quad4 elements, when going from fine mesh to medium mesh, the stresses decrease more quickly than with quad9. However, when going from the medium mesh to the coarse mesh, the stresses decrease with the same slope in both cases.

Quad4 has higher absolute stresses than Quad9, this may be due to the fact that quad9 better models the deformation of the element, which results in lower stresses.
With quad4 elements, the best results are obtained with thicker meshes, since this element is very stiff in some cases.
