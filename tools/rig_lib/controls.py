"""
controls.py

rig controls functions
"""


import maya.cmds as mc


def make( prefix, ctrlScale = 1.0, ctrlShape= '', matchObject= None, matchObjectTr = None, parentObj= None ):

    """
    make control
    """

    ctrl = None

    if ctrlShape == 'circleY':

        ctrl = circleY( curveScale = ctrlScale )

    if ctrlShape == 'circleX':

        ctrl = circleX( curveScale = ctrlScale )

    # rename control
    ctrl = mc.rename( ctrl, prefix + '_ctl' )

    # colorize control
    rgbColor = [.267,.440,.440]

    if prefix.startswith('L_'):

        rgbColor = [.118,.118,1]

    if prefix.startswith('R_'):

        rgbColor = [1,.157,.157]

    mc.color( ctrl, rgbColor = rgbColor )

    # offset control
    ctrlOffset = mc.group( n= prefix + '_cto', em=True )
    mc.parent( ctrl, ctrlOffset )
    
    # limit control channels
    if prefix != 'global':

        for channel in ['sx', 'sy', 'sz', 'v']:

            mc.setAttr( ctrl + '.' + channel, l = True, k = False )

    # move control to reference
    if matchObject:

        mc.delete( mc.parentConstraint( matchObject, ctrlOffset ) )

    # translate control to reference
    if matchObjectTr:
        
        mc.delete( mc.pointConstraint( matchObjectTr, ctrlOffset ) )

    # parent control
    if parentObj:

        mc.parent( ctrlOffset, parentObj )

    return {
            'c':ctrl,
            'off':ctrlOffset
        }


def circleX( curveScale = 1.0 ):

    crv = mc.circle( normal=[1,0,0], ch=0, radius=curveScale * 0.5 )[0]

    return crv

def circleY( curveScale = 1.0 ):

    crv = mc.circle( normal=[0,1,0], ch=0, radius=curveScale * 0.5 )[0]

    return crv


"""
def shape( curveScale = 1.0 ):
    
    crv = mc.circle(radius=.5, normal=(0, 1, 0), constructionHistory=False)

    clsDf, clsHdl = mc.cluster( crv )
    mc.setAttr( clsHdl + '.s', curveScale, curveScale, curveScale )
    mc.delete( crv, ch=True )

    return crv
"""

def printCvPositions( curveObj ):

    """
    print curve CVs positions for control function
    """

    CVs = mc.ls( curveObj + '.cv[*]', fl = True )
    poslist = []

    print('pos = []')

    for cv in CVs:

        pos = mc.xform( cv, q = True, t = True, ws = True )
        poslist.append( pos )
        print('pos.append( ( %f, %f, %f ) )' % ( pos[0], pos[1], pos[2] ) )

    return poslist


