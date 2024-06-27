"""
module.py

rig module groups structure
"""

import maya.cmds as mc

def make(
        prefix = 'newmodule'
    ):
    
    mainGrp = mc.group( n = prefix + 'RigModule_grp', em = True )
    controlsGrp = mc.group( n = prefix + 'Controls_grp', em = True, p = mainGrp )
    partsGrp = mc.group( n = prefix + 'Parts_grp', em = True, p = mainGrp )
    partsStaticGrp = mc.group( n = prefix + 'PartsStatic_grp', em = True, p = mainGrp )

    mc.hide( partsGrp, partsStaticGrp )
    mc.setAttr( partsStaticGrp + '.it', 0 )

    return {
        'mainGrp':mainGrp,
        'controlsGrp':controlsGrp,
        'partsGrp':partsGrp,
        'partsStaticGrp':partsStaticGrp
        }
    




