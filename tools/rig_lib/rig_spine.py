"""
rig_spine.py

spine control setup
"""

import maya.cmds as mc

from . import module
from . import controls

def build(
        spineJoints,
        ribbonJoints,
        pelvisJnt,
        rootJnt,
        prefix= 'spine',
        ctrlScale = 1.0
        ):

    # make module
    moduleObjs = module.make( prefix = prefix )

    # make controls

    bodyCtrl = controls.make( prefix = prefix + 'Body', ctrlScale = ctrlScale * 5, ctrlShape= 'torso', matchObjectTr = spineJoints[-3], parentObj = moduleObjs['controlsGrp'] )
    
    # bodyCtrl offset
    bodyCls, bodyClsHdl = mc.cluster( bodyCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( spineJoints[-3], bodyClsHdl ) )
    translation_amount = [0, -3.35, 3.2]
    mc.xform( bodyClsHdl, translation=translation_amount, relative=True )
    mc.delete( bodyCtrl['c'], ch = True )

    pelvisJntEnd = mc.listRelatives( pelvisJnt, c = True, type = 'joint' )[0]
    hipsCtrl = controls.make( prefix = prefix + 'Hips', ctrlScale = ctrlScale * 3.75, ctrlShape = 'hips', matchObjectTr = pelvisJnt, parentObj = bodyCtrl['c'] )
    
    # hipsCtrl offset
    hipsCls, hipsClsHdl = mc.cluster( hipsCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( pelvisJnt, hipsClsHdl ) )
    translation_amount = [0, -2, 0]
    mc.xform( hipsClsHdl, translation=translation_amount, relative=True )
    mc.delete( hipsCtrl['c'], ch = True )

    spineBaseCtrl = controls.make( prefix = prefix + 'SpineBase', ctrlScale = ctrlScale * 3.5, ctrlShape = 'hips', matchObjectTr = spineJoints[-5], parentObj = bodyCtrl['c'] )
    
    # spineBaseCtrl offset
    spineBaseCls, spineBaseClsHdl = mc.cluster( spineBaseCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( spineJoints[-5], spineJoints[-4], spineBaseClsHdl ) )
    mc.delete( spineBaseCtrl['c'], ch = True )

    spineBaseLocalCtrl = controls.make( prefix = prefix + 'SpineBaseLocal', ctrlScale = ctrlScale * 3.25, ctrlShape = 'hips', matchObjectTr = spineJoints[-5], parentObj = spineBaseCtrl['c'] )
    
    # spineBaseLocalCtrl offset
    spineBaseLocalCls, spineBaseLocalClsHdl = mc.cluster( spineBaseLocalCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( spineJoints[-5], spineJoints[-4], spineBaseLocalClsHdl ) )
    translation_amount = [0, 2, 0]
    mc.xform( spineBaseLocalClsHdl, translation=translation_amount, relative=True )
    mc.delete( spineBaseLocalCtrl['c'], ch = True )

    spineBCtrl = controls.make( prefix = prefix + 'SpineB', ctrlScale = ctrlScale * 3.3, ctrlShape = 'torso', matchObjectTr = spineJoints[-3], parentObj = spineBaseCtrl['c'] )
    
    # spineBCtrl offset
    spineBCls, spineBClsHdl = mc.cluster( spineBCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( spineJoints[-3], spineBClsHdl ) )
    translation_amount = [0, 0, 1.28]
    mc.xform( spineBClsHdl, translation=translation_amount, relative=True )
    mc.delete( spineBCtrl['c'], ch = True )

    spineBLocalCtrl = controls.make( prefix = prefix + 'SpineBLocal', ctrlScale = ctrlScale * 3.15, ctrlShape = 'torso', matchObjectTr = spineJoints[-3], parentObj = spineBCtrl['c'] )
    
    # spineBLocalCtrl offset
    spineBLocalCls, spineBLocalClsHdl = mc.cluster( spineBLocalCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( spineJoints[-3], spineBLocalClsHdl ) )
    translation_amount = [0, 2, 1]
    mc.xform( spineBLocalClsHdl, translation=translation_amount, relative=True )
    mc.delete( spineBLocalCtrl['c'], ch = True )

    ribCtrl = controls.make( prefix = prefix + 'Chest', ctrlScale = ctrlScale * 3.6, ctrlShape = 'torso', matchObjectTr = spineJoints[-2], parentObj = spineBCtrl['c'] )
    
    # ribCtrl offset
    ribCls, ribClsHdl = mc.cluster( ribCtrl['c'], n = 'tempShapeOffset_cls' )
    mc.delete( mc.pointConstraint( spineJoints[-2], ribClsHdl ) )
    translation_amount = [0, 0, 2.8]
    mc.xform( ribClsHdl, translation=translation_amount, relative=True )
    mc.delete( ribCtrl['c'], ch = True )

    # attach skeleton
    mc.parentConstraint( bodyCtrl['c'], rootJnt, mo = True )

    mc.parentConstraint( hipsCtrl['c'], pelvisJnt, mo = True )

    mc.parentConstraint( spineBaseCtrl['c'], ribbonJoints[-3], mo = True )
    mc.parentConstraint( spineBaseLocalCtrl['c'], spineJoints[-5], mo = True )

    mc.parentConstraint( spineBCtrl['c'], ribbonJoints[-2], mo = True )
    mc.parentConstraint( spineBLocalCtrl['c'], spineJoints[-3], mo = True )

    mc.parentConstraint( ribCtrl['c'], ribbonJoints[-1], mo = True )


    return{
        'moduleObjs':moduleObjs,
        'bodyCtrl':bodyCtrl
        }





