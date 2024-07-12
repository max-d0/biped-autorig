"""
rig_head.py

head control setup
"""

import maya.cmds as mc

from . import module
from . import controls

def build( 
        neckJoints,
        headJnt = 'headBase2_jnt',
        lEyeJnt = 'L_eye1_jnt',
        rEyeJnt = 'R_eye1_jnt',
        jawJnt = 'jaw1_jnt',
        ikCurve = 'neck_crv',
        eyeAimLoc = 'eyeAim_loc',
        prefix = 'head',
        ctrlScale = 1.0
        ):

    # make module
    moduleObjs = module.make( prefix = prefix )

    baseGrp = mc.group( n = prefix + 'NeckBase_grp', em = True, p = moduleObjs['partsGrp'] )
    headOrientGrp = mc.group( n = prefix + 'HeadOrient_grp', em = True, p = baseGrp )

    # make controls
    
    # head setup
    headCtrl = controls.make( prefix = prefix + 'Main', ctrlScale = ctrlScale * 6.5, ctrlShape = 'head', matchObjectTr = headJnt, parentObj = moduleObjs['controlsGrp'] )

    # headCtrl offset
    headEndJnt = mc.listRelatives( headJnt, c = True, type = 'joint' )[0]
    headCls, headClsHdl = mc.cluster( headCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( headEndJnt, headClsHdl ) )
    translation_amount = [0, -5.5, 0]
    mc.xform( headClsHdl, translation=translation_amount, relative=True )
    mc.delete( headCtrl['c'], ch = True )

    mc.orientConstraint( headOrientGrp, headCtrl['off'], mo = True )
    mc.parentConstraint( baseGrp, headCtrl['off'], mo = True, sr = ['x', 'y', 'z'] )
    mc.orientConstraint( headCtrl['c'], headJnt, mo = True )

    
    # jaw setup
    jawCtrl = controls.make( prefix = prefix + 'Jaw', ctrlScale = ctrlScale * 2, ctrlShape = 'circleY', matchObject = jawJnt, parentObj = headCtrl['c'] )
    
    jawEndJnt = mc.listRelatives( jawJnt, c = True, type = 'joint' )[0]
    jawCls, jawClsHdl = mc.cluster( jawCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( jawEndJnt, jawClsHdl ) )
    mc.move( 0, -ctrlScale * 2, 0, jawClsHdl, r = True )
    mc.delete( jawCtrl['c'], ch = True )
    
    mc.parentConstraint( jawCtrl['c'], jawJnt, mo = True )
    

    # neck setup
    chainIk = mc.ikHandle( n = prefix + 'Neck_ikh', sol = 'ikSplineSolver', sj = neckJoints[0], ee = neckJoints[-1], c = ikCurve, ccv = 0, parentCurve = 0 )[0]

    mc.parent( chainIk, ikCurve, moduleObjs['partsStaticGrp'] )
    
    # neck twist system
    neckTwistOffsetGrp = mc.group( n = prefix + 'NeckTwistOff_grp', em = True, p = moduleObjs['partsGrp'] )
    mc.delete( mc.pointConstraint( neckJoints[0], neckTwistOffsetGrp ) )
    mc.parent( neckTwistOffsetGrp, baseGrp )
    
    mc.aimConstraint( headCtrl['c'], neckTwistOffsetGrp, aim = [1, 0, 0], u = [0, 0, 1], wut = 'objectrotation', wu = [1, 0, 0], wuo = baseGrp )
    
    neckTwistGrp = mc.group( n = prefix + 'NeckTwist_grp', em = True, p = neckTwistOffsetGrp )
    neckTwistOriConstr = mc.parentConstraint( headCtrl['c'], neckTwistGrp, mo = True, st = ['x', 'y', 'z'] )[0]
    mc.setAttr( neckTwistOriConstr + '.interpType', 2 )  # shortest
    
    mc.connectAttr( neckTwistGrp + '.rx', chainIk + '.twist' )

    # neck curve attachment
    mc.cluster( ikCurve + '.cv[0:1]', wn = [baseGrp, baseGrp], bs = True )
    mc.cluster( ikCurve + '.cv[2:3]', wn = [headCtrl['c'], headCtrl['c']], bs = True )
    
    
    # eyes setup
    eyesAimCtrl = controls.make( prefix = prefix + 'EyeAim', ctrlScale = ctrlScale * 2, ctrlShape = 'circleZ', matchObjectTr = eyeAimLoc, parentObj = moduleObjs['controlsGrp'] )
    
    mc.parentConstraint( headCtrl['c'], eyesAimCtrl['off'], mo = True )
    
    middleEyesAimGrp = mc.group( n = prefix + 'MiddleEyesAim_grp', em = True, p = moduleObjs['partsGrp'] )
    mc.delete( mc.pointConstraint( lEyeJnt, rEyeJnt, middleEyesAimGrp ) )
    mc.parentConstraint( headJnt, middleEyesAimGrp, mo = True, sr = ['x', 'y', 'z'] )
    mc.aimConstraint( eyesAimCtrl['c'], middleEyesAimGrp, aim = [1, 0, 0], u = [0, 1, 0], wu = [1, 0, 0], wut = 'objectrotation', wuo = headJnt )
    
    for eyeJnt in [lEyeJnt, rEyeJnt]:
        
        mc.orientConstraint( middleEyesAimGrp, eyeJnt, mo = True )
    

    
    return {
        'moduleObjs':moduleObjs,
        'baseGrp':baseGrp,
        'headOrientGrp':headOrientGrp,
        'headCtrl':headCtrl
        }

