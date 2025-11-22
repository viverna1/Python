aspects = [
    ["Alienis", "Vacous", "Tenebrae"],
    ["Arbor", "Terra", "Herba"],
    ["Auram", "Praecantatio", "Aer"],
    ["Bestia", "Motus", "Victus"],
    ["Cognitio", "Terra", "Spiritus"],
    ["Corpus", "Mortuus", "Bestia"],
    ["Exanimis", "Motus", "Mortuus"],
    ["Fabrico", "Humanus", "Instrumentum"],
    ["Fames", "Victus", "Vacous"],
    ["Granum", "Victus", "Terra"],
    ["Herba", "Granum", "Terra"],
    ["Humanus", "Bestia", "Cognitio"],
    ["Instrumentum", "Humanus", "Ordo"],
    ["Iter", "Motus", "Terra"],
    ["Limus", "Victus", "Aqua"],
    ["Lucrum", "Humanus", "Fames"],
    ["Lux", "Aer", "Fames"],
    ["Machina", "Motus", "Instrumentum"],
    ["Messis", "Granum", "Humanus"],
    ["Metallum", "Saxum", "Ordo"],
    ["Mortuus", "Victus", "Perditio"],
    ["Motus", "Aer", "Ordo"],
    ["Pannus", "Instrumentum", "Bestia"],
    ["Prefodio", "Humanus", "Saxum"],
    ["Permutatio", "Motus", "Aqua"],
    ["Potentia", "Ordo", "Ignis"],
    ["Praecantatio", "Vacous", "Potentia"],
    ["Saxum", "Terra", "Terra"],
    ["Sensus", "Aer", "Spiritus"],
    ["Spiritus", "Victus", "Mortuus"],
    ["Telum", "Instrumentum", "Perditio"],
    ["Tempestas", "Aer", "Aqua"],
    ["Tenebrae", "Vacous", "Lux"],
    ["Tutamen", "Instrumentum", "Terra"],
    ["Vacous", "Aer", "Perditio"],
    ["Venenum", "Aqua", "Mortuus"],
    ["Victus", "Aqua", "Terra"],
    ["Vinculum", "Motus", "Perditio"],
    ["Vitium", "Praecantatio", "Perditio"],
    ["Vitreus", "Saxum", "Aqua"],
    ["Volatus", "Aer", "Motus"],
]


def bold(text: str) -> str:
    return "\033[1m" + text + "\033[0m"


def format_formula(aspects_list: list, necessary_aspects: str) -> str:
    bold_aspect = [bold(aspect) if aspect == necessary_aspects else aspect for aspect in aspects_list]
    return bold_aspect[0] + " = " + bold_aspect[1] + " + " + bold_aspect[2]


while True:
    necessary_aspects = input("Введите аспект: ").capitalize()

    for formula in aspects:
        if necessary_aspects in formula:
            print(format_formula(formula, necessary_aspects))
    print()