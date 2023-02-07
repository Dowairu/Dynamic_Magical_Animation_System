''' David Magical Animation System:

    This program is designed to create procedural animations using different simple algorithms.
    it takes an object or group of objects as input and applies a selected animation onto them. 
    The animations can also be stacked so that a user can perform multiuple actions on one or multiple objects'''

__author__ =  'David Owairu'
__version__=  '1.4.0'

'''deletes all the globals in mayas memory.'''
for name in dir():
    if not name.startswith('_'):
        try:
            del globals()[name]
        except:
            pass

import maya.cmds as mc
from collections import OrderedDict
import random as rd
from maya.OpenMaya import MVector
'''variables in lowerCamelCase'''
'''funtions in CamelCase'''


objCoordDict = OrderedDict()
submission_Path='\\home\\xyang\\maya_scripts\\submission'
filePath = 'David_Owairu_Scripting\\src\\'

def CreateShader(shaderType,shaderName,object,number):
    '''this functions creates a shader of specified type:
    
       - shaderType: the type of shader we are creating eg:Lambert,standard surface etc.
       - shaderName: the name of the shader.
       - object:     object the shader is being applied to.
       - number:     the shader number at the end of its name to avoid clashing 
                    with existing shaders of the same type.
        
        Return Value:
       - returns the name of the shader'''

    mc.shadingNode(shaderType,asShader=True,n=shaderName+ str(number))
    mc.sets(r=True,nss=True,em=True,n=shaderName + str(number) +'SG')
    mc.connectAttr(shaderName+str(number)+'.outColor',shaderName+str(number)+'SG.surfaceShader',f=True)
    mc.select(object)
    mc.sets(forceElement=shaderName+str(number)+'SG')
    return shaderName+str(number)

def GetObjPos(objName):
    '''Gets the position of an object and returns it as a list:
    
       - objName: the object we are getting the pos of.
        
        Return Value:
       - objScale:      List of object xyz pos'''

    xpos = mc.getAttr(objName + '.translateX')
    ypos = mc.getAttr(objName + '.translateY')
    zpos = mc.getAttr(objName + '.translateZ')
    objPos = [xpos,ypos,zpos]
    return objPos

def GetObjSize(objName):
    '''Gets the size of an object and returns it as a list:
    
       - objName: the object we are getting the size of.
       
       Return Value:
       - objScale:      List of object xyz scales'''

    mc.currentTime(query=True,update=True)
    sx = mc.getAttr(objName + '.scaleX')
    sy = mc.getAttr(objName + '.scaleY')
    sz = mc.getAttr(objName + '.scaleZ')
    objScale = [sx,sy,sz]
    return objScale

def SetProjectKey(shader,startFrame,endFrame):
    '''Sets the transmission attributte for a shader
       from 0 to 1 or 1 to 0 for a specific time frame:

       - shader:       shader we are changing the transmission on. 
       - startFrame:   first keyframe of the transmission.
       - endFrame:     last keyframe of the transmision.'''

    mc.setKeyframe(shader, attribute="it", v=0, t=startFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(shader, attribute="it", v=1, t=endFrame, inTangentType="spline", outTangentType="spline")

def SetVisibleKey(object,startFrame,endFrame):
    '''Sets the visibility attributte for an object.
       from 0 to 1 or 1 to 0 for a specific time frame.

       - object:       object we are changing the visibility on. 
       - startFrame:   first keyframe of the visibilty.
       - endFrame:     last keyframe of the visibilty.'''   

    mc.setKeyframe(object, attribute="v", v=0, t=startFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(object, attribute="v", v=1, t=endFrame, inTangentType="spline", outTangentType="spline")
    
def SetScaleKey(object,startFrame,endFrame,scalefactor):
    '''Sets the scale attributte for an object for a specific time frame.

        - object:       object being scaled. 
        - startFrame:   first keyframe of the scaling..
        - endFrame:     last keyframe of the scaling..
        - scalefactor:  number original object is multiplied by.''' 

    scale = GetObjSize(object)
    mc.setKeyframe(object, attribute="sx", v=scale[0], t=startFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(object, attribute="sy", v=scale[1], t=startFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(object, attribute="sz", v=scale[2], t=startFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(object, attribute="sx", v=scale[0]*scalefactor, t=endFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(object, attribute="sy", v=scale[1]*scalefactor, t=endFrame, inTangentType="spline", outTangentType="spline")
    mc.setKeyframe(object, attribute="sz", v=scale[2]*scalefactor, t=endFrame, inTangentType="spline", outTangentType="spline")

def ClearScene():
    '''Clears everything in the scene for a fresh scene.'''
    mc.select(all=True)
    mc.delete()

def SnapToPos(wand,object,*args):
    '''Snaps an objects local x axis to the position and angle of another object.
        
       - wand: object that we are snapping/rotating.
       - object: object we are snapping to. '''

    shapeNode=mc.listRelatives(object)
    type = mc.objectType(shapeNode[0])
    pointer = MVector(*GetObjPos(wand))
    if type == 'nurbsCurve' and args:
        point = MVector(*mc.pointPosition(object+'.cv['+str(args[0])+']'))
    else:
        point = MVector(*GetObjPos(object))
    dVector = point - pointer
    angle = mc.angleBetween(euler=True, v1=(1,0,0),v2=(dVector.x,dVector.y,dVector.z))
    mc.rotate(0,angle[1],angle[2],wand)

def frameCalc(stf,enf):
    '''calculates the total number of frames for an animation.
       
       - stf: starting frame.
       - enf: ending frame.
       
       Return Values:
       nFrames:     The total number of frames between stf and enf'''

    if stf == 1:
        nFrames=enf
    else:
        nFrames=enf-stf
    return nFrames

def CreateMotionPath(object,startFrame,endFrame,precision):
    '''Generates a motionpath for animated objects.
       The paths generated will be used to control the movement of the wand
       if the user decides to use a wand:
        
        - object:       object we are getting the motion path from
        - startFrame:   start frame of objects existing animation
        - endFrame:     end frame of objects existing animation
        - precision:    how precise the curve should be to the animation'''

    curPos = GetObjPos(object)
    mc.curve(n=object + 'motionPath',p=[(curPos[0],curPos[1],curPos[2])])
    for i in range(startFrame,endFrame,int(precision)):
        mc.currentTime(i)
        curPos = GetObjPos(object)
        mc.curve(object + 'motionPath',a=True,p=[(curPos[0],curPos[1],curPos[2])])

def GetObjCoordArray(flag):
    '''this funtion fills up a global dictionary that is used to animate the floating cleanup function.

       - flag:  Used to determine what values to save into the dictionary can either be 'source' or 'destination' 
    '''
    mc.select(hierarchy=True)
    length = mc.ls(selection=True, type="mesh",sn=True)
    for i in range(len(length)):
        objName = mc.listRelatives(length[i], parent=True)
        position = GetObjPos(objName[0])
        objCoordDict.setdefault(objName[0],[0,0])
        if flag =='source':
            objCoordDict[objName[0]][0]=position
        elif flag =='destination':
            objCoordDict[objName[0]][1]=position
            
def ParticleEmitter(numOfParticles,grav,object,color1,color2):
    """funtion that creates creates creates and initialises and emiiter.

       - numOfParticles: number of particles for the system to generate persecond.
       - grav:           gravity of the nucleus affecting the particles.
       - object:         the object being used as an emiiter. if this argument is false and emitter is created and returned.
       
       Return Values:
       - particles:      List od nparticles nodes
       - emitSphere:     List of sphere node"""
    
    if object:
        for obj in range(len(object)):
            particleName=object[obj[0]] + 'nparticle'
            emitterName = object[obj[0]] + 'emmiter'
            if mc.objExists(particleName) and mc.objExists(emitterName):
                break
            mc.select(object[obj])
            mc.emitter(type='surface', name=emitterName,r=numOfParticles,spd=0.5,srn=0.25,nsp=1,dx=1,vsh='sphere',mxd=0.3,mnd=0.1, vof= (0,0,0),vsw=360,tsr=0.5,afc=0.8,afx=1)
            particles = mc.nParticle(name=particleName)
            mc.connectDynamic(particleName,em=emitterName)
            CreateGradient(particleName,color1,color2)
            mc.setAttr('nucleus1.gravity',grav)
            mc.setAttr(particleName + '.lifespanMode',2)
            mc.setAttr(particleName + '.lifespan',2)
            mc.setAttr(particleName + '.lifespanRandom',1)
            return particles
    
    else:
        emitSphere = mc.polySphere(n='blastEmitter',r=0.125,sx=20,sy=20,ax=(0,1,0))
        particleName=emitSphere[0]+'nparticle'
        emitterName =emitSphere[0]+'emmiter'
        if mc.objExists(particleName) and mc.objExists(emitterName):
            particleName=emitSphere[0]+'nparticle#'
            emitterName =emitSphere[0]+'emmiter#'
        mc.select(emitSphere)
        mc.emitter(type='volume', name=emitterName,r=numOfParticles,spd=0.2,srn=0.25,nsp=1,dx=1,vsh='sphere',mxd=0.3,mnd=0.1, vof= (0,0,0),vsw=360,tsr=0.5,afc=0.8,afx=1)
        particles = mc.nParticle(name=particleName)
        mc.connectDynamic(particleName,em=emitterName)
        CreateGradient(particleName,color1,color2)
        mc.setAttr('nucleus1.gravity',grav)
        mc.setAttr(particleName + '.lifespanMode',2)
        mc.setAttr(particleName + '.lifespan',2)
        mc.setAttr(particleName + '.lifespanRandom',1)
        return emitSphere,particles

def CreateGradient(particleName,color1,color2):
    '''Creates a gradient using two colors and applies it to a particle system
       
       particleName:    Particle system were changing the color of
       color1:          first color of the gradient
       color2:          Second color of the gradient
    '''
    mc.setAttr(particleName +'.colorInput',6)
    colList=[color1,color2]
    for i in range(len(colList)):
        mc.setAttr(particleName + '.color'+'['+str(i)+']'+'.color_Color',colList[i][0],colList[i][1],colList[i][2],type='double3')
        mc.setAttr(particleName + '.color'+'['+str(i)+']'+'.color_Position',i)
        mc.setAttr(particleName + '.color'+'['+str(i)+']'+'.color_Interp',1)

def BlastAnimation(wandCtrl,wand,object,wandstFrame,stBeamFrame,endBeamFrame,color1,color2,numParticles,grav):
    ''' extension to the wand function. It animates a blast between the wand and the object being affected:
        
        - wandCtrl:     rig control for the wand.    
        - wand:         wand the balst is coming from.
        - object:       object the being blasted.
        - wandstFrame:      start frame of the wand animation.
        - startBeamFrame:   start frame of blast animation.
        - endBeamFrame:     end freame of blast animation.
        - color1:        first color of the gradient
        - color2:        Second color of the gradient
        - numParticles:  number of particles for the system to generate persecond
        - grav:          gravity of the nucleus affecting the particles.
    '''
    shapeNode=mc.listRelatives(object)
    wandName = mc.listRelatives(wandCtrl,parent=True)
    type = mc.objectType(shapeNode[0])
    
    if type == 'nurbsCurve':
        mc.duplicate(object,n=object + 'BlastPath',st=True,rc=True)
        blastObj = ParticleEmitter(100,1,False,color1,color2)
        mc.select(blastObj[0][0],object+'BlastPath')
        mc.pathAnimation(fractionMode=True,follow=True,followAxis='z',upAxis='y',worldUpType="vector",worldUpVector= (0,1,0),inverseUp=False,inverseFront=False,bank=False,startTimeU=wandstFrame,endTimeU=endBeamFrame)
        mc.group(('BlastPath',blastObj[0][0],blastObj[1][0],'nucleus1'),n=object+'_BlastGrp')
    
    else:
        SnapToPos(wandCtrl,object)
        #could have made an algorithm to find these points for more universality.
        if (wandName[0] == 'Wizard_Wand') or (wandName[0] =='Sorcerer_Wand'):
            wandpos= mc.pointPosition(wand+'.vtx[17]')
        elif wandName[0] == 'Magician_Wand':
            wandpos= mc.pointPosition(wand+'.vtx[65]')
        elif wandName[0] == 'Witch_Wand':
            wandpos= mc.pointPosition(wand+'.vtx[49]')

        objectpos=GetObjPos(object)
        mc.curve(n='BlastPath',degree=1,p=[(wandpos[0],wandpos[1],wandpos[2])])
        mc.curve('BlastPath',a=True,p=[(objectpos[0],objectpos[1],objectpos[2])])
        blastObj = ParticleEmitter(numParticles,grav,False,color1,color2)
        mc.select(blastObj[0][0],'BlastPath')
        mc.pathAnimation(fractionMode=True,follow=True,followAxis='z',upAxis='y',worldUpType="vector",worldUpVector= (0,1,0),inverseUp=False,inverseFront=False,bank=False,startTimeU=stBeamFrame,endTimeU=endBeamFrame)
        SetVisibleKey(blastObj[1][0],wandstFrame,stBeamFrame)
        SetVisibleKey(blastObj[1][0],endBeamFrame,stBeamFrame)
        SetVisibleKey(blastObj[0][0],wandstFrame,stBeamFrame)
        SetVisibleKey(blastObj[0][0],endBeamFrame,stBeamFrame)
        mc.group(('BlastPath',blastObj[0][0],blastObj[1][0],'nucleus1'),n=object+'_BlastGrp')


def ImportWand(wand):
    '''This function imports a wand selected by the user. Importing a wand also lets users create wand animations:
    
        - wand: name/type of wand being imported.'''

    mc.file(submission_Path + filePath + wand + '.ma',i=True)
    
def AnimateWand(wandCtrl,wand,curveName,startFrame,endFrame,precision,color1,color2,numParticles,grav,*args):
    '''Animates the wand to the movement of a curve:
       
       - wand:          wand we are animating.
       - curveName:     the curve being used for animtion.
       - startFrame:    start frame of animation.
       - endFrame:      end frame of animation.
       - precision:     the level of detail that the wand follows the curve.
       - color1:        first color of the gradient
       - color2:        Second color of the gradient
       - numParticles:  number of particles for the system to generate persecond
       - grav:          gravity of the nucleus affecting the particles.
       - args:          extra arguments'''


    numOfFrames = frameCalc(startFrame,endFrame)
    spans = numOfFrames/precision
    mc.rebuildCurve(curveName,rpo=True,s=spans,d=1)

    if startFrame == 1:
        frameOffset = 0
    else:
        frameOffset = startFrame
    
    if args[1]==True:
        shapeNode=mc.listRelatives(args[0][0])
        type = mc.objectType(shapeNode[0])
        
        if type == 'nurbsCurve':
            BlastAnimation(wandCtrl,wand,args[0][0],startFrame,startFrame,endFrame,color1,color2,numParticles,grav)
            
            for i in range (spans):
                frame = mc.currentTime((i+1)*precision)
                SnapToPos(wandCtrl,curveName,i)
                mc.setKeyframe(wandCtrl, attribute="ry", t=frameOffset + frame, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(wandCtrl, attribute="rz", t=frameOffset + frame, inTangentType="spline", outTangentType="spline")
        else:
            spans +=2
            if len(args[0]) > 1:
                wandpos=[0,0,0]
                for obj in range(len(args[0])):
                    pos = GetObjPos(args[0][obj])
                    wandpos[0]+=pos[0]
                    wandpos[1]+=pos[1]
                    wandpos[2]+=pos[2]
                newWandpos=[wandpos[0]/len(args[0]),wandpos[1]/len(args[0]),wandpos[2]/len(args[0])]
                grpSphere = mc.polySphere(n='grpPosSphere',r=0.065,sx=5,sy=5,ax=(0,1,0))
                mc.move(newWandpos[0],newWandpos[1],newWandpos[2],grpSphere[0])
                SnapToPos(wandCtrl,grpSphere[0])
                mc.curve(curveName,a=True,p=[(newWandpos[0],newWandpos[1],newWandpos[2])])
            else:
                SnapToPos(wandCtrl,args[0][0])
                wandpos= GetObjPos(args[0][0])
                mc.curve(curveName,a=True,p=[(wandpos[0],wandpos[1],wandpos[2])])

            for i in range (spans):
                frame = mc.currentTime((i+1)*precision)
                SnapToPos(wandCtrl,curveName,i)
                mc.setKeyframe(wandCtrl, attribute="ry", t=frameOffset + frame, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(wandCtrl, attribute="rz", t=frameOffset + frame, inTangentType="spline", outTangentType="spline")
            
            if len(args[0]) > 1:
                BlastAnimation(wandCtrl,wand,grpSphere[0],startFrame,frame,args[2],color1,color2,numParticles,grav)
            else:
                BlastAnimation(wandCtrl,wand,args[0][0],startFrame,frame,args[2],color1,color2,numParticles,grav)

    else:
        for i in range (spans):
            frame = mc.currentTime((i+1)*precision)
            SnapToPos(wandCtrl,curveName,i)
            mc.setKeyframe(wandCtrl, attribute="ry", t=frameOffset + frame, inTangentType="spline", outTangentType="spline")
            mc.setKeyframe(wandCtrl, attribute="rz", t=frameOffset + frame, inTangentType="spline", outTangentType="spline")
        
def GetParentNode(selectedObject):
    '''Gets the parent Node for every object in the list
       - selectedObject:  List of objects 
       
       Return Values:
       - object:    list of Parent nodes'''

    object = []
    if len(selectedObject) == 1:
        parentNode = mc.listRelatives(selectedObject[0], parent=True)
        object.append(parentNode[0])
        return object
    
    else:
        for i in range(len(selectedObject)):
            parentNode = mc.listRelatives(selectedObject[i], parent=True)
            object.append(parentNode[0])
        return object

def ShrinkGrow(object,startFrame,endFrame,scaleFactor,projectionSize,spacing,random,offset1,offset2):
    '''shrinks or grows the size of an object:

       - object:            object being shrunk/grown.
       - scalefactor:       number original object is multiplied by.
       - projectionSize:    size of the projection effect.
       - spacing:           number of frames between each keyframe          
       - random:            random flag to determine wether to use random offsets
       - offset1:           lower range of random offset, but also main offset if random i not chosen
        -offset2:           upper range of random offset'''
    
    totalFrames = frameCalc(startFrame,endFrame)
    projections= totalFrames/spacing

    frameOffset=offset1
    for obj in range(len(object)):
        projectionGrp=[]
        if random==True:
            frameOffset = rd.randint(offset1,offset2)
        if obj > 0:
            startFrame+=frameOffset
            endFrame+=frameOffset
        SetScaleKey(object[obj],startFrame,endFrame,scaleFactor)
    
        for i in range(int(projections)):
    
            frame = mc.currentTime(startFrame+(spacing*i))
            dupe = object[obj] + 'projection'+str(i+1)
            mc.duplicate(object[obj],n=dupe,st=True,rc=True)
            shader = CreateShader('lambert','projshader',dupe,i+1)
            SetScaleKey(dupe,frame,frame+spacing,projectionSize)
            SetProjectKey(shader,frame,frame+spacing)
            SetVisibleKey(dupe,startFrame,frame)
            projectionGrp.append(dupe)
        mc.group(projectionGrp, n="projectionGrp",parent=object[obj])

def levitation(object,startFrame,endFrame,floatPercentage,height,spacing,float,random,offset1,offset2):
    '''animates an object levitating:
       
       - object:            object being levitated.
       - startFrame:        start frame of levitation.
       - endFrame:          start frame of levitation.
       - floatPercentage:   percentage of frames to be used for floating.
       - height:            height the object will levitate to.
       - spacing:           number of frames between each keyframe.
       - float:             flag that determines wether the object 
                            will float in place at the desired height.
       - random:            random flag to determine wether to use random offsets
       - offset1:           lower range of random offset, but also main offset if random i not chosen
        -offset2:           upper range of random offset'''

    numOfFrames = frameCalc(startFrame,endFrame)    
    if float ==True:
        floatPercentage=50.0
        floatInPlaceFrames= ((floatPercentage/100.0)*numOfFrames)/spacing
        levitateFrames = (numOfFrames/spacing)-floatInPlaceFrames
        totalFrames=levitateFrames+floatInPlaceFrames

    else:
        levitateFrames = numOfFrames/spacing
        totalFrames=levitateFrames

    frameOffset=0
    for obj in range(len(object)):
        if random==True:
            frameOffset = rd.randint(offset1,offset2)
        if obj > 0:
            startFrame+=frameOffset
        for i in range (0,int(totalFrames+1)):
            frame = startFrame+(spacing*i)
            if i <= levitateFrames:
            #floating upwards with side to side movement.'''
                position = GetObjPos(object[obj])
                posx = position[0] + rd.random()
                posy = position[1] + (height/levitateFrames)*i
                posz = position[2] + rd.random()
                if (i > 0) and (startFrame ==1):
                    mc.setKeyframe(object[obj], attribute="tx", v=posx, t=frame-1, inTangentType="spline", outTangentType="spline")
                    mc.setKeyframe(object[obj], attribute="ty", v=posy, t=frame-1, inTangentType="spline", outTangentType="spline")
                    mc.setKeyframe(object[obj], attribute="tz", v=posz, t=frame-1, inTangentType="spline", outTangentType="spline")
                else:
                    mc.setKeyframe(object[obj], attribute="tx", v=posx, t=frame, inTangentType="spline", outTangentType="spline")
                    mc.setKeyframe(object[obj], attribute="ty", v=posy, t=frame, inTangentType="spline", outTangentType="spline")
                    mc.setKeyframe(object[obj], attribute="tz", v=posz, t=frame, inTangentType="spline", outTangentType="spline")

            else:
            #random static floating.
                position = GetObjPos(object[obj])
                posx = position[0] + rd.random()%2
                posz = position[2] + rd.random()%2
                mc.setKeyframe(object[obj], attribute="tx", v=posx, t=frame, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(object[obj], attribute="tz", v=posz, t=frame, inTangentType="spline", outTangentType="spline")
        frameOffset=offset1

def CleanUp(startFrame,endFrame,spacing,random,offset1,offset2):
    '''Creates an animation for objects poasitions. it takes the initial position of objects
        once the user has moved the objects it animates the objects floating from one point to another
    
        - startFrame:        start frame of levitation.
        - endFrame:          start frame of levitation.
        - spacing:           number of frames between each keyframe.          
        - random:            random flag to determine wether to use random offsets
        - offset1:           lower range of random offset, but also main offset if random i not chosen
        - offset2:           upper range of random offset'''

    totalFrames = frameCalc(startFrame,endFrame)
    frames = totalFrames/spacing
    objArray = list(objCoordDict.keys())
    coordArray = list(objCoordDict.values())
    sourceIndex = 0
    destIndex = 1
    
    frameOffset=0
    for obj in range(len(objArray)):
        if random==True:
            frameOffset = rd.randint(offset1,offset2)
        if obj > 0:
            startFrame+=frameOffset
        for i in range(0,int(frames+1)):
            frame = startFrame+(spacing*i)
            rd.seed(i)
            #interpolation from end position to start position
            posx = ((coordArray[obj][destIndex][0] - coordArray[obj][sourceIndex][0])/frames)*i + coordArray[obj][sourceIndex][0] + rd.random()%50
            posy = ((coordArray[obj][destIndex][1] - coordArray[obj][sourceIndex][1])/frames)*i + coordArray[obj][sourceIndex][1] + rd.random()%10
            posz = ((coordArray[obj][destIndex][2] - coordArray[obj][sourceIndex][2])/frames)*i + coordArray[obj][sourceIndex][2] + rd.random()%7
            if (i > 0) and (startFrame ==1):
                mc.setKeyframe(objArray[obj], attribute="tx", v=posx, t=frame-1, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(objArray[obj], attribute="ty", v=posy, t=frame-1, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(objArray[obj], attribute="tz", v=posz, t=frame-1, inTangentType="spline", outTangentType="spline")
            else:
                mc.setKeyframe(objArray[obj], attribute="tx", v=posx, t=frame, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(objArray[obj], attribute="ty", v=posy, t=frame, inTangentType="spline", outTangentType="spline")
                mc.setKeyframe(objArray[obj], attribute="tz", v=posz, t=frame, inTangentType="spline", outTangentType="spline")
        frameOffset =offset1


def AnimManager(wandPrecision,curveName,wandStartFrame,wandEndFrame,wandCtrl,wand,beamEndFrame,animateWand,animateBeam,
                numOfParticlesControl,gravityControl,color1,color2,objParticles,
                random,animOffset1,animOffset2,
                startFrame1,endFrame1,scaleFactor,projectionSize,spacing1,animated1,
                startFrame2,endFrame2,floatPercentage,height,spacing2,float,animated2,
                startFrame3,endFrame3,spacing3,animated3,*pArgs):

    '''This funtion is resposible for collecting all the values from the UI
       and running all the other funtions in the correct order and with the 
       necesary variables:
       
       - wandPrecision:             the level of detail that the wand follows the curve.                
       - curveName:                 the curve being used for wand animtion.
       - wandStartFrame:            start frame of animation.
       - wandEndFrame:              end frame of animation.
       - wandCtrl:                  rig control for the wand.
       - wand:                      wand we are animating.
       - beamEndFrame:              end frame of Beam animation.
       - animateWand:               Flag for wether Wand will be animated.
       - animateBeam:               Flag for wether Beam will be animated.
       - numOfParticlesControl:     number of particles for the system to generate persecond.
       - gravityControl:            gravity of the nucleus affecting the particles.
       - color1:                    first color of the gradient.
       - color2:                    Second color of the gradient.
       - objParticles:              Flag for wether particles will be used or not on objects.
       - random:                    Flag for wether random offset will be used or not.
       - animOffset1:               lower range of random offset, but also main offset if random i not chosen.
       - animOffset2:               upper range of random offset.
       - startFrame1:               start frame of ShrinkGrow.
       - endFrame1:                 end frame of ShrinkGrow.
       - scaleFactor:               number original object is multiplied by  .             
       - projectionSize:            size of the projection effect.
       - spacing1:                  number of frames between each keyframe.
       - animated1:                 Flag for wether ShrinkGrow will be animated.
       - startFrame2:               start frame of levitation.
       - endFrame2:                 end frame of levitation.
       - floatPercentage:           percentage of frames to be used for floating.
       - height:                    height the object will levitate to.         
       - spacing2:                  number of frames between each keyframe.
       - float:                     Flag for wether Levitation will be add a float at the top.
       - animated2:                 Flag for wether Levitation will be animated.
       - startFrame3:               start frame of CleanUp.
       - endFrame3:                 end frame of CleanUp.         
       - spacing3:                  number of frames between each keyframe.
       - animated3:                 Flag for wether CleanUp will be animated.
       '''
    
    mc.select(hierarchy=True)
    selectedObject = mc.ls(selection=True, type=["mesh",'nurbsCurve'])
    object = GetParentNode(selectedObject)

    if objParticles == True:
        ParticleEmitter(numOfParticlesControl,gravityControl,object,color1,color2)

    if animateWand ==True:
        mc.cutKey( object, time=(), at=["rx","ry","rz","tx","ty","tz","sx","sy","sz",'visibility'], option="keys" )
        AnimateWand(wandCtrl,wand,curveName,wandStartFrame,wandEndFrame,wandPrecision,color1,color2,numOfParticlesControl,gravityControl,object,animateBeam,beamEndFrame)
    
    if animated1 == True:
        mc.cutKey( object, time=(), at=["rx","ry","rz","tx","ty","tz","sx","sy","sz",'visibility'], option="keys" )
        ShrinkGrow(object,startFrame1,endFrame1,scaleFactor,projectionSize,spacing1,random,animOffset1,animOffset2)
        
    if animated2 == True:
        mc.cutKey( object, time=(), at=["rx","ry","rz","tx","ty","tz","sx","sy","sz",'visibility'], option="keys" )
        if float == True:
            levitation(object,startFrame2,endFrame2,floatPercentage,height,spacing2,True,random,animOffset1,animOffset2)
        else:
            levitation(object,startFrame2,endFrame2,floatPercentage,height,spacing2,False,random,animOffset1,animOffset2)
       
    if animated3 == True:
        mc.cutKey( object, time=(), at=["rx","ry","rz","tx","ty","tz","sx","sy","sz",'visibility'], option="keys" )
        CleanUp(startFrame3,endFrame3,spacing3,random,animOffset1,animOffset2) 

def CancelProc(win,*args):
    '''Closes the window when 'Quit' button is pressed

       win: The window we are closing'''

    print('Action cancelled')
    mc.deleteUI(win)

def CreateUI(): 
    '''Creates The UI for the program.'''
    winw =400
    winh =800
    winID = "DMAS"
    image = 'dmas.jpg'
    padding = 5
   
    if (mc.window(winID,exists= True)):
        mc.deleteUI(winID)
    
    win = mc.window(winID,title=winID,widthHeight=(winw,winh),sizeable=False,rtf=True)
    mc.columnLayout('Main Layout',adj=True,rs=5,cat=['both',padding])
    mc.image(i=submission_Path + filePath + image,w=winw,h=100 )
    
    mc.frameLayout( label='Wand settings',cll=True,cl=False)
    wandPrecision = mc.intSliderGrp(label='Wand Precision',minValue=1, maxValue=5, value=1,field=True)
    mc.rowColumnLayout('wand frames section',nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    wandStartFrame = mc.intFieldGrp(nf=1,label=" Wand Start Frame",value1=1,adj=1,cat=[1,'right',padding])
    wandEndFrame = mc.intFieldGrp(nf=1,label="Wand end Frame",value1=30,adj=1,cat=[1,'left',padding])
    mc.setParent('..')
    mc.rowColumnLayout('wand Names',nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    wandCtrl =mc.textFieldGrp(label='wandCtrl',tx='handcontrol',adj=1,cw2=[(winw*0.75)/2,(winw*0.75)/2])
    wand =mc.textFieldGrp(label='Wand',tx='genericWand',adj=1,cw2=[(winw*0.75)/2,(winw*0.75)/2])
    mc.setParent('..')
    mc.rowColumnLayout(nc=2,cw=[(1,winw*0.25),(2,winw*0.75)],adj=True)
    animateWand= mc.checkBox( label='Animate Wand')
    curveName = mc.textFieldGrp(label='Wand Animation Curve',adj=1,cw2=[(winw*0.75)/2,(winw*0.75)/2])
    mc.setParent('..')
    mc.rowColumnLayout('wand section',nc=4,cw=[(1,winw/4),(2,winw/4),(3,winw/4),(4,winw/4)],adj=True)
    wand1 = mc.button(label="Magician",command=lambda *args:ImportWand(mc.button(wand1,query=True,label=True)))
    wand2 = mc.button(label="Witch",command=lambda *args:ImportWand(mc.button(wand2,query=True,label=True)))
    wand3 = mc.button(label="Wizard",command=lambda *args:ImportWand(mc.button(wand3,query=True,label=True)))
    wand4 = mc.button(label="Sorcerer",command=lambda *args:ImportWand(mc.button(wand4,query=True,label=True)))
    mc.setParent('..')
    mc.setParent('..')
    
    mc.frameLayout(label='Particle settings',cll=True,cl=True)
    numOfParticlesControl = mc.intSliderGrp(label='number of particles',minValue=10, maxValue=1000, value=50,field=True)
    gravityControl = mc.intSliderGrp(label='Gravity',minValue=0, maxValue=10, value=0,field=True)
    mc.rowColumnLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    color1=mc.colorSliderGrp( label='Color 1', rgb=(0, 0, 1),adj=1)
    color2=mc.colorSliderGrp( label='Color 2', rgb=(0, 1, 0),adj=1)
    mc.setParent('..')
    mc.rowColumnLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    objParticles = mc.checkBox(label='Object Particles')
    mc.separator(st="out",w=winw)    
    mc.setParent('..')
    mc.setParent('..')


    mc.frameLayout( label='Beam settings',cll=True,cl=True)
    mc.rowColumnLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    animateBeam = mc.checkBox( label='Animate Beam')
    beamEndFrame = mc.intFieldGrp(nf=1,label="Beam end Frame",value1=30)
    mc.separator(st="out",w=winw)
    mc.setParent('..')
    mc.setParent('..')

    mc.frameLayout( label='Magical animations',cll=True,cl=False)
    mc.rowColumnLayout(nc=2,cw=[(1,winw*0.75),(2,winw*0.25)],adj=True)
    animOffset1 = mc.intFieldGrp( label='group animation offset',nf=2,value1=0,value2=0,enable2=False,adj=1)
    random = mc.checkBox( label='random offsets',onc=lambda *args:mc.intFieldGrp(animOffset1,edit=True,enable2=True),ofc=lambda *args:mc.intFieldGrp(animOffset1,edit=True,enable2=False))
    mc.setParent('..')

    tabs = mc.tabLayout('effects tabs',innerMarginWidth=5, innerMarginHeight=5)
    shrinkGrow = mc.columnLayout('shrinkGrow',cw=winw,adj=True,cat=['both',padding])
    mc.rowColumnLayout(nc=3,cw=[(1,winw/2),(2,winw/2)],adj=True)
    startFrame1 = mc.intFieldGrp(nf=1,label="Start Frame",value1=1,adj=1)
    endFrame1 = mc.intFieldGrp(nf=1,label="end Frame",value1=30,adj=1)
    mc.setParent('..')
    scaleFactor = mc.floatSliderGrp(label='Scale Factor',minValue=0.1, maxValue=5, value=2,field=True,pre=2)
    projectionSize = mc.floatSliderGrp(label='Projection Size',minValue=2, maxValue=5, value=2,field=True)
    spacing1 = mc.floatSliderGrp(label='Frame Spacing',minValue=1, maxValue=10, value=5,field=True)
    animated1 = mc.checkBox( label='Animate')
    mc.setParent( '..' )

    levitation = mc.columnLayout('levitation',cw=winw,adj=True,cat=['both',padding])
    mc.rowColumnLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    startFrame2 = mc.intFieldGrp(nf=1,label="Start Frame",value1=1,adj=1)
    endFrame2 = mc.intFieldGrp(nf=1,label="end Frame",value1=30,adj=1)
    mc.setParent('..')
    floatPercentage = mc.floatSliderGrp(label='floatPercentage',minValue=10, maxValue=100, value=50,field=True)
    height = mc.floatSliderGrp(label='Height',minValue=2, maxValue=20, value=2,field=True)
    spacing2 = mc.floatSliderGrp(label='Frame Spacing',minValue=1, maxValue=10, value=5,field=True)
    float = mc.checkBox( label='Float')
    animated2 = mc.checkBox( label='Animate')

    mc.setParent( '..' )

    cleanUp = mc.columnLayout('cleanUp',cw=winw,cal='center',adj=True,cat=['both',padding])
    mc.rowColumnLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    startFrame3 = mc.intFieldGrp(nf=1,label="Start Frame",value1=1,adj=1)
    endFrame3 = mc.intFieldGrp(nf=1,label="end Frame",value1=30,adj=1)    
    mc.setParent('..')
    spacing3 = mc.floatSliderGrp(label='Frame Spacing',minValue=1, maxValue=10, value=5,field=True)
    mc.rowColumnLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    mc.button(label='Store starting positions',command=lambda *args:GetObjCoordArray('source'))
    mc.button(label='Store ending positions',command=lambda *args:GetObjCoordArray('destination'))
    mc.setParent('..')
    animated3 = mc.checkBox( 'animated3',label='Animate')
    mc.setParent( '..' )

    mc.tabLayout( tabs, edit=True, tabLabel=((shrinkGrow, 'Shrink/Grow'), (levitation, 'Levitation'), (cleanUp, 'Clean up')) )
    mc.setParent( '..' )
    mc.setParent( '..' )

    mc.button(label='Select objects',w=winw,command= lambda *args:mc.select(all=True,visible=True,hierarchy=True))
    mc.rowLayout(nc=2,cw=[(1,winw/2),(2,winw/2)],adj=True)
    mc.button(label='Execute selected',w=winw/2,command= lambda *args:AnimManager(
        
        #Wand UI Values
        mc.intSliderGrp(wandPrecision,q=True,v=True),
        mc.textFieldGrp(curveName,q=True,tx=True), 
        mc.intFieldGrp(wandStartFrame,q=True,v1=True),
        mc.intFieldGrp(wandEndFrame,q=True,v1=True),
        mc.textFieldGrp(wandCtrl,q=True,tx=True), 
        mc.textFieldGrp(wand,q=True,tx=True), 
        mc.intFieldGrp(beamEndFrame,q=True,v1=True),
        mc.checkBox(animateWand,q=True,v=True),
        mc.checkBox(animateBeam,q=True,v=True),
        
        #Particle UI Values
        mc.intSliderGrp(numOfParticlesControl,q=True,v=True),
        mc.intSliderGrp(gravityControl,q=True,v=True),
        mc.colorSliderGrp(color1,q=True,rgb=True),
        mc.colorSliderGrp(color2,q=True,rgb=True),
        mc.checkBox(objParticles,q=True,v=True),

        
        #Anim offset UI Values
        mc.checkBox(random,q=True,v=True),
        mc.intFieldGrp(animOffset1,q=True,v1=True),
        mc.intFieldGrp(animOffset1,q=True,v2=True),


        #shrinkGrow UI Values
        mc.intFieldGrp(startFrame1,q=True,v1=True), 
        mc.intFieldGrp(endFrame1,q=True,v1=True), 
        mc.floatSliderGrp(scaleFactor,q=True,v=True), 
        mc.floatSliderGrp(projectionSize,q=True,v=True),
        mc.floatSliderGrp(spacing1,q=True,v=True),
        mc.checkBox(animated1,q=True,v=True),
        
        #Levitation UI Values
        mc.intFieldGrp(startFrame2,q=True,v1=True), 
        mc.intFieldGrp(endFrame2,q=True,v1=True), 
        mc.floatSliderGrp(floatPercentage,q=True,v=True), 
        mc.floatSliderGrp(height,q=True,v=True), 
        mc.floatSliderGrp(spacing2,q=True,v=True),
        mc.checkBox(float,q=True,v=True),
        mc.checkBox(animated2,q=True,v=True),
         
        #Cleanup UI Values
        mc.intFieldGrp(startFrame3,q=True,v1=True), 
        mc.intFieldGrp(endFrame3,q=True,v1=True),
        mc.floatSliderGrp(spacing3,q=True,v=True),
        mc.checkBox(animated3,q=True,v=True),
        )
    )
    mc.button(label='Quit', w=winw/2,command=lambda *args:CancelProc(win))
    mc.setParent('|')
    
    mc.showWindow(win)

if __name__ == "__main__":
    CreateUI()
