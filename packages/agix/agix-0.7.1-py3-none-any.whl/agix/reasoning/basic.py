class Reasoner:
    def select_best_model(self, evaluations):
        if not evaluations:
            return {
                "name": None,
                "accuracy": 0.0,
                "reason": "No se proporcionaron modelos para evaluar."
            }

        # Ordenar por precisión
        evaluations_sorted = sorted(evaluations, key=lambda m: m["accuracy"], reverse=True)
        best = evaluations_sorted[0]

        # Buscar modelos dentro de un 2% de la mejor precisión
        threshold = best["accuracy"] - 0.02
        candidates = [m for m in evaluations_sorted if m["accuracy"] >= threshold]

        # Dentro de los candidatos, elegir el más interpretable
        final = sorted(candidates, key=lambda m: m["interpretability"], reverse=True)[0]

        reason = (
            f"El modelo '{final['name']}' fue seleccionado porque obtuvo una precisión de "
            f"{final['accuracy']:.2f} y tiene un buen nivel de interpretabilidad "
            f"({final['interpretability']:.2f})."
        )

        return {
            "name": final["name"],
            "accuracy": final["accuracy"],
            "reason": reason
        }
