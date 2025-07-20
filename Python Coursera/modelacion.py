from fenics import *
import matplotlib.pyplot as plt

# ─── 1. Mesh & Function Spaces ────────────────────────────────
nx, ny = 40, 40
mesh = UnitSquareMesh(nx, ny)

V = VectorFunctionSpace(mesh, "P", 2)   # velocity
Q = FunctionSpace(mesh, "P", 1)         # pressure
T_space = FunctionSpace(mesh, "P", 1)   # temperature

# Mixed space for velocity + pressure
W = MixedFunctionSpace([V, Q])

# ─── 2. Trial/Test Funcs & Variables ─────────────────────────
u_p = Function(W)
u, p = split(u_p)
v, q = TestFunctions(W)

T = Function(T_space)
S = TestFunction(T_space)
T_n = interpolate(Constant(20.0), T_space)  # initial temperature

# ─── 3. Physical Parameters ──────────────────────────────────
rho = 1.0         # density
mu = 1e-3         # dynamic viscosity
g = 9.81          # gravity
beta = 0.003      # thermal expansion coefficient
T_ref = 20.0      # reference temperature
kappa = 1e-2      # thermal diffusivity
dt = 0.01         # time step
t_end = 2.0       # simulation time

# ─── 4. Boundary Conditions ───────────────────────────────────
def hot(x, on_boundary):
    return near(x[0], 0) and on_boundary

def cold(x, on_boundary):
    return near(x[0], 1) and on_boundary

bc_T = [DirichletBC(T_space, Constant(100.0), hot),
        DirichletBC(T_space, Constant(0.0), cold)]

bc_u = DirichletBC(W.sub(0), Constant((0, 0)), "on_boundary")
bcs = [bc_u]  # velocity no-slip

# ─── 5. Variational Forms ────────────────────────────────────
# Navier–Stokes variational form (Boussinesq term added)
F1 = rho*dot((u - u), v)/dt*dx \
     + rho*dot(dot(u, nabla_grad(u)), v)*dx \
     + mu*inner(grad(u), grad(v))*dx \
     - p*div(v)*dx \
     - rho*g*beta*(T_n - T_ref)*v[1]*dx \
     + div(u)*q*dx

# Energy equation (convection + diffusion)
F2 = (T - T_n)/dt*S*dx \
     + dot(u, grad(T))*S*dx \
     + kappa*dot(grad(T), grad(S))*dx

# ─── 6. Time-stepping ─────────────────────────────────────────
t = 0.0
while t < t_end:
    solve(lhs(F1) == rhs(F1), u_p, bcs)
    u, p = u_p.split()
    solve(lhs(F2) == rhs(F2), T, bc_T)
    T_n.assign(T)

    t += dt
    print(f"t = {t:.2f} s")

# ─── 7. Visualization ─────────────────────────────────────────
plt.figure()
plot(u, title="Velocity field")
plt.show()

plt.figure()
plot(T, title="Temperature field")
plt.colorbar()
plt.show()
