`closeformIK` is an analytical inverse kinematics calculation library for a 6-DOF robotic arm. When solving for inverse kinematics, you should call the `CIK` function. Below is the description of the input parameters for the function:

- `eeTform`: End-effector trans 4x4 matrix
- `MdhParams`: DH parameter table including `d`, `a`, `alpha`, `theta`
- `jointlimits`: Joint angle limits
- `joint_ref`: Reference joint angles

Here's a typical application example:

```python
from closeformIK import CIK
import numpy as np

# Define Modified Denavit-Hartenberg parameters
MdhParams = np.array([
    [a1, alpha1, d1, theta1],
    [a2, alpha2, d2, theta2],
    [a3, alpha3, d3, theta3],
    [a4, alpha4, d4, theta4],
    [a5, alpha5, d5, theta5],
    [a6, alpha6, d6, theta6]
])

# Define joint angle limits
Jointlimits = [
    [limit_n_j1, limit_p_j1],  # Joint 1
    [limit_n_j2, limit_p_j2],  # Joint 2
    [limit_n_j3, limit_p_j3],  # Joint 3
    [limit_n_j4, limit_p_j4],  # Joint 4
    [limit_n_j5, limit_p_j5],  # Joint 5
    [limit_n_j6, limit_p_j6]   # Joint 6
]

# Compute the inverse kinematics solution
sol, allsol = CIK(eeTform, MdhParams, Jointlimits, joint_ref=joint_ref)