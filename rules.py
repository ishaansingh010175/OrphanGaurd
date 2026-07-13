from models import OrphanResource


class RuleEngine:
    """
    Applies deterministic rules to determine whether a resource
    should be considered an orphan candidate.
    """

    def __init__(self, min_age_days: int = 7):
        self.min_age_days = min_age_days

    def evaluate(self, resources: list[OrphanResource]) -> list[OrphanResource]:
        """
        Evaluate all resources.

        Returns only the resources that pass our orphan rules.
        """

        candidates = []

        for resource in resources:

            # Rule 1
            # Ignore very new resources
            if resource.age_days < self.min_age_days:
                continue

            # Rule 2
            # Skip resources that still have an owner
            if resource.owner:
                continue

            # Rule 3
            # Skip resources still referenced
            if resource.used_by:
                continue

            # Rule 4
            # Candidate for AI review
            resource.can_delete = True

            candidates.append(resource)

        return candidates