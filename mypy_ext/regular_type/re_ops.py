from typing import Set, cast

from automata.base.exceptions import RejectionException
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


def extract_middle(msg: str, prefix: str, suffix: str) -> str:
    assert msg.startswith(prefix) and msg.endswith(suffix)
    return msg[len(prefix) : -len(suffix)]


def DFA_reachable(dfa: DFA, state: int, target: Set[int]) -> bool:
    """Tell if a `state` is reachable to any `target` state in the `dfa`."""
    reachable = [state]
    i = 0

    while i < len(reachable):
        s = reachable[i]
        for succ in dfa.transitions[s].values():
            if succ in target:
                return True

            if succ not in reachable:
                reachable.append(succ)
        i += 1

    return False


def re_starts_with(regex: str, prefix: str) -> bool:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    try:
        dfa.read_input(prefix)
    except RejectionException as ex:
        msg = cast(str, ex.args[0])
        state = int(extract_middle(msg, "the DFA stopped on a non-final state (", ")"))
        return DFA_reachable(dfa, state, dfa.final_states)
    else:
        return True
