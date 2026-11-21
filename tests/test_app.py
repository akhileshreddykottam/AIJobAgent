import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from google.genai.errors import APIError
from streamlit.testing.v1 import AppTest

from jobs import jobs, job_locations

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    @staticmethod
    def run_app(*, name="Sam", location=None, skills=(), interests=()):
        app = AppTest.from_file(str(APP_PATH)).run()
        app.text_input[0].set_value(name)
        if location is not None:
            app.selectbox[0].set_value(location)
        app.run()

        if skills:
            app.multiselect[0].set_value(list(skills))
            app.run()
        if interests:
            app.multiselect[1].set_value(list(interests))
        app.button[0].click()
        return app.run()

    def test_location_options_only_contain_catalog_locations(self):
        app = AppTest.from_file(str(APP_PATH)).run()

        expected_locations = sorted(
            {location for job in jobs for location in job_locations(job)},
            key=str.casefold,
        )
        self.assertEqual(app.selectbox[0].options, expected_locations)

    def test_skills_are_filtered_by_selected_location(self):
        app = AppTest.from_file(str(APP_PATH)).run()
        app.selectbox[0].set_value("Oslo")
        app.run()

        oslo_skills = sorted({
            skill
            for job in jobs
            if "Oslo" in job_locations(job)
            for skill in job["skills"]
        }, key=str.casefold)
        self.assertEqual(app.multiselect[0].options, oslo_skills)

        app.selectbox[0].set_value("Bergen")
        app.run()
        bergen_skills = sorted({
            skill
            for job in jobs
            if "Bergen" in job_locations(job)
            for skill in job["skills"]
        }, key=str.casefold)
        self.assertEqual(app.multiselect[0].options, bergen_skills)

    def test_interests_are_filtered_by_location_and_selected_skills(self):
        app = AppTest.from_file(str(APP_PATH)).run()
        app.selectbox[0].set_value("Oslo")
        app.run()
        app.multiselect[0].set_value(["python"])
        app.run()

        expected_interests = sorted({
            interest
            for job in jobs
            if "Oslo" in job_locations(job) and "python" in job["skills"]
            for interest in job["interests"]
        }, key=str.casefold)
        self.assertEqual(app.multiselect[1].options, expected_interests)

    def test_multiple_skills_include_interests_from_each_matching_job(self):
        app = AppTest.from_file(str(APP_PATH)).run()
        app.selectbox[0].set_value("Oslo")
        app.run()
        app.multiselect[0].set_value(["python", "communication"])
        app.run()

        selected_skills = {"python", "communication"}
        expected_interests = sorted({
            interest
            for job in jobs
            if "Oslo" in job_locations(job)
            and selected_skills.intersection(job["skills"])
            for interest in job["interests"]
        }, key=str.casefold)
        self.assertEqual(app.multiselect[1].options, expected_interests)

    def test_location_change_clears_invalid_skill_and_interest_selections(self):
        app = AppTest.from_file(str(APP_PATH)).run()
        app.selectbox[0].set_value("Oslo")
        app.run()
        app.multiselect[0].set_value(["python"])
        app.run()
        app.multiselect[1].set_value(["data science"])
        app.run()

        app.selectbox[0].set_value("Bergen")
        app.run()

        self.assertEqual(app.multiselect[0].value, [])
        self.assertEqual(app.multiselect[1].value, [])

    def test_skill_change_clears_interests_no_longer_available(self):
        app = AppTest.from_file(str(APP_PATH)).run()
        app.selectbox[0].set_value("Oslo")
        app.run()
        app.multiselect[0].set_value(["python"])
        app.run()
        app.multiselect[1].set_value(["data science"])
        app.run()

        app.multiselect[0].set_value(["communication"])
        app.run()

        self.assertNotIn("data science", app.multiselect[1].options)
        self.assertEqual(app.multiselect[1].value, [])

    def test_location_and_skill_are_required(self):
        app = self.run_app()
        self.assertTrue(any("select a location" in item.value.lower() for item in app.warning))

        app = self.run_app(location="Oslo")
        self.assertTrue(any("select at least one skill" in item.value.lower()
                            for item in app.warning))

    def test_selected_skills_and_interests_drive_results(self):
        with patch("ai_helper.generate_response", return_value="Analysis") as generate_response:
            app = self.run_app(
                location="Oslo",
                skills=("python",),
                interests=("data science",),
            )

        markdown = " ".join(item.value for item in app.markdown)
        self.assertIn("Data Analyst", markdown)
        self.assertIn("Matched Interests", markdown)
        self.assertNotIn("Cross-category matches", markdown)
        prompts = [call.args[0] for call in generate_response.call_args_list]
        self.assertTrue(prompts)
        self.assertTrue(all("Cross-category matches:" not in prompt for prompt in prompts))
        self.assertTrue(all(
            "Match skills only to required skills, and interests only to job interests." in prompt
            for prompt in prompts
        ))

    def test_direct_match_ranks_above_cross_category_match(self):
        with patch("ai_helper.generate_response", return_value="Analysis"):
            app = self.run_app(
                location="Oslo",
                skills=("python",),
                interests=("analytics",),
            )

        markdown = [item.value for item in app.markdown]
        data_analyst_index = next(i for i, value in enumerate(markdown) if "Data Analyst" in value)
        self.assertIn("Data Analyst", markdown[data_analyst_index])
        self.assertNotIn("Digital Marketing Specialist", " ".join(markdown))

    def test_ai_failure_does_not_hide_job_match(self):
        with patch("ai_helper.generate_response", side_effect=RuntimeError("offline")):
            app = self.run_app(location="Oslo", skills=("communication",))

        markdown = " ".join(item.value for item in app.markdown)
        self.assertIn("Store Assistant", markdown)
        self.assertTrue(any("ai analysis is unavailable" in item.value.lower() for item in app.warning))

    def test_ai_failures_show_safe_actionable_diagnostics(self):
        failures = (
            (RuntimeError("missing credential"), "gemini_api_key is not set"),
            (APIError(403, {"error": {"message": "private provider details"}}), "api key or it lacks permission"),
            (APIError(404, {"error": {"message": "private provider details"}}), "configured model"),
            (APIError(429, {"error": {"message": "private provider details"}}), "quota"),
            (APIError(503, {"error": {"message": "private provider details"}}), "temporarily unavailable"),
            (httpx.ConnectError("private provider details"), "network"),
            (ValueError("private provider details"), "unexpected error occurred"),
        )

        for error, expected_message in failures:
            with self.subTest(expected_message=expected_message):
                with patch("ai_helper.generate_response", side_effect=error):
                    app = self.run_app(location="Oslo", skills=("communication",))

                warnings = " ".join(item.value for item in app.warning).lower()
                markdown = " ".join(item.value for item in app.markdown)
                self.assertIn(expected_message, warnings)
                self.assertNotIn("private provider details", warnings)
                self.assertIn("Store Assistant", markdown)


if __name__ == "__main__":
    unittest.main()