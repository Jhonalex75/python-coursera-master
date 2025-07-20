# Double pendulum

# The analysis is in terms of Lagrangian mechanics.
# The Lagrangian variables are angle of upper bar, angle of lower bar,
# measured from the vertical.

# Bruce Sherwood
from vpython import *
'''
From https://scipython.com/blog/the-double-compound-pendulum:
L1 is length of upper rod of Mass M1, L2 is length of lower rod of mass M2
theta1 is angle from vertical of upper rod, theta2 is angle from vertical of lower rod
thetadot1 is time derivative of theta1, thetadot2 is time derivative of theta2

p1 = (1/3)*M1*L1**2*thetadot1 + M2*L1**2*thetadot1 + (1/2)*M2*L1*L2*thetadot2*cos(theta1-theta2)
p2 = (1/3)*M2*L2**2*thetadot2 + (1/2)*M2*L1*L2*thetadot1*cos(theta1-theta2)

thetadot1 = (6/(L1**2))*(2*p1 - 3*(L1/L2)*cos(theta1-theta2)*p2)/(4*(M1+3*M2) - 9*M2*(cos(theta1-theta2))**2)
thetadot2 = (6/(M2*L2**2))*(2*p2*(M1+3*M2) - 3*M2*(L2/L1)*cos(theta1-theta2)*p1)/(4*(M1+3*M2) - 9*M2*(cos(theta1-theta2)**2))

dp1/dt = -(1/2)*M2*L1*L2*thetadot1*thetadot2*sin(theta1-theta2) - ((1/2)*M1+M2)*g*L1*sin(theta1)
dp2/dt = (1/2)*M2*L1*L2*thetadot1*thetdot2*sin(theta1-theta2) - (1/2)*M2*g*L2*sin(theta2)
'''

scene.width = 800
scene.height = 800
scene.range = 1.5
scene.title = "A double pendulum"

g = 9.8
M1 = 1
M2 = 2
d = 0.05 # thickness of each bar
gap = 2*d # distance between two parts of upper, U-shaped assembly
L1 = 0.5 # physical length of upper assembly; distance between axles
I1 = (1/12)*M1*L1**2
L1display = L1+d # show upper assembly a bit longer than physical, to overlap axle
L2 = 1 # physical length of lower bar
I2 = (1/12)*M2*L2**2
L2display = L2+d/2 # show lower bar a bit longer than physical, to overlap axle

hpedestal = 1.1*(L1+L2) # height of pedestal
wpedestal = 0.1 # width of pedestal
tbase = 0.05 # thickness of base
wbase = 8*gap # width of base
offset = 2*gap # from center of pedestal to center of U-shaped upper assembly
pedestal_top = vec(0,hpedestal/2,0) # top of inner bar of U-shaped upper assembly

theta1 = 1.3*pi/2 # initial upper angle (from vertical)
theta2 = 0 # initial lower angle (from vertical)

pedestal = box( pos=pedestal_top-vec(0,hpedestal/2,offset),
                size=vec(wpedestal,1.1*hpedestal,wpedestal),
                color=vec(0.4,0.4,0.5) )
base = box( pos=pedestal_top-vec(0,hpedestal+tbase/2,offset),
                 size=vec(wbase,tbase,wbase),
                 color=pedestal.color )
axle1 = cylinder( pos=pedestal_top-vec(0,0,gap/2-d/4), axis=vec(0,0,-1),
                 size=vec(offset,d/4,d/4), color=color.yellow )

bar1 = box( pos=pedestal_top+vec(L1display/2-d/2,0,-(gap+d)/2), 
                 size=vec(L1display,d,d), color=color.red )
bar1.rotate( angle=-pi/2, axis=vec(0,0,1), origin=vec(axle1.pos.x, axle1.pos.y, bar1.pos.z) )
bar1.rotate( angle=theta1, axis=vec(0,0,1), origin=vec(axle1.pos.x, axle1.pos.y, bar1.pos.z) )

bar1b = box( pos=pedestal_top+vec(L1display/2-d/2,0,(gap+d)/2), 
                 size=vec(L1display,d,d), color=bar1.color )
bar1b.rotate( angle=-pi/2, axis=vec(0,0,1), origin=vec(axle1.pos.x, axle1.pos.y, bar1b.pos.z) )
bar1b.rotate( angle=theta1, axis=vec(0,0,1), origin=vec(axle1.pos.x, axle1.pos.y, bar1b.pos.z) )

pivot1 = vec(axle1.pos.x, axle1.pos.y, 0)

axle2 = cylinder( pos=pedestal_top+vec(L1,0,-(gap+d)/2), axis=vec(0,0,1), 
                size=vec(gap+d,axle1.size.y/2,axle1.size.y/2), color=axle1.color )
axle2.rotate( angle=-pi/2, axis=vec(0,0,1), origin=vec(axle1.pos.x, axle1.pos.y, axle2.pos.z) )
axle2.rotate( angle=theta1, axis=vec(0,0,1), origin=vec(axle1.pos.x, axle1.pos.y, axle2.pos.z) )

#bar2 = box( pos=axle2.pos+vec(L2display/2-d/2,0,(gap+d)/2), opacity=0.5,
bar2 = box( pos=axle2.pos+vec(L2/2,0,(gap+d)/2), 
        size=vec(L2display,d,d), color=color.green )

bar2.rotate( angle=-pi/2,  axis=vec(0,0,1), origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z) )

thetadot1 = 0 # initial rate of change of theta1
thetadot2 = 0 # initial rate of change of theta2
p1 = 0
p2 = 0

graph(scroll=True, xmin=0, xmax=5)
energy = gcurve(color=color.black, label="E<sub>total</sub>", interval=1000)
ktrans = gcurve(color=color.red, label="K<sub>trans</sub>", interval=1000)
krot = gcurve(color=0.7*color.green, label="K<sub>rot</sub>", interval=1000)
PE = gcurve(color=color.blue, label="E<sub>potential</sub>", interval=1000)

y1 = bar1.pos.y
y2 = bar2.pos.y

run = False
def pause(b):
    global run
    run = not run
    if run: b.text = 'Pause'
    else: b.text = 'Run'
button(text='Run', bind=pause)

graphing = False 
tstart = 0
def graphit(b):
    global graphing, tstart, instructions
    graphing = not graphing
    if graphing: 
        instructions.text = ''
        b.text = 'Pause Graph'
        energy.data = []
        ktrans.data = []
        krot.data = []
        PE.data = []
    else: b.text = 'Graph Energy'
wtext(text='     ')
button(text='Graph Energy', bind=graphit)

instructions = wtext(text="""

In Web VPython programs:
To rotate "camera", drag with right button or Ctrl-drag.
To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
  On a two-button mouse, middle is left + right.
To pan left/right and up/down, Shift-drag.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate.""")

dt = 2e-5
t = 0

while True:
    rate(1/dt)
    if not run: continue

    p1 += (-(1/2)*M2*L1*L2*thetadot1*thetadot2*sin(theta1-theta2) - ((1/2)*M1+M2)*g*L1*sin(theta1))*dt
    p2 += ((1/2)*M2*L1*L2*thetadot1*thetadot2*sin(theta1-theta2) - (1/2)*M2*g*L2*sin(theta2))*dt
    
    thetadot1 = (6/(L1**2))*(2*p1 - 3*(L1/L2)*cos(theta1-theta2)*p2)/(4*(M1+3*M2) - 9*M2*(cos(theta1-theta2))**2)
    thetadot2 = (6/(M2*L2**2))*(2*p2*(M1+3*M2) - 3*M2*(L2/L1)*cos(theta1-theta2)*p1)/(4*(M1+3*M2) - 9*M2*(cos(theta1-theta2)**2))
    
    dtheta1 = thetadot1*dt
    dtheta2 = thetadot2*dt
    theta1 += dtheta1
    theta2 += dtheta2
    
    pos1 = vec(bar1.pos) # keep copies of where we were
    pos2 = vec(bar2.pos)
    bar1.axis = L1display*vec(sin(theta1), -cos(theta1), 0)
    bar1.pos = pivot1 + vec(0,0,-(gap+d)/2) + 0.5*L1*hat(bar1.axis)
    bar1b.axis = bar1.axis
    bar1b.pos = bar1.pos+vec(0,0,bar1b.pos.z-bar1.pos.z)
    axle2.pos = pivot1 - vec(0,0,(gap+d)/2) + L1*hat(bar1.axis)
    pivot2 = vec(axle2.pos.x, axle2.pos.y, 0)
    bar2.axis = L2display*vec(sin(theta2), -cos(theta2), 0)
    bar2.pos = pivot2 + 0.5*L2*hat(bar2.axis)
    
    if graphing:
        dpos1 = bar1.pos-pos1
        dpos2 = bar2.pos-pos2
        Ktrans1 = .5*M1*mag2(dpos1/dt)
        Ktrans2 = .5*M2*mag2(dpos2/dt)
        Krot1 = .5*I1*thetadot1**2
        Krot2 = .5*I2*thetadot2**2
        PE1 = M1*g*(bar1.pos.y-y1)
        PE2 = M2*g*(bar2.pos.y-y2)
        total = Ktrans1+Ktrans2+Krot1+Krot2+PE1+PE2
        energy.plot(t, total)
        krot.plot(t,Krot1+Krot2)
        ktrans.plot(t,Ktrans1+Ktrans2)
        PE.plot(t,PE1+PE2)
    
    t = t+dt
