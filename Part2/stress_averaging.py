from numpy import array, pi, zeros, ix_, meshgrid, sqrt, ones, int32, unique, setdiff1d, arange
from quad4 import quad4, quad4_post
import matplotlib.pylab as plt
from scipy.linalg import solve

fid = open("Hw3.msh", "r")

LINE_ELEMENT = 1
QUAD_ELEMENT = 3

Empotrado = 1
BordeNatural = 2
Placa = 3
Extremos = 4
while True:

	line = fid.readline()
	if line.find("$Nodes") >= 0:
		break
	#print(line)

Nnodes = int(fid.readline())

xy = zeros([Nnodes,2])

for i in range(Nnodes):
	line = fid.readline()
	sl = line.split()
	xy[i,0] = float(sl[1])
	xy[i,1] = float(sl[2])


def stress_averaging(xy, properties):

	E = properties["E"]
	ν = properties["nu"]
	bx = properties["bx"]
	by = properties["by"]
	t = properties["t"]

	Eσ = E / (1-ν**2) * array(
		[
		[1 , ν , 0       ]       ,
		[ν , 1 , 0       ]       ,
		[0 , 0 , (1-ν)/2 ]
		])

	x0 = xy[0,0]
	x1 = xy[1,0]
	x2 = xy[2,0]
	x3 = xy[3,0]

	y0 = xy[0,1]
	y1 = xy[1,1]
	y2 = xy[2,1]
	y3 = xy[3,1]

	ke = zeros((8,8))
	fe = zeros((8,1))

	#Primer punto de Gauss de la regla 2x2
	# xi = 1.0 / sqrt(3)
	# eta = -1.0 / sqrt(3)
	# wi = 1.0
	# wj = 1.0

	gauss_rule = [
		(-1.0 / sqrt(3), -1.0 / sqrt(3), -1.0, -1.0),
		( 1.0 / sqrt(3), -1.0 / sqrt(3), 1.0, -1.0),
		( 1.0 / sqrt(3),  1.0 / sqrt(3), 1.0, 1.0),
		(-1.0 / sqrt(3),  1.0 / sqrt(3), -1.0, 1.0),
	]

	for xi, eta, ξ, η in gauss_rule:

		# print(f"xi = {xi} eta = {eta}")
		N1 = (1-ξ)*(1-η)/4
		N2 = (1+ξ)*(1-η)/4
		N3 = (1+ξ)*(1+η)/4
		N4 = (1-ξ)*(1+η)/4

		N = zeros((4, 4))

		N[0,0] = N3
		N[0,1] = N4
		N[0,2] = N1
		N[0,3] = N2
		N[1,0] = N2
		N[1,1] = N3
		N[1,2] = N4
		N[1,3] = N1
		N[2,0] = N1
		N[2,1] = N2
		N[2,2] = N3
		N[2,3] = N4
		N[3,0] = N4
		N[3,1] = N1
		N[3,2] = N2
		N[3,3] = N3

		

	return N



