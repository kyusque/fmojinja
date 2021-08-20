from ..mixin import CpptrajMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class Hbond(CpptrajMixin):

    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """ 
{%- for path in trajin %}
parm {{ parm }}
trajin {{ path }} 1 last {{ offset }}
hbond BB {{ mask if mask else "" }} {{ "dist {}".format(dist) if dist else "" }} avgout {{ prefix ~ path.stem }}.dat
run
{% if trajin | length != loop.index %} clear all{% endif %}
{% endfor %}

"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p.add_argument("-P", "--prefix", default="hbond/")
        p.add_argument("--offset", type=int, default=1)
        p.add_argument("-d", "--dist", type=float, default=6.0, help="H bond distance (Acceptor and Donor) cutoff")
        return super(Hbond, cls).set_arguments(p)
