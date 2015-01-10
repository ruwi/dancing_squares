% Dancing squares
% W
% 10.01.2015

# What are we doing and why?

We are implementing a simulation of a simple dynamic system using two different
architectural approaches to compare them.

One will be ad hoc and the other will be using the Entity Component System
(ECS) architecture.

# Model

+ 2D
+ no rotation
+ discrete time and space
+ instead of velocity: number of time steps to wait between moving by 1
    + not every particle moves at all
    + some particles move in one direction but not the other 
+ collisions
    + collisions happen when 
        + `AB` -- either particle A or B is trying to move to the position of
          the other
        + `A_B` -- A and B are trying to move to the same position
    + when a collision happens, we invert the *active* "velocity" components




