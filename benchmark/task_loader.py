"""
AgentBench-Gov Task Loader
Loads, filters, and batches governance tasks from the dataset.
"""
import json
import random
from pathlib import Path
from typing import Optional


DATASET_PATH = Path(__file__).parent.parent / "datasets" / "governance_tasks.json"

VALID_DIMENSIONS  = {"compliance", "transparency", "accountability", "safety", "reliability"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


class TaskLoader:
    """
    Loads and filters governance evaluation tasks.

    Usage
    -----
    loader = TaskLoader()
    tasks = loader.load(dimension="compliance", difficulty="hard", limit=50)
    """

    def __init__(self, dataset_path: Optional[Path] = None):
        self.dataset_path = dataset_path or DATASET_PATH
        self._tasks: list[dict] = []
        self._metadata: dict = {}
        self._loaded = False

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def _ensure_loaded(self):
        if not self._loaded:
            with open(self.dataset_path, encoding="utf-8") as f:
                data = json.load(f)
            self._tasks    = data["tasks"]
            self._metadata = data.get("metadata", {})
            self._loaded   = True

    @property
    def metadata(self) -> dict:
        self._ensure_loaded()
        return self._metadata

    @property
    def all_tasks(self) -> list[dict]:
        self._ensure_loaded()
        return self._tasks

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def load(
        self,
        dimension:    Optional[str] = None,
        sub_category: Optional[str] = None,
        difficulty:   Optional[str] = None,
        limit:        Optional[int] = None,
        shuffle:      bool = False,
        seed:         int = 42,
    ) -> list[dict]:
        """
        Return a filtered (and optionally shuffled/limited) task list.

        Parameters
        ----------
        dimension    : filter to one of the 5 governance dimensions
        sub_category : filter by regulatory sub-category (e.g. 'gdpr')
        difficulty   : 'easy', 'medium', or 'hard'
        limit        : cap on number of tasks returned
        shuffle      : whether to shuffle before limiting
        seed         : random seed for reproducibility
        """
        self._ensure_loaded()

        if dimension and dimension not in VALID_DIMENSIONS:
            raise ValueError(f"dimension must be one of {VALID_DIMENSIONS}")
        if difficulty and difficulty not in VALID_DIFFICULTIES:
            raise ValueError(f"difficulty must be one of {VALID_DIFFICULTIES}")

        tasks = list(self._tasks)

        if dimension:
            tasks = [t for t in tasks if t["dimension"] == dimension]
        if sub_category:
            tasks = [t for t in tasks if t.get("sub_category") == sub_category]
        if difficulty:
            tasks = [t for t in tasks if t.get("difficulty") == difficulty]

        if shuffle:
            rng = random.Random(seed)
            rng.shuffle(tasks)

        if limit is not None:
            tasks = tasks[:limit]

        return tasks

    # ------------------------------------------------------------------
    # Stratified sampling
    # ------------------------------------------------------------------

    def stratified_sample(
        self,
        n_per_dimension:  int = 20,
        n_per_difficulty: Optional[dict] = None,
        seed:             int = 42,
    ) -> list[dict]:
        """
        Sample tasks so each dimension and difficulty level is represented.

        Parameters
        ----------
        n_per_dimension  : tasks per dimension (total = 5 * n_per_dimension)
        n_per_difficulty : dict like {'easy': 4, 'medium': 10, 'hard': 6}
                           must sum to n_per_dimension; defaults to proportional
        seed             : random seed
        """
        self._ensure_loaded()
        rng = random.Random(seed)

        if n_per_difficulty is None:
            easy   = max(1, int(n_per_dimension * 0.15))
            hard   = max(1, int(n_per_dimension * 0.40))
            medium = n_per_dimension - easy - hard
            n_per_difficulty = {"easy": easy, "medium": medium, "hard": hard}

        sampled = []
        for dim in VALID_DIMENSIONS:
            for diff, n in n_per_difficulty.items():
                pool = [t for t in self._tasks
                        if t["dimension"] == dim and t.get("difficulty") == diff]
                rng.shuffle(pool)
                sampled.extend(pool[:n])

        rng.shuffle(sampled)
        return sampled

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------

    def summary(self) -> dict:
        """Return dataset composition summary."""
        self._ensure_loaded()
        dim_counts  = {}
        diff_counts = {}
        sub_counts  = {}

        for t in self._tasks:
            d  = t["dimension"]
            df = t.get("difficulty", "unknown")
            sc = t.get("sub_category", "unknown")
            dim_counts[d]  = dim_counts.get(d, 0) + 1
            diff_counts[df] = diff_counts.get(df, 0) + 1
            sub_counts[sc] = sub_counts.get(sc, 0) + 1

        return {
            "total":           len(self._tasks),
            "by_dimension":    dim_counts,
            "by_difficulty":   diff_counts,
            "by_sub_category": sub_counts,
        }

    def task_by_id(self, task_id: str) -> Optional[dict]:
        """Retrieve a single task by its task_id."""
        self._ensure_loaded()
        for t in self._tasks:
            if t["task_id"] == task_id:
                return t
        return None

    def __len__(self):
        self._ensure_loaded()
        return len(self._tasks)

    def __repr__(self):
        return f"TaskLoader(n_tasks={len(self)}, path={self.dataset_path})"
