from typing import Tuple
import warnings


class BaseDataTest:
    """
    Base class for Bayesian A/B test.
    """

    def __init__(self) -> None:
        """
        Initialize BaseDataTest class.
        """
        self.data = {}

    @property
    def variant_names(self):
        return [k for k in self.data]

    def eval_simulation(
        self,
        sim_count: int = 20000,
        seed: int = None,
        min_is_best: bool = False,
        interval_alpha: float = 0.95,
    ) -> Tuple[dict, dict, dict]:
        """
        Should be implemented in each individual experiment.
        """
        raise NotImplementedError

    def probabs_of_being_best(
        self,
        sim_count: int = 20000,
        seed: int = None,
        min_is_best: bool = False,
        interval_alpha: float = 0.95,
    ) -> dict:
        """
        Calculate probabilities of being best for a current class state.

        Parameters
        ----------
        sim_count : Number of simulations to be used for probability estimation.
        seed : Random seed.
        min_is_best : Option to change "being best" to a minimum. Default is maximum.
        interval_alpha : Credible interval probability (value between 0 and 1).

        Returns
        -------
        pbbs : Dictionary with probabilities of being best for all variants in experiment.
        """
        pbbs, loss, intervals = self.eval_simulation(sim_count, seed, min_is_best, interval_alpha)

        return pbbs

    def expected_loss(
        self,
        sim_count: int = 20000,
        seed: int = None,
        min_is_best: bool = False,
        interval_alpha: float = 0.95,
    ) -> dict:
        """
        Calculate expected loss for a current class state.

        Parameters
        ----------
        sim_count : Number of simulations to be used for probability estimation.
        seed : Random seed.
        min_is_best : Option to change "being best" to a minimum. Default is maximum.
        interval_alpha : Credible interval probability (value between 0 and 1).

        Returns
        -------
        loss : Dictionary with expected loss for all variants in experiment.
        """
        pbbs, loss, intervals = self.eval_simulation(sim_count, seed, min_is_best, interval_alpha)

        return loss

    def credible_intervals(
        self,
        sim_count: int = 20000,
        seed: int = None,
        min_is_best: bool = False,
        interval_alpha: float = 0.95,
    ) -> dict:
        """
        Calculate quantile-based credible intervals for a current class state.

        Parameters
        ----------
        sim_count : Number of simulations to be used for probability estimation.
        seed : Random seed.
        min_is_best : Option to change "being best" to a minimum. Default is maximum.
        interval_alpha : Credible interval probability (value between 0 and 1).

        Returns
        -------
        intervals : Dictionary with quantile-based credible intervals for all variants.
        """
        pbbs, loss, intervals = self.eval_simulation(sim_count, seed, min_is_best, interval_alpha)

        return intervals

    def delete_variant(self, name: str) -> None:
        """
        Delete variant and all its data from experiment.

        Parameters
        ----------
        name : Variant name.
        """
        if not isinstance(name, str):
            raise ValueError("Variant name has to be a string.")
        if name not in self.variant_names:
            warnings.warn(f"Nothing to be deleted. Variant {name} is not in experiment.")
        else:
            del self.data[name]
