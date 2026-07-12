from abc import ABC, abstractmethod


class EstadisticasStrategy(ABC):
    """Interfaz (Strategy) para el cálculo de puntos según posición del jugador.

    Define el contrato que deben cumplir todas las estrategias concretas de
    cálculo de rendimiento (Portero, Defensa, Medio, Delantero), permitiendo
    que `Rendimiento` calcule los puntos sin conocer la lógica particular de
    cada posición (Polimorfismo vía patrón Strategy).
    """
    @abstractmethod
    def calcular_puntos(self):
        """Calcula los puntos obtenidos según las estadísticas del jugador
        en el partido. Cada posición implementa su propia fórmula de
        puntuación.

        Returns:
            float: Puntos calculados.
        """
        pass
    @abstractmethod
    def obtener_estadisticas(self):
        """Obtiene las estadísticas crudas utilizadas para el cálculo de puntos.

        Returns:
            dict: Estadísticas específicas de la posición.
        """
        pass

    