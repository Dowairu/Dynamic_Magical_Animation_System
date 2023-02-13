

**Manual**

**How to run the script**

Before running the script, line 27 and 28 should be changed to the user’s directory. If the user wants to create wand

animations, they can import one of four pre-sets provided or make use of their rigged model, making sure that they

enter the name of their wand control into the UI.

A wand is not needed to use the program. Each magical effect has a select button to select an object to be animated.

If the user wants to animate a specific object, they can select it directly. To animate a group of objects, the user must

keep the objects they want animated visible and everything else hidden.

**How to Use the UI**

The UI is explained in the video titled “UI Explanation” in the artefacts folder.

**Algorithm/Design**

The overall design of this program is simple. Most of it involved solving minor problems and combining them to

make a more complicated system. I developed an algorithm for each magical effect, then added functionality for

stacking and combination of animations. My program is based on six core procedures.

AnimateWand – This function makes use of vectors to animate the wand along the curve. First, we rebuild the curve,

so the number of points matches the number of frames for the animation. Then we check for the animate beam. If

the option is chosen by the user there are a few extra steps. Before going through the loop, we add some extra

points to the curve. The position of this added point is the same as the position of the object, the wand

blasting/beaming. This way the wand animation will end pointing at the object. Then we enter a loop, starting from

the first point.

•

•

We the Get position of the point on the curve.

Then we align the wand to the point. To align these two things, we get the position of the point and find the

angle between the wands position vector and the curve points position vector. Then rotate our wand

accordingly.

•

Once rotated, we set the rotation keyframes. And go through the loop until the last point on the curve.

BeamBlastAnimation – Animates a nparticle emitter along a path from a wand to a chosen object. This function is

embedded within the wand animation function and only runs if the animate beam option is chosen by the user.

~~First, we check w~~hat type of object we are blasting. If the object is a curve, we just duplicate the original curve and

animated our emitter along with it. If it is any other object or group of objects, we.

•

•

•

•

•

•

Point the wand to the object.

Get the position of the tip of the wand.

Create a curve starting at the wand tip and ending at the object’s position.

Create our emitter with the users’ particles settings.

Animate the emitter along this curve.

Group everything to keep the outliner clean.

ShrinkGrow – Animates an object shrinking or growing. The first thing we do in this function calculates the number

of projections (loops). This is determined by the total number of frames divided by the spacing provided by the user.

Then we use the number of projections for the loop.

•

•

•

•

Calculate the frame we should be on using the start frame of the animation and loop increment.

Duplicate object.

Create and assign a shader to duplicated object.

Set keys on the scale of the duplicated object.





•

•

Set keys on the transmission of duplicated objects shader.

Set keys on duplicated objects visibility.

Levitation- Animates an object levitating upwards with an option to make it float in place. First, we determine if the

user has chosen the “float” tag. If they have, we calculate the number of frames to be used for levitating and the

number of frames to be used for floating. Then we proceed with the algorithm.

•

•

•

•

Get object position.

Add random values between 0 and 1 to x position and z position.

Calculate the height increment for the current frame and add it to the y position.

Set keyframes on all translation values.

If the float tag is true

•

•

Add random values between 0 and 1 to x position and z position.

Set keyframes on all translation values.

CleanUp – Animates an object or group of objects moving from one position to another. This is quite simple, the

more complicated part comes with the method of storing these values before accessing them. The first part of this

function is dynamically storing the starting and ending positions of objects in a dictionary. The dictionary is like this,

key=objectName, value = [[starting positions] [ending positions]]. The rest of the function is just accessing these

values using generated lists, then interpolating between the start and end positions with added random values and

setting keyframes of translation.

ParticleEmitter – Creates a surface emitter from the provided object or generates one if no object is given.

There are quite a few functions I created to bridge the gaps between these functions and create a fully functional

program. I made many functions that I have classed as “utility” functions, designed to make certain things easier and

eliminate unnecessary lines of code that would have been in several places. Here the most popular ones.

•

•

•

FrameCalc – calculates the total number of frames for animation.

GetObjPos – gets the current position of an object and returns the value in a list of XYZ positions.

SnapToPos – points the front normal of an object to the position of another object.

**Script structure.**

Here is a diagram showing the script structure and flow control of my program.





The Program starts with CreateUI in the Main function. Once the user has chosen all their settings and clicks execute,

all the relevant values are sent to AnimManager. Dependent on the options chosen by the user if statements are

used to decide which functions to run. Within each function, there are further if statements to check for other values

and options. Once all things have been checked, the function will run the required code. All core functions run in a

nested for loop, they run the commands for every object selected.

**Improvements**

The first improvement I would have been the wand function. I would have given it more functionality, making it

follow an object even after animating to mimic the user actively manipulating an object.

I would also have added a transformation/shapeshifting/morphing function. My first attempt at this using linear

interpolation of the position of vertices did not work very well. I would like to add such functionality using

techniques like mesh registration or mesh reconstruction from a point cloud. The last thing I would improve about

my program is the programming. I would have liked to implement the use of Object-oriented programming

techniques where necessary.

**Visual Artefacts**

Because my project is based on animation, my visual artefacts are in video form. They are in the visual artefacts

folder of the project. All settings are shown in the videos and objects used are also provided.





##Python Modules and Functions
*genrated with pydoc and converted to md*

David Magical Animation System:  
   
This program is designed to create procedural animations using different simple algorithms.  
it takes an object or group of objects as input and applies a selected animation onto them.   
The animations can also be stacked so that a user can perform multiuple actions on one or multiple objects

   
**Modules**

      

 

[random](random.html)  

   
**Functions**

      

 

**AnimManager**(wandPrecision, curveName, wandStartFrame, wandEndFrame, wandCtrl, wand, beamEndFrame, animateWand, animateBeam, numOfParticlesControl, gravityControl, color1, color2, objParticles, random, animOffset1, animOffset2, startFrame1, endFrame1, scaleFactor, projectionSize, spacing1, animated1, startFrame2, endFrame2, floatPercentage, height, spacing2, float, animated2, startFrame3, endFrame3, spacing3, animated3, \*pArgs)

This funtion is resposible for collecting all the values from the UI  
and running all the other funtions in the correct order and with the   
necesary variables:  
   
\- wandPrecision:             the level of detail that the wand follows the curve.                  
\- curveName:                 the curve being used for wand animtion.  
\- wandStartFrame:            start frame of animation.  
\- wandEndFrame:              end frame of animation.  
\- wandCtrl:                  rig control for the wand.  
\- wand:                      wand we are animating.  
\- beamEndFrame:              end frame of Beam animation.  
\- animateWand:               Flag for wether Wand will be animated.  
\- animateBeam:               Flag for wether Beam will be animated.  
\- numOfParticlesControl:     number of particles for the system to generate persecond.  
\- gravityControl:            gravity of the nucleus affecting the particles.  
\- color1:                    first color of the gradient.  
\- color2:                    Second color of the gradient.  
\- objParticles:              Flag for wether particles will be used or not on objects.  
\- random:                    Flag for wether random offset will be used or not.  
\- animOffset1:               lower range of random offset, but also main offset if random i not chosen.  
\- animOffset2:               upper range of random offset.  
\- startFrame1:               start frame of ShrinkGrow.  
\- endFrame1:                 end frame of ShrinkGrow.  
\- scaleFactor:               number original object is multiplied by  .               
\- projectionSize:            size of the projection effect.  
\- spacing1:                  number of frames between each keyframe.  
\- animated1:                 Flag for wether ShrinkGrow will be animated.  
\- startFrame2:               start frame of levitation.  
\- endFrame2:                 end frame of levitation.  
\- floatPercentage:           percentage of frames to be used for floating.  
\- height:                    height the object will levitate to.           
\- spacing2:                  number of frames between each keyframe.  
\- float:                     Flag for wether Levitation will be add a float at the top.  
\- animated2:                 Flag for wether Levitation will be animated.  
\- startFrame3:               start frame of CleanUp.  
\- endFrame3:                 end frame of CleanUp.           
\- spacing3:                  number of frames between each keyframe.  
\- animated3:                 Flag for wether CleanUp will be animated.

**AnimateWand**(wandCtrl, wand, curveName, startFrame, endFrame, precision, color1, color2, numParticles, grav, \*args)

Animates the wand to the movement of a curve:  
   
\- wand:          wand we are animating.  
\- curveName:     the curve being used for animtion.  
\- startFrame:    start frame of animation.  
\- endFrame:      end frame of animation.  
\- precision:     the level of detail that the wand follows the curve.  
\- color1:        first color of the gradient  
\- color2:        Second color of the gradient  
\- numParticles:  number of particles for the system to generate persecond  
\- grav:          gravity of the nucleus affecting the particles.  
\- args:          extra arguments

**BlastAnimation**(wandCtrl, wand, object, wandstFrame, stBeamFrame, endBeamFrame, color1, color2, numParticles, grav)

extension to the wand function. It animates a blast between the wand and the object being affected:  
   
\- wandCtrl:     rig control for the wand.      
\- wand:         wand the balst is coming from.  
\- object:       object the being blasted.  
\- wandstFrame:      start frame of the wand animation.  
\- startBeamFrame:   start frame of blast animation.  
\- endBeamFrame:     end freame of blast animation.  
\- color1:        first color of the gradient  
\- color2:        Second color of the gradient  
\- numParticles:  number of particles for the system to generate persecond  
\- grav:          gravity of the nucleus affecting the particles.

**CancelProc**(win, \*args)

Closes the window when 'Quit' button is pressed  
   
win: The window we are closing

**CleanUp**(startFrame, endFrame, spacing, random, offset1, offset2)

Creates an animation for objects poasitions. it takes the initial position of objects  
once the user has moved the objects it animates the objects floating from one point to another  
   
\- startFrame:        start frame of levitation.  
\- endFrame:          start frame of levitation.  
\- spacing:           number of frames between each keyframe.            
\- random:            random flag to determine wether to use random offsets  
\- offset1:           lower range of random offset, but also main offset if random i not chosen  
\- offset2:           upper range of random offset

**ClearScene**()

Clears everything in the scene for a fresh scene.

**CreateGradient**(particleName, color1, color2)

Creates a gradient using two colors and applies it to a particle system  
   
particleName:    Particle system were changing the color of  
color1:          first color of the gradient  
color2:          Second color of the gradient

**CreateMotionPath**(object, startFrame, endFrame, precision)

Generates a motionpath for animated objects.  
The paths generated will be used to control the movement of the wand  
if the user decides to use a wand:  
   
 - object:       object we are getting the motion path from  
 - startFrame:   start frame of objects existing animation  
 - endFrame:     end frame of objects existing animation  
 - precision:    how precise the curve should be to the animation

**CreateShader**(shaderType, shaderName, object, number)

this functions creates a shader of specified type:  
   
\- shaderType: the type of shader we are creating eg:Lambert,standard surface etc.  
\- shaderName: the name of the shader.  
\- object:     object the shader is being applied to.  
\- number:     the shader number at the end of its name to avoid clashing   
             with existing shaders of the same type.  
   
 Return Value:  
\- returns the name of the shader

**CreateUI**()

Creates The UI for the program.

**GetObjCoordArray**(flag)

this funtion fills up a global dictionary that is used to animate the floating cleanup function.  
   
\- flag:  Used to determine what values to save into the dictionary can either be 'source' or 'destination'

**GetObjPos**(objName)

Gets the position of an object and returns it as a list:  
   
\- objName: the object we are getting the pos of.  
   
 Return Value:  
\- objScale:      List of object xyz pos

**GetObjSize**(objName)

Gets the size of an object and returns it as a list:  
   
\- objName: the object we are getting the size of.  
   
Return Value:  
\- objScale:      List of object xyz scales

**GetParentNode**(selectedObject)

Gets the parent Node for every object in the list  
\- selectedObject:  List of objects   
   
Return Values:  
\- object:    list of Parent nodes

**ImportWand**(wand)

This function imports a wand selected by the user. Importing a wand also lets users create wand animations:  
   
\- wand: name/type of wand being imported.

**ParticleEmitter**(numOfParticles, grav, object, color1, color2)

funtion that creates creates creates and initialises and emiiter.  
   
\- numOfParticles: number of particles for the system to generate persecond.  
\- grav:           gravity of the nucleus affecting the particles.  
\- object:         the object being used as an emiiter. if this argument is false and emitter is created and returned.  
   
Return Values:  
\- particles:      List od nparticles nodes  
\- emitSphere:     List of sphere node

**SetProjectKey**(shader, startFrame, endFrame)

Sets the transmission attributte for a shader  
from 0 to 1 or 1 to 0 for a specific time frame:  
   
\- shader:       shader we are changing the transmission on.   
\- startFrame:   first keyframe of the transmission.  
\- endFrame:     last keyframe of the transmision.

**SetScaleKey**(object, startFrame, endFrame, scalefactor)

Sets the scale attributte for an object for a specific time frame.  
   
\- object:       object being scaled.   
\- startFrame:   first keyframe of the scaling..  
\- endFrame:     last keyframe of the scaling..  
\- scalefactor:  number original object is multiplied by.

**SetVisibleKey**(object, startFrame, endFrame)

Sets the visibility attributte for an object.  
from 0 to 1 or 1 to 0 for a specific time frame.  
   
\- object:       object we are changing the visibility on.   
\- startFrame:   first keyframe of the visibilty.  
\- endFrame:     last keyframe of the visibilty.

**ShrinkGrow**(object, startFrame, endFrame, scaleFactor, projectionSize, spacing, random, offset1, offset2)

shrinks or grows the size of an object:  
   
\- object:            object being shrunk/grown.  
\- scalefactor:       number original object is multiplied by.  
\- projectionSize:    size of the projection effect.  
\- spacing:           number of frames between each keyframe            
\- random:            random flag to determine wether to use random offsets  
\- offset1:           lower range of random offset, but also main offset if random i not chosen  
 -offset2:           upper range of random offset

**SnapToPos**(wand, object, \*args)

Snaps an objects local x axis to the position and angle of another object.  
   
\- wand: object that we are snapping/rotating.  
\- object: object we are snapping to.

**frameCalc**(stf, enf)

calculates the total number of frames for an animation.  
   
\- stf: starting frame.  
\- enf: ending frame.  
   
Return Values:  
nFrames:     The total number of frames between stf and enf

**levitation**(object, startFrame, endFrame, floatPercentage, height, spacing, float, random, offset1, offset2)

animates an object levitating:  
   
\- object:            object being levitated.  
\- startFrame:        start frame of levitation.  
\- endFrame:          start frame of levitation.  
\- floatPercentage:   percentage of frames to be used for floating.  
\- height:            height the object will levitate to.  
\- spacing:           number of frames between each keyframe.  
\- float:             flag that determines wether the object   
                     will float in place at the desired height.  
\- random:            random flag to determine wether to use random offsets  
\- offset1:           lower range of random offset, but also main offset if random i not chosen  
 -offset2:           upper range of random offset

   
**Data**

      

 

**filePath** = r'David\_Owairu\_Scripting\\src\\'  
**name** = '\_\_version\_\_'  
**objCoordDict** = OrderedDict()  
**submission\_Path** = r'\\home\\xyang\\maya\_scripts\\submission'

   
**Author**

      

 

David Owairu