from ..mixin import TemplateRendererMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class ReformatPdb(TemplateRendererMixin):
    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
BEGIN { i = 1
{%- set letters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" | list) %}
{%- for _ in chain_starts %}; tag[{{ loop.index }}] = "{{ letters[loop.index0] }}"{% endfor -%}
; tag[{{ (chain_starts | length) + 1}}] = "{{ letters[(chain_starts | length)] }}" }
# Left-justification
/^ATOM|^HETATM/ && substr($0, 18, 2) == "  " { $0 = substr($0, 0, 17) substr($0, 20, 1) "  "  substr($0, 21) }
/^ATOM|^HETATM/ && substr($0, 18, 1) == " " { $0 = substr($0, 0, 17) substr($0, 19, 2) " "  substr($0, 21) }
# Reformat chain names
{% for seq_id in chain_starts -%}
!start_seq_{{ seq_id }} && int(substr($0, 23, 4)) == {{ seq_id }} { start_seq_{{ seq_id }} = 1; i = i + 1 }
{% endfor %}# Print
{ print substr($0, 0, 21) tag[i] substr($0, 23) }


"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(ReformatPdb, cls).set_arguments(p)
        p.add_argument("-c", "--chain-starts", nargs="*", default=[])
        return p