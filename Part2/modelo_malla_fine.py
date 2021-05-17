from numpy import array, pi, zeros, ix_, meshgrid, sqrt, ones, int32, unique, setdiff1d, arange
from quad4 import quad4, quad4_post
import matplotlib.pylab as plt
from scipy.linalg import solve
from stress_averaging import stress_averaging


fid = open("Hw3_fine.msh", "r")

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


while True:

	line = fid.readline()
	if line.find("$Elements") >= 0:
		break

Nelem = int(fid.readline())
conec = zeros((Nelem,4), dtype = int32)

fixed_nodes = []

Nquads = 0

Quadrangles = []
T = []

for i in range(Nelem):
	line = fid.readline()
	sl = line.split()
	element_number = int32(sl[0]) - 1
	element_type = int32(sl[1])
	physical_grp = int32(sl[3])
	entity_number = int32(sl[4])

	if element_type == LINE_ELEMENT and physical_grp == Empotrado:

		n1 = int32(sl[5])-1
		n2 = int32(sl[6])-1
		fixed_nodes += [n1, n2]


	if element_type == QUAD_ELEMENT and (physical_grp == Placa or physical_grp == Extremos):
		n0 = int32(sl[5])-1
		n1 = int32(sl[6])-1
		n2 = int32(sl[7])-1
		n3 = int32(sl[8])-1

		conec[element_number, :] = [n0, n1, n2, n3]

		Quadrangles.append(element_number)
		Nquads += 1

	

fid.close()

rho = 2500.
g = 0.91

properties = {}
properties["E"] = 20e9
properties["nu"] = 0.25
properties["bx"] = 0.
properties["by"] = 0.
#properties["t"] = 4e-3

NDOFs_per_node = 2
NDOFs = 2 * Nnodes

K = zeros((NDOFs, NDOFs))
f = zeros((NDOFs, 1))


for e in Quadrangles:
	ni = int(conec[e,0])
	nj = int(conec[e,1])
	nk = int(conec[e,2])
	nl = int(conec[e,3])


	print(f"e = {e} ni = {ni} nj = {nj} nz = {nk} nl = {nl}")

	xy_e = xy[[ni, nj, nk, nl], :]

	if e in range(1760,2145):
		properties["t"] = 5e-3
	else:
		properties["t"] = 4e-3

	
	#print(xy_e)

	ke, fe = quad4(xy_e, properties)

	d = [2*ni, 2*ni+1, 2*nj, 2*nj+1, 2*nk, 2*nk+1, 2*nl, 2*nl+1]

	for i in range(8):
		p = d[i]
		for j in range(8):
			q = d[j]
			K[p,q] += ke[i,j]
		f[p] += fe[i]
	

#print(K)
#print(f)
free = []
constrained_DOFs = []
fixed_nodes = unique(fixed_nodes)


for n in fixed_nodes:

	constrained_DOFs += [2*n, 2*n+1]
print(f"cons = {constrained_DOFs}")
free_DOFs = arange(NDOFs)
free_DOFs = setdiff1d(free_DOFs, constrained_DOFs)

nodes = [19-1, 34-1,26-1,33-1,22-1,32-1,25-1,31-1,21-1,30-1,24-1,29-1,20-21,28-1,23-1,27-1,18-1]

for n in nodes:
	f[2*n] = 1.0

Kff = K[ix_(free_DOFs,free_DOFs)]
Kfc = K[ix_(free_DOFs,constrained_DOFs)]
Kcf = K[ix_(constrained_DOFs,free_DOFs)]
Kcc = K[ix_(constrained_DOFs,constrained_DOFs)]



ff= f[free_DOFs]
fc = f[constrained_DOFs]

u = zeros((NDOFs,1))

u[free_DOFs] = solve(Kff, ff)

R = Kcf@u[free_DOFs] + Kcc@u[constrained_DOFs] - fc


print(f"u={u}")
print(f"R={R}")


factor = 2e7
uv = factor*u.reshape([-1,2])
#plt.plot(xy[:,0] + uv[:,0], xy[:,1] + uv[:,1], ".")

for e in Quadrangles:

	ni = int(conec[e,0])
	nj = int(conec[e,1])
	nk = int(conec[e,2])
	nl = int(conec[e,3])

	xy_e = xy[[ni, nj, nk, nl, ni], :] + uv[[ni, nj, nk, nl, ni], :]
	plt.plot(xy_e[:,0],xy_e[:,1],"k")

	#xy_e2 = xy[[ni, nj, nk, ni], :]
	#plt.plot(xy_e2[:,0],xy_e2[:,1], ":")
plt.axis("equal")
#plt.show()

from gmsh_post import write_node_data, write_node_data_2, write_element_data

nodes = arange(1,Nnodes+1)
write_node_data("ux.msh", nodes, uv[:,0], "Despl. X")
write_node_data("uy.msh", nodes, uv[:,1], "Despl. Y")
write_node_data_2("desplazamientos.msh", nodes, uv[:,0], uv[:,1], "Despl")


i = 0

σxx = zeros(len(Quadrangles)+1)
σyy = zeros(len(Quadrangles)+1)
σxy = zeros(len(Quadrangles)+1)
new_σxx = []
for e in Quadrangles:
	ni = int(conec[e,0])
	nj = int(conec[e,1])
	nk = int(conec[e,2])
	nl = int(conec[e,3])

	xy_e = xy[[ni, nj, nk, nl, ni], :]

	uv_e = uv[[ni, nj, nk, nl], :]

	u_e = uv_e.reshape((-1))

	εe, σe = quad4_post(xy_e, u_e, properties)

	σxx[i] = σe[0]
	σyy[i] = σe[1]
	σxy[i] = σe[2]

	ωp = [σe[0], σe[1], σe[2], εe[2]]

	N = stress_averaging(xy, properties)
	
	ω = N@ωp
	
	new_σxx.append(ω[0])

	i+=1


elementos = array(Quadrangles)+1
write_element_data("sigma_x_fine.msh", elementos, σxx, "Sigma_x")
write_element_data("new_sigma_x_fine.msh", elementos, new_σxx, "New_Sigma_x")

	