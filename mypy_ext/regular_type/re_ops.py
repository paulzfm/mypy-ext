from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


# def extract_middle(msg: str, prefix: str, suffix: str) -> str:
#     assert msg.startswith(prefix) and msg.endswith(suffix)
#     return msg[len(prefix) : -len(suffix)]
#
#
# def DFA_reachable(dfa: DFA, state: int, target: Set[int]) -> bool:
#     """Tell if a `state` is reachable to any `target` state in the `dfa`."""
#     reachable = [state]
#     i = 0
#
#     while i < len(reachable):
#         s = reachable[i]
#         for succ in dfa.transitions[s].values():
#             if succ in target:
#                 return True
#
#             if succ not in reachable:
#                 reachable.append(succ)
#         i += 1
#
#     return False


def re_starts_with(regex: str, prefix: str) -> bool:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    prefix_dfa = DFA.from_prefix(dfa.input_symbols, prefix)
    return dfa <= prefix_dfa


def re_ends_with(regex: str, suffix: str) -> bool:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    suffix_dfa = DFA.from_suffix(dfa.input_symbols, suffix)
    return dfa <= suffix_dfa
