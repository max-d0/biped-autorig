"""
main.py

main rig structure functions
"""

import maya.cmds as mc

from . import controls

def baseGroups(charName = '', rigScale = 1.0, settingsCtrlRefObj = "headTop_jnt", settingsCtrlOffset = 1.0 ):

    """
    build base rig groups
    """

    topGrp = mc.group( n= charName + '_rig_grp', em=True )

    jointsGrp = mc.group( n= 'joints_grp', em=True, p= topGrp )
    modelGrp = mc.group( n= 'model_grp', em=True, p= topGrp )
    controlsGrp = mc.group( n= 'controls_grp', em=True, p= topGrp )

    # lock attributes of top group
    for channel in ['t', 'r', 's']:

        for axis in ['x', 'y', 'z']:

            mc.setAttr( topGrp + '.' + channel + axis, l=True, k=False, cb=False )


    # make global control
    globalCtrl = controls.make( prefix= 'global', ctrlScale = rigScale * 95, ctrlShape= 'circleY', parentObj= topGrp )

    # make settings control
    settingsCtrl = controls.make( prefix= 'settings', ctrlScale = rigScale * 5, ctrlShape= 'circleX', matchObject = settingsCtrlRefObj, parentObj= globalCtrl['c'] )

    mc.move( 0, settingsCtrlOffset * 2, 0, settingsCtrl['off'], r = True )

    # add settings attributes
    groupsVisAtList = ['jointsVis', 'modelVis', 'controlsVis']
    groupsDispTypeAtList = ['jointsDispType', 'modelDispType', 'controlsDispType']
    mainGroups = [jointsGrp, modelGrp, controlsGrp]

    for grp, visAt, dispTypeAt in zip( mainGroups, groupsVisAtList, groupsDispTypeAtList ):

        mc.addAttr( settingsCtrl['c'], ln= visAt, at = 'enum', enumName = 'off:on', k = True, dv = 1 )
        mc.connectAttr( settingsCtrl['c'] + '.' + visAt, grp + '.v' )

        if grp == jointsGrp:

            mc.setAttr( settingsCtrl['c'] + '.' + visAt, 0 )

        if not grp == controlsGrp:

            mc.addAttr( settingsCtrl['c'], ln= dispTypeAt, at = 'enum', enumName = 'normal:template:reference', k = True, dv = 2 )
            mc.setAttr( grp + '.ove', 1 )
            mc.connectAttr( settingsCtrl['c'] + '.' + dispTypeAt, grp + '.ovdt' )

    # attach groups to global control
    for grp in [jointsGrp, controlsGrp]:

        for channel in ['t', 'r', 's']:

            mc.connectAttr( globalCtrl['c'] + '.' + channel, grp + '.' + channel )

    return {
        'topGrp':topGrp,
        'jointsGrp':jointsGrp,
        'modelGrp':modelGrp,
        'controlsGrp':controlsGrp
        }


