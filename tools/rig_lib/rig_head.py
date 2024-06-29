"""
rig_head.py

head control setup
"""

import maya.cmds as mc

from . import module
from . import controls

def build( 
        neckJoints,
        headJnt,
        ikCurve = 'neck_crv',
        prefix = 'head',
        ctrlScale = 1.0
        ):

    # make module
    moduleObjs = module.make( prefix = prefix )

    baseGrp = mc.group( n = prefix + 'NeckBase_grp', em = True, p = moduleObjs['partsGrp'] )

    # make controls

    # head setup
    headCtrl = controls.make( prefix = prefix + 'Main', ctrlScale = ctrlScale * 6.5, ctrlShape = 'circleY', matchObjectTr = headJnt, parentObj = moduleObjs['controlsGrp'] )

    # headCtrl offset
    headEndJnt = mc.listRelatives( headJnt, c = True, type = 'joint' )[0]
    headCls, headClsHdl = mc.cluster( headCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( headEndJnt, headClsHdl ) )
    translation_amount = [0, 9.4, 0]
    mc.xform( headClsHdl, translation=translation_amount, relative=True )
    mc.delete( headCtrl['c'], ch = True )

    mc.orientConstraint( headCtrl['c'], headJnt, mo = True )

    # neck setup

    chainIk = mc.ikHandle( n = prefix + 'Neck_ikh', sol = 'ikSplineSolver', sj = neckJoints[0], ee = neckJoints[-1], c = ikCurve, ccv = 0, parentCurve = 0 )[0]

    mc.parent( chainIk, moduleObjs['partsStaticGrp'] )

    # neck twist system
    neckTwistOffsetGrp = mc.group( n = prefix + 'NeckTwistOff_grp', em = True, p = moduleObjs['partsGrp'] )
    mc.delete( mc.pointConstraint( neckJoints[0], neckTwistOffsetGrp ) )
    mc.parent( neckTwistOffsetGrp, baseGrp )
    
    mc.aimConstraint( headCtrl['c'], neckTwistOffsetGrp, aim = [1, 0, 0], u = [0, 0, 1], wut = 'objectrotation', wu = [1, 0, 0], wuo = baseGrp )
    
    neckTwistGrp = mc.group( n = prefix + 'NeckTwist_grp', em = True, p = neckTwistOffsetGrp )
    neckTwistOriConstr = mc.parentConstraint( headCtrl['c'], neckTwistGrp, mo = True, st = ['x', 'y', 'z'] )[0]
    mc.setAttr( neckTwistOriConstr + '.interpType', 2 )  # shortest
    
    mc.connectAttr( neckTwistGrp + '.rx', chainIk + '.twist' )


    return {
        'moduleObjs':moduleObjs
        }
