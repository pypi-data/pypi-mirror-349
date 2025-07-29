# agix/reasoning/basic.py

class Reasoner:
    def select_best_model(self, evaluations):
        if not evaluations:
            return {
                "name": None,
                "accuracy": 0.0,
                "reason": "No se proporcionaron modelos para evaluar."
            }

        best = sorted(evaluations, key=lambda m: m["accuracy"], reverse=True)[0]

        reason = (
            f"El modelo '{best['name']}' fue seleccionado porque obtuvo la mayor precisión "
            f"({best['accuracy']:.2f}) entre los modelos evaluados."
        )

        return {
            "name": best["name"],
            "accuracy": best["accuracy"],
            "reason": reason
        }
