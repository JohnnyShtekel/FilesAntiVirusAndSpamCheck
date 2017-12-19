from model.eml_parser import EmlParser



with open('sample.eml', 'rb') as fhdl:
    a = EmlParser(fhdl)
    print a.parse()