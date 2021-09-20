# Program ... Setter
# Date ...... 20 / 10 / 20
# Name ...... Edgar A.


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#
# blockMeshDict
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Read the turbine's operational parameters
dataFile = open('data', 'r')

NACA = int( dataFile.readline().rstrip(';\n').split()[1] )
BPA = float( dataFile.readline().rstrip(';\n').split()[1] )
NB = int( dataFile.readline().rstrip(';\n').split()[1] )
CH = float( dataFile.readline().rstrip(';\n').split()[1] )
R = float( dataFile.readline().rstrip(';\n').split()[1] )
RPM = float( dataFile.readline().rstrip(';\n').split()[1] )
LAMBDA = float( dataFile.readline().rstrip(';\n').split()[1] )
U0 = float( dataFile.readline().rstrip(';\n').split()[1] )
RI = float( dataFile.readline().rstrip(';\n').split()[1] )
RO = float( dataFile.readline().rstrip(';\n').split()[1] )

dataFile.close()

# Read the coordinates
coordinatesFile = open('coordinates', 'r')

lines = coordinatesFile.readlines()

x = []
y = []
k = []

for line in lines:
	col1, col2, col3 = line.strip().split()
	x.append(float(col1))
	y.append(float(col2))
	k.append(int(col3))

coordinatesFile.close()

# Find the domain's dimensions
minx = min(x)
maxx = max(x)
miny = min(y)
maxy = max(y)

# One turbine case
if len(lines) == 1:
    rectMinX = -6.00 * R
    rectMaxX =  6.00 * R
    rectMinY = -6.00 * R
    rectMaxY =  6.00 * R

else:
    rectMinX = minx - 6.00 * R
    rectMaxX = maxx + 12.00 * R        
    rectMinY = miny - 6.00 * R
    rectMaxY = maxy + 6.00 * R

# Set the number of cells according to crosswidth length

# Number of cells diameterwise
nCellsDiam = 30

nYCells = round( nCellsDiam * abs(rectMaxY - rectMinY) / (2 * R) )
nXCells = int (round( nYCells * abs(rectMaxX - rectMinX) / abs(rectMaxY - rectMinY) ) )

# Write the variable file
variableFile = open('blockMeshVariablePart', 'w')

variableFile.write('vertices\n')
variableFile.write('(\n')
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMinX, rectMinY, -1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMaxX, rectMinY, -1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMaxX, rectMaxY, -1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMinX, rectMaxY, -1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMinX, rectMinY,  1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMaxX, rectMinY,  1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMaxX, rectMaxY,  1))
variableFile.write('\t({0:5.0f} {1:5.0f} {2:5.0f})\n'.format(rectMinX, rectMaxY,  1))
variableFile.write(');\n\n')

variableFile.write('blocks\n')
variableFile.write('(\n')
variableFile.write('\thex (0 1 2 3 4 5 6 7) ({0:} {1:} 1) simpleGrading (1 1 1)\n'.format(nXCells, nYCells))
variableFile.write(');\n\n')

variableFile.close()

# Link the blockMesh files
filenames = ['blockMeshBanner', 'blockMeshVariablePart', 'blockMeshBoundary']
with open('blockMeshDict', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#
# fvSolution
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Write the fvSolution variable file
variableFile = open('fvSolutionVariablePart', 'w')

variableFile.write('numberOfCylinders\n')
variableFile.write('{\n')
variableFile.write('\tnoc\t\t{};\n'.format(len(x)))
variableFile.write('}\n\n')

variableFile.write('general\n')
variableFile.write('{\n')
variableFile.write('\tNACA\t\t{};\n'.format(NACA))
variableFile.write('\tBPA\t\t\t{};\n'.format(BPA))
variableFile.write('\tNB\t\t\t{};\n'.format(NB))
variableFile.write('\tCH\t\t\t{0:.2f};\n'.format(CH))
variableFile.write('\tR\t\t\t{0:.2f};\n'.format(R))
variableFile.write('\tRPM\t\t\t{0:.2f};\n'.format(RPM))
variableFile.write('\tLAMBDA\t\t{0:.2f};\n'.format(LAMBDA))
variableFile.write('\tU0\t\t\t{0:.2f};\n'.format(U0))
variableFile.write('}\n\n')

for ix, (xi, yi, ki) in enumerate( zip(x, y, k) ):
	variableFile.write('actuatorCylinder{}\n'.format(ix)) 
	variableFile.write('{\n')
	variableFile.write('\tcenter\t\t({0:6.2f} {1:6.2f} {2:6.2f});\n'.format(xi, yi, 0.00))
	variableFile.write('\tintRadius\t{0:.2f};\n'.format(RI))
	variableFile.write('\textRadius\t{0:.2f};\n'.format(RO))
	variableFile.write('\tspin\t\t{0:1d};\n'.format(ki))
	variableFile.write('}\n\n')

variableFile.close()

# Link the fvSolution files
filenames = ['fvSolutionSettings', 'fvSolutionVariablePart']
with open('fvSolution', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())


