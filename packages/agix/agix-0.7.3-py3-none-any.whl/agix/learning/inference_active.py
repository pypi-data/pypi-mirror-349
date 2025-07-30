# src/agix/learning/inference_active.py

import numpy as np


class ActiveInferenceAgent:
    """
    Agente que utiliza inferencia activa para minimizar la entropía de creencias
    sobre el entorno y sus estados internos.
    """

    def __init__(self, action_space, state_space, prior_beliefs=None):
        self.action_space = action_space
        self.state_space = state_space
        self.beliefs = prior_beliefs if prior_beliefs is not None else np.ones(len(state_space)) / len(state_space)

    def update_beliefs(self, observation):
        """
        Actualiza las creencias según la nueva observación.
        Esta implementación usa una regla de actualización bayesiana simple.
        """
        likelihood = self.compute_likelihood(observation)
        self.beliefs *= likelihood
        self.beliefs /= np.sum(self.beliefs)  # Normalizar

    def compute_likelihood(self, observation):
        """
        Calcula la verosimilitud de cada estado dado una observación.
        Este método debe ser sobrescrito por subclases específicas.
        """
        raise NotImplementedError("Debe implementarse compute_likelihood().")

    def select_action(self):
        """
        Selecciona una acción que minimice la incertidumbre esperada.
        Por defecto, elige aleatoriamente.
        """
        return np.random.choice(self.action_space)
