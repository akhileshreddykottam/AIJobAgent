import unittest

from jobs import jobs, job_locations


class JobCatalogTests(unittest.TestCase):
    def test_job_locations_accepts_a_string_or_a_list(self):
        self.assertEqual(job_locations({"location": "Oslo"}), ["Oslo"])
        self.assertEqual(job_locations({"location": ["Oslo", " Bergen ", ""]}), ["Oslo", "Bergen"])
        self.assertEqual(job_locations({}), [])

    def test_some_jobs_are_advertised_in_multiple_locations(self):
        self.assertTrue(any(len(job_locations(job)) > 1 for job in jobs))

    def test_catalog_has_a_broad_collection_of_valid_sample_jobs(self):
        self.assertGreaterEqual(len(jobs), 50)

        records = set()
        locations = set()
        titles = set()

        for job in jobs:
            self.assertTrue({"title", "company", "location", "skills"}.issubset(job))
            self.assertTrue(all(isinstance(job[field], str) and job[field].strip()
                                for field in ("title", "company")))
            self.assertTrue(job_locations(job))
            self.assertEqual(len(set(job_locations(job))), len(job_locations(job)))
            self.assertIsInstance(job["skills"], list)
            self.assertTrue(job["skills"])
            self.assertTrue(all(isinstance(skill, str) and skill.strip() for skill in job["skills"]))
            self.assertEqual(len({skill.strip().casefold() for skill in job["skills"]}), len(job["skills"]))
            self.assertIsInstance(job["interests"], list)
            self.assertTrue(job["interests"])
            self.assertTrue(all(isinstance(interest, str) and interest.strip()
                                for interest in job["interests"]))

            record = (
                job["title"],
                job["company"],
                tuple(job_locations(job)),
                tuple(job["skills"]),
                tuple(job["interests"]),
            )
            self.assertNotIn(record, records)
            records.add(record)
            locations.update(job_locations(job))
            titles.add(job["title"])

        self.assertGreaterEqual(len(locations), 10)
        self.assertGreaterEqual(len(titles), 30)


if __name__ == "__main__":
    unittest.main()
