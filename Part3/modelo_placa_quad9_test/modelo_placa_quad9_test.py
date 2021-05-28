import numpy as np

fid  = open('malla_fine.msh','r')


'''
quad9
$Elements
16
1 8 2 6 2 2 8 9
5 10 2 7 1 2 18 22 5 26 27 28 7 29
5 | 10 | 2 | 7 | 1 | 2 18 22 5 26 27 28 7 29

quad4
$Elements
1461
1 1 2 14 5 4 58
37 3 2 12 1 6 234 368 50

'''


LINE_ELEMENT =  8
QUAD_ELEMENT =  3
QUAD9_ELEMENT= 10

EMPOTRADO = 14
BORDE_NATURAL = 15
PLACA  = 13
EXTREMOS = 12

natural_nodes = []

while True:
	line = fid.readline() 
	if line.find('Nodes') >=0:
		break
	elif line.find('EndElements') >=0:
		break

Nnodes = int(fid.readline())

xy = np.zeros([Nnodes,2])

for i in range(Nnodes):
	line = fid.readline()
	sl = line.split()
	xy[i,0]= float(sl[1])
	xy[i,1]= float(sl[2])

EndNodes = fid.readline()
if fid.readline().find('Elements') >=0:
	NElm = int(fid.readline())
	conec = np.zeros([NElm,9],dtype=int)
	fixed_nodes = []
	natural_border = []
	Nquads = 0
	Quadrangles = []
	Quadrangles_fixed = []
	for i in range(NElm):
		line = fid.readline().split()

		element_number = int(line[0]) -1 
		element_type   = int(line[1])
		physical_grp   = int(line[3])
		entity_number  = int(line[4])


		if element_type == LINE_ELEMENT and \
			physical_grp == EMPOTRADO:
			n1 = int(line[5])-1
			n2 = int(line[6])-1
			n3 = int(line[7])-1
			fixed_nodes += [n1,n2,n3]
		elif element_type == LINE_ELEMENT and \
			physical_grp == BORDE_NATURAL:
			n1 = int(line[5])-1
			n2 = int(line[6])-1
			n3 = int(line[7])-1
			natural_border += [n1,n2,n3]
			natural_nodes += [[n1,n2,n3]]
		elif element_type==QUAD9_ELEMENT and \
			(physical_grp==PLACA or physical_grp==EXTREMOS):
			n0 = int(line[5 ])-1
			n1 = int(line[6 ])-1
			n2 = int(line[7 ])-1
			n3 = int(line[8 ])-1
			n4 = int(line[9 ])-1
			n5 = int(line[10])-1
			n6 = int(line[11])-1
			n7 = int(line[12])-1
			n8 = int(line[13])-1

			conec[element_number,:] = [n0,n1,n2,n3,n4,n5,n6,n7,n8]
			Nquads +=1
			Quadrangles.append(element_number)
			if physical_grp==EXTREMOS:
				Quadrangles_fixed.append(element_number)

fixed_nodes = np.unique(fixed_nodes)
natural_border = np.unique(natural_border)

fid.close()

if __name__ == '__main__':
	print(f'conec = \n{conec}\n')
	print(f'Quadrangles    = {Quadrangles}')
	print(f'fixed_nodes    = {fixed_nodes}')
	print(f'natural_border = {natural_border}')