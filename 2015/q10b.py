# naive

elements = {
    "H": {"Sequence": "22", "Decays into": ["H"], "Abundance": 91790.383216},
    "He": {"Sequence": "13112221133211322112211213322112", "Decays into": ["Hf", "Pa", "H", "Ca", "Li"], "Abundance": 3237.2968588},
    "Li": {"Sequence": "312211322212221121123222112", "Decays into": ["He"], "Abundance": 4220.0665982},
    "Be": {"Sequence": "111312211312113221133211322112211213322112", "Decays into": ["Ge", "Ca", "Li"], "Abundance": 2263.8860325},
    "B": {"Sequence": "1321132122211322212221121123222112", "Decays into": ["Be"], "Abundance": 2951.1503716},
    "C": {"Sequence": "3113112211322112211213322112", "Decays into": ["B"], "Abundance": 3847.0525419},
    "N": {"Sequence": "111312212221121123222112", "Decays into": ["C"], "Abundance": 5014.9302464},
    "O": {"Sequence": "132112211213322112", "Decays into": ["N"], "Abundance": 6537.3490750},
    "F": {"Sequence": "31121123222112", "Decays into": ["O"], "Abundance": 8521.9396539},
    "Ne": {"Sequence": "111213322112", "Decays into": ["F"], "Abundance": 11109.006696},
    "Na": {"Sequence": "123222112", "Decays into": ["Ne"], "Abundance": 14481.448773},
    "Mg": {"Sequence": "3113322112", "Decays into": ["Pm", "Na"], "Abundance": 18850.441228},
    "Al": {"Sequence": "1113222112", "Decays into": ["Mg"], "Abundance": 24573.006696},
    "Si": {"Sequence": "1322112", "Decays into": ["Al"], "Abundance": 32032.812960},
    "P": {"Sequence": "311311222112", "Decays into": ["Ho", "Si"], "Abundance": 14895.886658},
    "S": {"Sequence": "1113122112", "Decays into": ["P"], "Abundance": 19417.939250},
    "Cl": {"Sequence": "132112", "Decays into": ["S"], "Abundance": 25312.784218},
    "Ar": {"Sequence": "3112", "Decays into": ["Cl"], "Abundance": 32997.170122},
    "K": {"Sequence": "1112", "Decays into": ["Ar"], "Abundance": 43014.360913},
    "Ca": {"Sequence": "12", "Decays into": ["K"], "Abundance": 56072.543129},
    "Sc": {"Sequence": "3113112221133112", "Decays into": ["Ho", "Pa", "H", "Ca", "Co"], "Abundance": 9302.0974443},
    "Ti": {"Sequence": "11131221131112", "Decays into": ["Sc"], "Abundance": 12126.002783},
    "V": {"Sequence": "13211312", "Decays into": ["Ti"], "Abundance": 15807.181592},
    "Cr": {"Sequence": "31132", "Decays into": ["V"], "Abundance": 20605.882611},
    "Mn": {"Sequence": "111311222112", "Decays into": ["Cr", "Si"], "Abundance": 26861.360180},
    "Fe": {"Sequence": "13122112", "Decays into": ["Mn"], "Abundance": 35015.858546},
    "Co": {"Sequence": "32112", "Decays into": ["Fe"], "Abundance": 45645.877256},
    "Ni": {"Sequence": "11133112", "Decays into": ["Zn", "Co"], "Abundance": 13871.123200},
    "Cu": {"Sequence": "131112", "Decays into": ["Ni"], "Abundance": 18082.082203},
    "Zn": {"Sequence": "312", "Decays into": ["Cu"], "Abundance": 23571.391336},
    "Ga": {"Sequence": "13221133122211332", "Decays into": ["Eu", "Ca", "Ac", "H", "Ca", "Zn"], "Abundance": 1447.8905642},
    "Ge": {"Sequence": "31131122211311122113222", "Decays into": ["Ho", "Ga"], "Abundance": 1887.4372276},
    "As": {"Sequence": "11131221131211322113322112", "Decays into": ["Ge", "Na"], "Abundance": 27.246216076},
    "Se": {"Sequence": "13211321222113222112", "Decays into": ["As"], "Abundance": 35.517547944},
    "Br": {"Sequence": "3113112211322112", "Decays into": ["Se"], "Abundance": 46.299868152},
    "Kr": {"Sequence": "11131221222112", "Decays into": ["Br"], "Abundance": 60.355455682},
    "Rb": {"Sequence": "1321122112", "Decays into": ["Kr"], "Abundance": 78.678000089},
    "Sr": {"Sequence": "3112112", "Decays into": ["Rb"], "Abundance": 102.56285249},
    "Y": {"Sequence": "1112133", "Decays into": ["Sr", "U"], "Abundance": 133.69860315},
    "Zr": {"Sequence": "12322211331222113112211", "Decays into": ["Y", "H", "Ca", "Tc"], "Abundance": 174.28645997},
    "Nb": {"Sequence": "1113122113322113111221131221", "Decays into": ["Er", "Zr"], "Abundance": 227.19586752},
    "Mo": {"Sequence": "13211322211312113211", "Decays into": ["Nb"], "Abundance": 296.16736852},
    "Tc": {"Sequence": "311322113212221", "Decays into": ["Mo"], "Abundance": 386.07704943},
    "Ru": {"Sequence": "132211331222113112211", "Decays into": ["Eu", "Ca", "Tc"], "Abundance": 328.99480576},
    "Rh": {"Sequence": "311311222113111221131221", "Decays into": ["Ho", "Ru"], "Abundance": 428.87015041},
    "Pd": {"Sequence": "111312211312113211", "Decays into": ["Rh"], "Abundance": 559.06537946},
    "Ag": {"Sequence": "132113212221", "Decays into": ["Pd"], "Abundance": 728.78492056},
    "Cd": {"Sequence": "3113112211", "Decays into": ["Ag"], "Abundance": 950.02745646},
    "In": {"Sequence": "11131221", "Decays into": ["Cd"], "Abundance": 1238.4341972},
    "Sn": {"Sequence": "13211", "Decays into": ["In"], "Abundance": 1614.3946687},
    "Sb": {"Sequence": "3112221", "Decays into": ["Pm", "Sn"], "Abundance": 2104.4881933},
    "Te": {"Sequence": "1322113312211", "Decays into": ["Eu", "Ca", "Sb"], "Abundance": 2743.3629718},
    "I": {"Sequence": "311311222113111221", "Decays into": ["Ho", "Te"], "Abundance": 3576.1856107},
    "Xe": {"Sequence": "11131221131211", "Decays into": ["I"], "Abundance": 4661.8342720},
    "Cs": {"Sequence": "13211321", "Decays into": ["Xe"], "Abundance": 6077.0611889},
    "Ba": {"Sequence": "311311", "Decays into": ["Cs"], "Abundance": 7921.9188284},
    "La": {"Sequence": "11131", "Decays into": ["Ba"], "Abundance": 10326.833312},
    "Ce": {"Sequence": "1321133112", "Decays into": ["La", "H", "Ca", "Co"], "Abundance": 13461.825166},
    "Pr": {"Sequence": "31131112", "Decays into": ["Ce"], "Abundance": 17548.529287},
    "Nd": {"Sequence": "111312", "Decays into": ["Pr"], "Abundance": 22875.863883},
    "Pm": {"Sequence": "132", "Decays into": ["Nd"], "Abundance": 29820.456167},
    "Sm": {"Sequence": "311332", "Decays into": ["Pm", "Ca", "Zn"], "Abundance": 15408.115182},
    "Eu": {"Sequence": "1113222", "Decays into": ["Sm"], "Abundance": 20085.668709},
    "Gd": {"Sequence": "13221133112", "Decays into": ["Eu", "Ca", "Co"], "Abundance": 21662.972821},
    "Tb": {"Sequence": "3113112221131112", "Decays into": ["Ho", "Gd"], "Abundance": 28239.358949},
    "Dy": {"Sequence": "111312211312", "Decays into": ["Tb"], "Abundance": 36812.186418},
    "Ho": {"Sequence": "1321132", "Decays into": ["Dy"], "Abundance": 47987.529438},
    "Er": {"Sequence": "311311222", "Decays into": ["Ho", "Pm"], "Abundance": 1098.5955997},
    "Tm": {"Sequence": "11131221133112", "Decays into": ["Er", "Ca", "Co"], "Abundance": 1204.9083841},
    "Yb": {"Sequence": "1321131112", "Decays into": ["Tm"], "Abundance": 1570.6911808},
    "Lu": {"Sequence": "311312", "Decays into": ["Yb"], "Abundance": 2047.5173200},
    "Hf": {"Sequence": "11132", "Decays into": ["Lu"], "Abundance": 2669.0970363},
    "Ta": {"Sequence": "13112221133211322112211213322113", "Decays into": ["Hf", "Pa", "H", "Ca", "W"], "Abundance": 242.07736666},
    "W": {"Sequence": "312211322212221121123222113", "Decays into": ["Ta"], "Abundance": 315.56655252},
    "Re": {"Sequence": "111312211312113221133211322112211213322113", "Decays into": ["Ge", "Ca", "W"], "Abundance": 169.28801808},
    "Os": {"Sequence": "1321132122211322212221121123222113", "Decays into": ["Re"], "Abundance": 220.68001229},
    "Ir": {"Sequence": "3113112211322112211213322113", "Decays into": ["Os"], "Abundance": 287.67344775},
    "Pt": {"Sequence": "111312212221121123222113", "Decays into": ["Ir"], "Abundance": 375.00456738},
    "Au": {"Sequence": "132112211213322113", "Decays into": ["Pt"], "Abundance": 488.84742982},
    "Hg": {"Sequence": "31121123222113", "Decays into": ["Au"], "Abundance": 637.25039755},
    "Tl": {"Sequence": "111213322113", "Decays into": ["Hg"], "Abundance": 830.70513293},
    "Pb": {"Sequence": "123222113", "Decays into": ["Tl"], "Abundance": 1082.8883285},
    "Bi": {"Sequence": "3113322113", "Decays into": ["Pm", "Pb"], "Abundance": 1411.6286100},
    "Po": {"Sequence": "1113222113", "Decays into": ["Bi"], "Abundance": 1840.1669683},
    "At": {"Sequence": "1322113", "Decays into": ["Po"], "Abundance": 2398.7998311},
    "Rn": {"Sequence": "311311222113", "Decays into": ["Ho", "At"], "Abundance": 3127.0209328},
    "Fr": {"Sequence": "1113122113", "Decays into": ["Rn"], "Abundance": 4076.3134078},
    "Ra": {"Sequence": "132113", "Decays into": ["Fr"], "Abundance": 5313.7894999},
    "Ac": {"Sequence": "3113", "Decays into": ["Ra"], "Abundance": 6926.9352045},
    "Th": {"Sequence": "1113", "Decays into": ["Ac"], "Abundance": 7581.9047125},
    "Pa": {"Sequence": "13", "Decays into": ["Th"], "Abundance": 9883.5986392},
    "U": {"Sequence": "3", "Decays into": ["Pa"], "Abundance": 102.56285249}
}


start = ["Bi"] # conway 83 Bi
sequence = start

for i in range(50):
    next_sequence = []
    for element in sequence:
        next_sequence += elements[element]["Decays into"]

    sequence = next_sequence

print(len(sequence))

total = 0
for element in sequence:
    total += len(elements[element]["Sequence"])

print(total)

