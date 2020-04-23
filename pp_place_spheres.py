import maya.cmds as cmds
from random import uniform, seed

# In the "RenderManProceduralShape->Scripts->Pre Shape Python Script" copy the following text:

# import rfm2.api.strings as apistr;import pp_place_spheres;pp_place_spheres.setDataStr(apistr.expand_string("<shape>"))
def setDataStr(shapeName):
	tnode = cmds.getAttr(shapeName + '.target')
	# If the name of the transform node of the target shape has
	# not been specified we assume the RenderManProgram has been
	# parented to the polymesh that will "receive" the spheres.
	'''
	if len(tnode) == 0:
		tnode = cmds.listRelatives(shapeName, parent=True)[0]
		tnode = cmds.listRelatives(tnode, parent=True)[0]
	'''
	rad = str(cmds.getAttr(shapeName + '.radius'))
	use_local_space = cmds.getAttr(shapeName + '.use_local_space')
	jitter = cmds.getAttr(shapeName + '.jitter')
	spread = cmds.getAttr(shapeName + '.particle_spread')
	num_particles = cmds.getAttr(shapeName + '.num_particles')
	probability = cmds.getAttr(shapeName + '.probability')
	
	coords = get_coordinates(tnode, use_local_space)
	
	jittered_coords = []
	seed(100)
	for n in range(0,len(coords), 3 ):
		probabi = uniform(0, 1)
		if probabi <= probability :
			original_x = coords[n] + uniform(-jitter, jitter)
			original_y = coords[n+1] + uniform(-jitter, jitter)
			original_z = coords[n+2] + uniform(-jitter, jitter)
			x = original_x + uniform(-spread, spread)
			y = original_y + uniform(-spread, spread)
			z = original_z + uniform(-spread, spread)
			jittered_coords.extend([x,y,z])
		
	rounded = []
	# Reduce precision to 3 decimal places - less text to pass.
	for coord in jittered_coords:
		rounded.append(round(coord,3))
		
	coords_str = " ".join(map(str, rounded))
	
	text = rad + ' ' + str(len(coords)) + ' ' + coords_str
	cmds.setAttr(shapeName + '.data', text, type='string')
	
# Rreturns a flat list of coords ie. [x0,y0,z0,x1,y1,z1....]
def get_coordinates(tnode, useLocalSpace=True):
	verts = []
	shape = cmds.listRelatives(tnode, shapes=True)[0]
	#if shapes != None and len(shapes) > 0
	#	shape = shape[0]
	num_verts = cmds.polyEvaluate(tnode, vertex=True)
	for n in range(num_verts):
		vert_str = shape + '.vtx[%d]' % n;
		vert_pos = cmds.pointPosition(vert_str, local=useLocalSpace) 
		verts.extend(vert_pos)	
	return verts
	
