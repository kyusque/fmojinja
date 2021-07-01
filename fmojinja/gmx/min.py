from ..mixin import TemplateRendererMixin

class Min(TemplateRendererMixin):
	@classmethod
	def template(cls):
		return """
define       =           ;
integrator   = steep     ; Algorithm (steep = steepest descent minimization)
emtol        = 1000.0    ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm
emstep       = 0.01      ; Energy step size
nsteps       = 50000     ; Maximum number of (minimization) steps to perform
nstlist	     = 100       ; Frequency to update the neighbor list and long range forces
ns_type      = grid      ; Method to determine neighbor list (simple, grid)
coulombtype  = PME       ; Treatment of long range electrostatic interactions
rcoulomb     = 1.2       ; Short-range electrostatic cut-off
rvdw         = 1.2       ; Short-range Van der Waals cut-off
pbc          = xyz       ; Periodic Boundary Conditions (yes/no)
"""
