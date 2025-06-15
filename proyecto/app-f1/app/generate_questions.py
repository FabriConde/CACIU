import random

def generate_questions(all_questions, nivel, piloto, equipo, num_total=10):
    def relacionadas_con_piloto_equipo(q):
        return q.get("piloto") == piloto or q.get("equipo") == equipo

    relacionadas = [q for q in all_questions if relacionadas_con_piloto_equipo(q)]
    nivel_match = [q for q in all_questions if q.get("nivel") == nivel]
    
    match nivel:
        case "Principiante":
            random.shuffle(relacionadas)
            seleccionadas = relacionadas[:num_total]

            if len(seleccionadas) < num_total:
                faltantes = num_total - len(seleccionadas)
                restantes = [q for q in all_questions if q not in seleccionadas]
                random.shuffle(restantes)
                seleccionadas += restantes[:faltantes]

        case "Intermedio":
            num_rel = int(num_total * 0.6)
            num_nivel = num_total - num_rel

            random.shuffle(relacionadas)
            seleccionadas_rel = relacionadas[:num_rel]

            restantes = [q for q in all_questions if q not in seleccionadas_rel]
            nivel_match = [q for q in restantes if q.get("nivel") == nivel]
            random.shuffle(nivel_match)
            seleccionadas_nivel = nivel_match[:num_nivel]

            faltan_rel = num_rel - len(seleccionadas_rel)
            if faltan_rel > 0:
                extra_nivel = nivel_match[num_nivel:num_nivel + faltan_rel]
                seleccionadas_nivel += extra_nivel

            seleccionadas = seleccionadas_rel + seleccionadas_nivel

            if len(seleccionadas) < num_total:
                restantes_final = [q for q in all_questions if q not in seleccionadas]
                random.shuffle(restantes_final)
                seleccionadas += restantes_final[:num_total - len(seleccionadas)]

        case "Avanzado":
            num_rel = int(num_total * 0.3)
            num_nivel = num_total - num_rel

            random.shuffle(relacionadas)
            seleccionadas_rel = relacionadas[:num_rel]

            restantes = [q for q in all_questions if q not in seleccionadas_rel]
            nivel_match = [q for q in restantes if q.get("nivel") == nivel]
            random.shuffle(nivel_match)
            seleccionadas_nivel = nivel_match[:num_nivel]

            faltan_rel = num_rel - len(seleccionadas_rel)
            if faltan_rel > 0:
                extra_nivel = nivel_match[num_nivel:num_nivel + faltan_rel]
                seleccionadas_nivel += extra_nivel

            seleccionadas = seleccionadas_rel + seleccionadas_nivel

            if len(seleccionadas) < num_total:
                restantes_final = [q for q in all_questions if q not in seleccionadas]
                random.shuffle(restantes_final)
                seleccionadas += restantes_final[:num_total - len(seleccionadas)]

        case "Experto":
            seleccionadas = random.sample(all_questions, min(num_total, len(all_questions)))

        case _:
            seleccionadas = random.sample(all_questions, min(num_total, len(all_questions)))

    random.shuffle(seleccionadas)
    return seleccionadas
