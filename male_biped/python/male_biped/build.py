"""
build.py

biped rig
"""

import maya.cmds as mc

from rig_lib import main
from rig_lib import weights
from rig_lib import rig_spine
from rig_lib import rig_head

projectPath = r'X:\Work\mayascripts\biped_autorig\%s'

modelPath = '%s\model\%s_model.ma'
skeletonPath = '%s\skeleton\%s_skeleton.ma'
weightsPath = '%s\weights/'


def setup( charName= '', rigScale= 1.0 ):

    """
    main rig setup function
    """

    mainProjectPath = projectPath % charName

    # make new scene
    mc.file(new=True, f=True)

    # import model
    modelPathFile = modelPath % (mainProjectPath,charName)
    mc.file( modelPathFile, i=True )

    # fit model to camera
    mc.viewFit()

    # import skeleton
    skeletonPathFile = skeletonPath % (mainProjectPath,charName)
    mc.file( skeletonPathFile, i=True )

    # main rig strcuture
    baseGroupsData = main.baseGroups(charName = charName, rigScale = rigScale, settingsCtrlOffset = rigScale )

    # parent rig objects
    assetModelGrp = '%s_model_grp' % charName
    rootJnt = 'root_jnt'
    spineRigDrivers = 'spine_driver_jnts'

    mc.parent( assetModelGrp, baseGroupsData['modelGrp'] )
    mc.parent( rootJnt, baseGroupsData['jointsGrp'] )
    mc.parent( spineRigDrivers, baseGroupsData['jointsGrp'] )

    """
    # temp binding of model
    mc.cluster( assetModelGrp, wn= [rootJnt, rootJnt], bs=True )
    """

    # build controls setup
    controlsSetup( baseGroupsData, rigScale )

    # load model skin weights
    loadSkinWeights( charName, modelGrp = baseGroupsData['modelGrp'] )

def controlsSetup( baseGroupsData, rigScale ):

    """
    build control setup
    """

    spineJointsList = ['C_spineBase_jnt', 'C_spineA_jnt', 'C_spineB_jnt', 'C_spineC_jnt', 'C_chest_jnt']
    ribbonJointsList = ['C_spineBase_driver_jnt', 'C_spineB_driver_jnt', 'C_spineC_driver_jnt']

    spineData = rig_spine.build(
                    spineJoints = spineJointsList,
                    ribbonJoints = ribbonJointsList,
                    pelvisJnt = 'C_pelvis_jnt',
                    rootJnt = 'root_jnt',
                    prefix= 'spine',
                    ctrlScale = rigScale * 10
                    )

    # parent main module group to controlsGrp
    mc.parent( spineData['moduleObjs']['mainGrp'], baseGroupsData['controlsGrp'] )

    """
    build control setup
    """

    neckJointsList = ['neck1_jnt', 'neck2_jnt', 'neck3_jnt']

    headData = rig_head.build(
        neckJoints = neckJointsList,
        headJnt = 'headBase1_jnt',
        prefix = 'head',
        ctrlScale = 3
    )

    mc.parent( headData['moduleObjs']['mainGrp'], baseGroupsData['controlsGrp'] )

def saveSkinWeights( charName, skinnedObjs ):

    """
    save character skin weights
    """

    projectFolder = projectPath % charName
    weightsFolder = weightsPath % projectFolder

    for geo in skinnedObjs:

        weights.saveSkinWeights( geo, weightsFolder )


def loadSkinWeights( charName, modelGrp ):

    """
    load character skin weights
    """

    modelGeos = [ mc.listRelatives( m, p = True )[0] for m in mc.listRelatives( modelGrp, ad = True, type = 'mesh' ) ]
    modelGeos = list( set( modelGeos ) )  # prevent duplicates
    
    projectFolder = projectPath % charName
    weightsFolder = weightsPath % projectFolder
    
    for geo in modelGeos:

        weights.loadSkinWeights( geo, weightsFolder )





