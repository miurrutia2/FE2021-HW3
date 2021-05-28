from numpy import *
from quad9 import quad9,quad9_post,quad9_stress_average
import modelo_placa_quad9_test as modelo_placa
from scipy.linalg import *


xy = modelo_placa.xy
conec = modelo_placa.conec
Quadrangles = modelo_placa.Quadrangles
Quadrangles_fixed = modelo_placa.Quadrangles_fixed
fixed_nodes = modelo_placa.fixed_nodes
natural_border = modelo_placa.natural_border
natural_nodes = modelo_placa.natural_nodes

kg = 1.
m = 1.
s = 1.
g = 9.80665*m/s**2
N = 1.*kg*g
Pa = N/m**2
kPa = 1e3*Pa
MPa = 1e6*Pa
GPa = 1e9*Pa

ρ_hormigon = 2500.*kg/m**3 #kg/m3

properties = {}
properties['E']  = 20*GPa
properties['nu'] = .25
properties['bx'] = 0
properties['by'] = 0#- ρ_hormigon*g
#properties['t']  = 1.


Nnodes = xy.shape[0]
Nelems = conec.shape[0]

NDOFs_per_node=2
NDOFs = NDOFs_per_node*Nnodes

K = zeros((NDOFs,NDOFs))
f = zeros((NDOFs,1))

for e in Quadrangles:
	n0 = int(conec[e,0])
	n1 = int(conec[e,1])
	n2 = int(conec[e,2])
	n3 = int(conec[e,3])
	n4 = int(conec[e,4])
	n5 = int(conec[e,5])
	n6 = int(conec[e,6])
	n7 = int(conec[e,7])
	n8 = int(conec[e,8])

	xy_e = xy[[n0,n1,n2,n3,n4,n5,n6,n7,n8],:]

	if e in Quadrangles_fixed:
		properties["t"] = 5.
	else:
		properties["t"] = 4.

	ke, fe = quad9(xy_e,properties)

	#Node k---> [3*k,3*k+1,3*k+2]
	d = [
	2*n0,2*n0+1,
	2*n1,2*n1+1,
	2*n2,2*n2+1,
	2*n3,2*n3+1,
	2*n4,2*n4+1,
	2*n5,2*n5+1,
	2*n6,2*n6+1,
	2*n7,2*n7+1,
	2*n8,2*n8+1]

	for i in range(len(d)):
		p = d[i]
		for j in range(len(d)):
			q = d[j]
			K[p,q] += ke[i,j]
		f[p] += fe[i]





from matplotlib import pylab as plt
#plt.matshow(K)
#plt.show()
#exit(-1)

constrained_DOFs=[]

for n in fixed_nodes:
	constrained_DOFs += [2*n,2*n +1]

free_DOFs = arange(NDOFs)
free_DOFs = setdiff1d(free_DOFs,constrained_DOFs)


####################################################### ver scipy.sparse.coo_matrix
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html#scipy.sparse.coo_matrix
Nelems_per_node = zeros((Nnodes,1))
for e in Quadrangles:
	for i in conec[e,:]:
		Nelems_per_node[i] += 1

#for node in natural_border:
#	f[2*node] = carga_distribuida/ Nelems_per_node[node]

Kff = K[ix_(free_DOFs,free_DOFs)]
Kfc = K[ix_(free_DOFs,constrained_DOFs)]
Kcf = K[ix_(constrained_DOFs,free_DOFs)]
Kcc = K[ix_(constrained_DOFs,constrained_DOFs)]

properties_load = {}
properties_load["t"] = 5
properties_load["tx"] = 1e3/(properties_load["t"]*4)
properties_load["ty"] = 0

#LINE LOAD


for nn in natural_nodes:
	ni = nn[0]
	nj = nn[2]
	nk = nn[1]

	xy_e = xy[[ni,nj,nk], :]
	
	xi =xy[ni,:]
	xj =xy[nj,:]
	xk =xy[nk,:]

	fe = zeros((6,1))

	L1 = norm(norm(xi-xj))
	L2 = norm(norm(xj-xk))

	fe[0] += properties_load['tx']*properties_load['t']*L1/2
	fe[1] += properties_load['ty']*properties_load['t']*L1/2
	fe[2] += properties_load['tx']*properties_load['t']*L1/2
	fe[3] += properties_load['ty']*properties_load['t']*L1/2

	fe[2] += properties_load['tx']*properties_load['t']*L2/2
	fe[3] += properties_load['ty']*properties_load['t']*L2/2
	fe[4] += properties_load['tx']*properties_load['t']*L2/2
	fe[5] += properties_load['ty']*properties_load['t']*L2/2

	'''
	for i in range(9):
		if i in [1,3,5,7,9]:
			y = properties_load["ty"]
		else:
			y = properties_load["tx"]
		
		fe.append(properties_load["t"]*y*L)
	'''

	d = [2*ni,2*ni+1,2*nj,2*nj+1,2*nk,2*nk+1]

	for i,force in enumerate(fe):
		f[d[i]] += force


ff = f[free_DOFs]
fc = f[constrained_DOFs]

# Solve


u = zeros((NDOFs,1))


u[free_DOFs] = solve(Kff,ff)



# Get reaction forces
R = Kcf @u[free_DOFs] + Kcc @ u[constrained_DOFs] - fc

uv = u.reshape([-1,2])

factor = 5e8
for e in Quadrangles:
	n0 = int(conec[e,0])
	n1 = int(conec[e,1])
	n2 = int(conec[e,2])
	n3 = int(conec[e,3])
	n4 = int(conec[e,4])
	n5 = int(conec[e,5])
	n6 = int(conec[e,6])
	n7 = int(conec[e,7])
	n8 = int(conec[e,8])

	xy_e = xy[[n0,n4,n1,n5,n2,n6,n3,n7,n0],:]
	uv_e = uv[[n0,n4,n1,n5,n2,n6,n3,n7,n0],:]
	#print([n0,n1,n2,n3,n4,n5,n6,n7,n8])
	#exit(0)


	plt.plot(xy_e[:,0]+factor*uv_e[:,0],xy_e[:,1]+factor*uv_e[:,1],'k')
#plt.plot(xy[:,0]+factor*uv[:,0],xy[:,1]+factor*uv[:,1],'.')
plt.axis('equal')
plt.show()

#print(f'max = {(uv[1][1]+uv[2][1])/2e-5}*1e5*m')



##### Post
from gmsh_post import write_node_data , write_node_data_2 , write_element_data

import os
try:
	os.mkdir('POST')#Crear carpeta POST
except:
	pass
nodes = arange(1,Nnodes +1)
write_node_data(f'POST/Fine/ux.msh', nodes, uv[:,0],'Despl. X')
write_node_data(f'POST/Fine/uy.msh', nodes, uv[:,1],'Despl. Y')
write_node_data_2(f'POST/Fine/desplazamientos.msh',nodes, uv[:,0],uv[:,1],'Despl')

σxx_node = zeros((Nnodes,1))
σyy_node = zeros((Nnodes,1))
σxy_node = zeros((Nnodes,1))



gauss = [
	[   -sqrt(3/5) , -sqrt(3/5), 5/9, 0],
	[        0     , -sqrt(3/5), 8/9, 1],
	[    sqrt(3/5) , -sqrt(3/5), 5/9, 2],
	[   -sqrt(3/5) ,      0    , 5/9, 3],
	[        0     ,      0    , 8/9, 4],
	[    sqrt(3/5) ,      0    , 5/9, 5],
	[   -sqrt(3/5) ,  sqrt(3/5), 5/9, 6],
	[        0     ,  sqrt(3/5), 8/9, 7],
	[    sqrt(3/5) ,  sqrt(3/5), 5/9, 8],]

for e in Quadrangles:
	n0 = int(conec[e,0])
	n1 = int(conec[e,1])
	n2 = int(conec[e,2])
	n3 = int(conec[e,3])
	n4 = int(conec[e,4])
	n5 = int(conec[e,5])
	n6 = int(conec[e,6])
	n7 = int(conec[e,7])
	n8 = int(conec[e,8])

	xy_e = xy[[n0,n1,n2,n3,n4,n5,n6,n7,n8],:]
	uv_e = uv[[n0,n1,n2,n3,n4,n5,n6,n7,n8],:]
	u_e = uv_e.reshape((18,1))

	εe,σe =quad9_post(xy_e, u_e ,properties)

	σxx = zeros((9,1))
	σyy = zeros((9,1))
	σxy = zeros((9,1))

	for ξ,η,wi,i in gauss:
		properties['xi'] = ξ
		properties['eta'] = η
		ε,(σxx[i],σyy[i],σxy[i]) = quad9_post(xy_e,u_e,properties)

	σxx_node[[n0,n1,n2,n3,n4,n5,n6,n7,n8],:] +=  quad9_stress_average(σxx,xy_e, properties) 
	σyy_node[[n0,n1,n2,n3,n4,n5,n6,n7,n8],:] +=  quad9_stress_average(σyy,xy_e, properties) 
	σxy_node[[n0,n1,n2,n3,n4,n5,n6,n7,n8],:] +=  quad9_stress_average(σxy,xy_e, properties) 


	#σxx[i] = quad9_stress_average(σe[0])
	#σyy[i] = quad9_stress_average(σe[1])
	#σxy[i] = quad9_stress_average(σe[2])
	#print(f'POST/e = {e}, sigma = {σe}')

	#i+=1
	#xy_e = xy[ [ni,nj,nk,nl,ni] ,:]
	#uv_e = uv[ [ni,nj,nk,nl,ni] ,:]
	#plt.plot(xy_e[:,0]+factor*uv_e[:,0],xy_e[:,1]+factor*uv_e[:,1],'k')
	
for node, cant in enumerate(Nelems_per_node):
	σxx_node[node] /= cant
	σyy_node[node] /= cant
	σxy_node[node] /= cant


#plt.plot(xy[:,0] + factor*uv[:,0],xy[:,1] + factor*uv[:,1],'r.')
#plt.axis('equal')
#plt.show()
print(f'sigma_x_node_max = {max(σxx_node)}')
print(f'sigma_x_node_min = {min(σxx_node)}')


write_node_data(f'POST/Fine/sigma_xx_per_node.msh', nodes, array(σxx_node),'Sigma_xx')
write_node_data(f'POST/Fine/sigma_yy_per_node.msh', nodes, array(σyy_node),'Sigma_yy')
write_node_data(f'POST/Fine/sigma_xy_per_node.msh', nodes, array(σxy_node),'Sigma_xy')


#elementos = array(Quadrangles)+1
#write_element_data(f'POST/sigma_x.msh',elementos, σxx,'Sigma_x')
#write_element_data(f'POST/sigma_y.msh',elementos, σyy,'Sigma_y')
#write_element_data(f'POST/sigma_xy.msh',elementos, σxy,'Sigma_xy')