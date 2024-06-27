"""
rig_spine.py

spine control setup
"""

import maya.cmds as mc

from . import module
from . import controls

def build(
        spineJoints,
        pelvisJnt,
        rootJnt,
        prefix= 'spine',
        ctrlScale = 1.0
        ):

    # make module
    moduleObjs = module.make( prefix = prefix )

    # make controls



    """
    bodyCtrl = controls.make( prefix = prefix + 'Body', ctrlScale = ctrlScale * 5, ctrlShape= 'circleY', matchObjectTr = rootJnt, parentObj = moduleObjs['controlsGrp'] )

    pelvisJntEnd = mc.listRelatives( pelvisJnt, c = True, type = 'joint' )[0]
    hipsCtrl = controls.make( prefix = prefix + 'Hips', ctrlScale = ctrlScale * 4, ctrlShape = 'circleY', matchObjectTr = pelvisJnt, parentObj = bodyCtrl['c'] )
    hipsLocalCtrl = controls.make( prefix = prefix + 'HipsLocal', ctrlScale = ctrlScale * 3.5, ctrlShape = 'circleY', matchObjectTr = pelvisJnt, parentObj = hipsCtrl['c'] )
    chestCtrl = controls.make( prefix = prefix + 'Chest', ctrlScale = ctrlScale * 4.5, ctrlShape = 'circleY', matchObjectTr = spineJoints[-2], parentObj = bodyCtrl['c'] )
    chestLocalCtrl = controls.make( prefix = prefix + 'ChestLocal', ctrlScale = ctrlScale * 4, ctrlShape = 'circleY', matchObjectTr = spineJoints[-1], parentObj = chestCtrl['c'] )
    """
    

    # offset hips controls
    


    # attach skeleton
 


    # drive joints



    return{
        'moduleObjs':moduleObjs
        }





