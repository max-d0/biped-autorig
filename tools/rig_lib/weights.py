"""
weights.py


functions for working with deformer weights
"""

import maya.cmds as mc
import json
import os.path

weightsFileExt = '.xml'
influencesFileExt = '.infs'

def saveSkinWeights( geoObject, weightsFolder ):
    
    """
    save weights of skinned geometry object to given weights folder
    Weights will be saved under the object short name with additional
    file storing its influences
    
    @param geoObject: str, name of skinned geometry object for saving its weights
    @param weightsFolder: str, absolute path to skin weights folder
    @return: str, name of skin weights file
    """
    
    his = mc.listHistory( geoObject )
    scRes = mc.ls( his, type = 'skinCluster' )
    
    if not scRes:
        
        print( '# no skinCluster found on %s, skipping saving skin weights' % geoObject )
        return
    
    geoSkinClusterNode = scRes[0]
    
    weightsFilename = geoObject + weightsFileExt
    mc.deformerWeights ( weightsFilename, path = weightsFolder, export = True, deformer = geoSkinClusterNode )
    
    # save influences file
    influences = mc.skinCluster( geoSkinClusterNode, q = True, inf = True )
    
    influencesFileName = geoObject + influencesFileExt
    influencesPath = os.path.join( weightsFolder, influencesFileName )
    fileobj = open( influencesPath, mode = 'w' )
    json.dump( influences, fileobj, sort_keys = True, indent = 4, separators = ( ',', ': ' ) )
    

def loadSkinWeights( geoObject, weightsFolder ):
    
    """
    load weights of skinned geometry object from given weights folder
    Weights will be loaded from filename matching object short name with additional
    file to get its influences
    
    @param geoObject: str, name of skinned geometry object for saving its weights
    @param weightsFolder: str, absolute path to skin weights folder
    @return: str, name of skin weights file
    """
    
    # define and check files
    weightsFilename = geoObject + weightsFileExt
    weightsFilepath = os.path.join( weightsFolder, weightsFilename )
    
    influencesFileName = geoObject + influencesFileExt
    influencesFilepath = os.path.join( weightsFolder, influencesFileName )
    
    if not os.path.exists( weightsFilepath ):
        
        print( '# weights file not found for %s, skipping loading weights from %s' % ( geoObject, weightsFilepath ) )
        return
    
    if not os.path.exists( influencesFilepath ):
        
        print( '# influences file not found for %s, skipping loading weights from %s' % ( geoObject, influencesFilepath ) )
        return
    
    
    # get influcences
    fileobj = open( influencesFilepath, mode = 'rb' )
    fileobjStr = fileobj.read()
    influences = json.loads( fileobjStr )
    fileobj.close()
    
    # create skinCluster
    sc = mc.skinCluster( geoObject, influences, tsb = True )[0]
    
    # load skin weights
    mc.deformerWeights ( weightsFilename, path = weightsFolder, im = True, deformer = sc )
    
    return weightsFilepath
    
    
    
