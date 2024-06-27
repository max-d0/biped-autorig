"""
build.py

biped rig
"""

import maya.cmds as mc

from rig_lib import main
from rig_lib import weights
from rig_lib import rig_spine

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
    spineRigGrp = 'spine_rig'

    mc.parent( assetModelGrp, baseGroupsData['modelGrp'] )
    mc.parent( rootJnt, baseGroupsData['jointsGrp'] )
    mc.parent( spineRigGrp, baseGroupsData['jointsGrp'] )

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

    spineData = rig_spine.build(
                    spineJoints = spineJointsList,
                    pelvisJnt = 'C_pelvis_jnt',
                    rootJnt = 'root_jnt',
                    prefix= 'spine',
                    ctrlScale = rigScale * 10
                    )

    mc.parent( spineData['moduleObjs']['mainGrp'], baseGroupsData['controlsGrp'] )

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





