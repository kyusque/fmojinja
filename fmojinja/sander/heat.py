from ..mixin import SanderMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class Heating(SanderMixin):
    """
    e.g. python -m fmojinja.sander heat > $*.in; sander -O -i $*.in -o $*.mdout -r $*.rst_opt -p $*.parm -c $< -ref $<
    """

    @classmethod
    def template(cls):
        return "{{ title }}" + f" !Generated by fmojinja version {get_version()}" + """ 
&cntrl
  nstlim={{ nsteps_limit }},
{%- if restraint_mask != None %}
  ntr=1,
  restraintmask="{{ restraint_mask }}",
  restraint_wt={{ restraint_wt }},
{%- else %}
  ntr=0,
{%- endif %}
  cut={{ cut }},
  ntt={{ ntt }}, 
  gamma_ln={{ gamma_ln }}, 
  tempi={{ temperature_start }}
  temp0={{ temperature_end }},
  taup={{ pressure_relaxation_time }}, 
  pres0={{ pressure }},
  dt={{ dt }},
  ntpr={{ nt }}, 
  ntwr={{ nt }}, 
  ntwx={{ nt }}, 
  ntwv={{ nt }}, 
  ntwe={{ nt }},
  ig={{ seed }},
  vlimit={{ vlimits }},
  iwrap={{ iwrap }},
  nmropt={{ nmropt }},
/
{%- if nmropt > 0 %}
&wt 
  type='TEMP0', 
  istep1=0, 
  istep2={{ (nsteps_limit * 0.8) | int }}, 
  value1={{ temperature_start }}, 
  value2={{ temperature_end }}, 
/
&wt 
  type='END', 
/
{%- endif %}

"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(Heating, cls).set_arguments(p)
        p.add_argument("-ps", "--pico-second")
        p.add_argument("-ntt", default=3)
        p.add_argument("-pr", "--pressure", default=1.0)
        p.add_argument("-ts", "--temperature-start", default=0)
        p.add_argument("-te", "--temperature-end", default=300)
        p.add_argument("-taup", "--pressure-relaxation-time", default=2.0)
        p.add_argument("-gl", "--gamma-ln", default=1.0)
        p.add_argument("-rm", "--restraint-mask", help="restraint mask. e.g. '!@H=' ")
        p.add_argument("-rw", "--restraint-wt", default=10, help="the weight (kcal/mol angstrom)"
                                                                 " for the positional restraints")
        p.add_argument("-nmropt", default=1)
        p.add_argument("-iwrap", default=1)
        return p
