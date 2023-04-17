from typing import Tuple, TypeAlias

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.regex import regex as RE

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

Regex: TypeAlias = str
Char: TypeAlias = str


def re_length(regex: Regex) -> Tuple[int, int | None]:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    # TODO: empty languages
    return dfa.minimum_word_length(), dfa.maximum_word_length()


def re_starts_with(regex: Regex, prefix: str) -> bool:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    prefix_dfa = DFA.from_prefix(dfa.input_symbols, prefix)
    return dfa <= prefix_dfa


def re_starts_with_re(regex: Regex, prefix: Regex) -> bool:
    prefix_regex = f"{prefix}.*"
    return RE.issubset(regex, prefix_regex, input_symbols=NFA.from_regex(regex).input_symbols)


def re_ends_with(regex: Regex, suffix: str) -> bool:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    suffix_dfa = DFA.from_suffix(dfa.input_symbols, suffix)
    return dfa <= suffix_dfa


def re_ends_with_re(regex: Regex, suffix: Regex) -> bool:
    suffix_regex = f".*{suffix}"
    return RE.issubset(regex, suffix_regex, input_symbols=NFA.from_regex(regex).input_symbols)


def re_contains(regex: Regex, substring: str) -> bool:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    infix_dfa = DFA.from_substring(dfa.input_symbols, substring)
    return dfa <= infix_dfa


def re_contains_re(regex: Regex, subregex: Regex) -> bool:
    infix_regex = f".*{subregex}.*"
    return RE.issubset(regex, infix_regex, input_symbols=NFA.from_regex(regex).input_symbols)


def re_may_have_char_at(dfa: DFA, ch: Char, index: int) -> bool:
    assert len(ch) == 1
    prefix_dfa = DFA.nth_from_start(dfa.input_symbols, ch, index)
    return not (dfa & prefix_dfa).isempty()


def re_char_at(regex: Regex, index: int) -> Regex:
    dfa = DFA.from_nfa(NFA.from_regex(regex))
    candidates = set()
    for ch in dfa.input_symbols:
        if re_may_have_char_at(dfa, ch, index):
            candidates.add(ch)
    assert len(candidates) > 0
    return "|".join(candidates)
