from ltlf2dfa.parser.ltlf import LTLfParser
from ltlf2dfa.base import MonaProgram
from ltlf2dfa.ltlf2dfa import invoke_mona, createMonafile

def to_mona(formula):
    parser = LTLfParser()
    formula = parser(formula)

    mona_p_string = MonaProgram(formula).mona_program()
    createMonafile(mona_p_string)
    mona = invoke_mona()

    return mona

if __name__ == "__main__":
    print(to_mona("G a && F b"))