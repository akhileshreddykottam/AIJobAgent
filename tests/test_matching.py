import unittest

from matching import calculate_match, match_breakdown, matched_skills, missing_skills


class MatchingTests(unittest.TestCase):
    def test_matching_is_case_insensitive_and_deduplicates_skills(self):
        user_skills = [" Python ", "python", "COMMUNICATION"]
        job_skills = ["python", "communication", "python"]

        self.assertEqual(calculate_match(user_skills, job_skills), 100)
        self.assertEqual(
            matched_skills(user_skills, job_skills),
            ["python", "communication"],
        )
        self.assertEqual(missing_skills(user_skills, job_skills), [])

    def test_missing_skills_are_normalized(self):
        self.assertEqual(
            missing_skills(["python"], [" Python ", "SQL"]),
            ["sql"],
        )

    def test_empty_requirements_have_zero_match(self):
        self.assertEqual(calculate_match(["python"], []), 0)
        self.assertEqual(matched_skills(["python"], []), [])
        self.assertEqual(missing_skills(["python"], []), [])

    def test_exact_skill_and_interest_matches_receive_full_credit(self):
        self.assertEqual(
            calculate_match(["python"], ["python"], ["design"], ["design"]),
            100,
        )

    def test_cross_category_matches_receive_no_credit(self):
        self.assertEqual(
            calculate_match([], ["python"], ["python"], []),
            0,
        )
        self.assertEqual(
            calculate_match(["design"], [], [], ["design"]),
            0,
        )

    def test_direct_and_cross_category_matches_only_credit_direct_matches(self):
        self.assertEqual(
            calculate_match(
                ["leadership", "communication"],
                ["python", "leadership"],
                ["design", "python"],
                ["design", "communication"],
            ),
            50,
        )

    def test_best_category_match_is_counted_once(self):
        breakdown = match_breakdown(
            ["python"],
            ["python"],
            ["python"],
            ["python"],
        )

        self.assertEqual(breakdown["score"], 100)
        self.assertEqual(breakdown["matched_skills"], ["python"])
        self.assertEqual(breakdown["matched_interests"], ["python"])

        direct_skill_match = match_breakdown(
            ["python"],
            ["python"],
            [],
            ["python"],
        )
        self.assertEqual(direct_skill_match["score"], 100)
        self.assertEqual(direct_skill_match["matched_skills"], ["python"])

        direct_interest_match = match_breakdown(
            [],
            ["python"],
            ["python"],
            ["python"],
        )
        self.assertEqual(direct_interest_match["score"], 100)
        self.assertEqual(direct_interest_match["matched_interests"], ["python"])

    def test_missing_skills_remain_missing_when_they_only_match_as_interests(self):
        breakdown = match_breakdown([], ["python"], ["python"], [])

        self.assertEqual(breakdown["score"], 0)
        self.assertEqual(breakdown["missing_skills"], ["python"])

    def test_interest_matching_job_skill_does_not_count_as_skill_or_match(self):
        breakdown = match_breakdown([], ["python"], ["python"], ["python"])

        self.assertEqual(breakdown["score"], 100)
        self.assertEqual(breakdown["matched_skills"], [])
        self.assertEqual(breakdown["matched_interests"], ["python"])
        self.assertEqual(breakdown["missing_skills"], ["python"])

    def test_duplicate_terms_are_counted_once_across_job_categories(self):
        self.assertEqual(
            calculate_match(
                ["python"],
                ["python", "python"],
                ["python"],
                ["python"],
            ),
            100,
        )

    def test_old_skill_only_call_remains_supported(self):
        self.assertEqual(calculate_match(["python"], ["python", "sql"]), 50)


if __name__ == "__main__":
    unittest.main()