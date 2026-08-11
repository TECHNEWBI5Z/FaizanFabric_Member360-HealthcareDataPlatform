# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "14c76d8b-f872-4b9f-a22a-d9e10ddc3c14",
# META       "default_lakehouse_name": "HealthcareLakehouse",
# META       "default_lakehouse_workspace_id": "2b558bb6-aefb-4342-a27b-56457f13dfc0",
# META       "known_lakehouses": [
# META         {
# META           "id": "14c76d8b-f872-4b9f-a22a-d9e10ddc3c14"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# **UnitTesting Frame work**

# CELL ********************

import unittest
from pyspark.sql import functions as F

class TestHealthcareDataQuality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patient = spark.table("silver_patient")
        cls.observation = spark.table("silver_observation")
        cls.condition = spark.table("silver_condition")

    # ---------------------------------------------------
    # Test 1 : Duplicate PatientID
    # ---------------------------------------------------
    def test_duplicate_patient(self):

        duplicate_count = (
            self.patient
            .groupBy("PatientID")
            .count()
            .filter("count > 1")
            .count()
        )

        self.assertEqual(
            duplicate_count,
            0,
            f"Found {duplicate_count} duplicate PatientIDs"
        )

    # ---------------------------------------------------
    # Test 2 : Mandatory Fields
    # ---------------------------------------------------
    def test_patient_mandatory_fields(self):

        missing = (
            self.patient
            .filter("""
                PatientID IS NULL
                OR Gender IS NULL
                OR BirthDate IS NULL
            """)
            .count()
        )

        self.assertEqual(
            missing,
            0,
            f"{missing} records have mandatory fields missing"
        )

    # ---------------------------------------------------
    # Test 3 : Observation Referential Integrity
    # ---------------------------------------------------
    def test_observation_patient_reference(self):

        invalid = (
            self.observation.alias("obs")
            .join(
                self.patient.alias("pat"),
                F.col("obs.PatientID") == F.col("pat.PatientID"),
                "left"
            )
            .filter(F.col("pat.PatientID").isNull())
            .count()
        )

        self.assertEqual(
            invalid,
            0,
            f"{invalid} observations reference invalid patients"
        )

    # ---------------------------------------------------
    # Test 4 : Condition Referential Integrity
    # ---------------------------------------------------
    def test_condition_patient_reference(self):

        invalid = (
            self.condition.alias("con")
            .join(
                self.patient.alias("pat"),
                F.col("con.PatientID") == F.col("pat.PatientID"),
                "left"
            )
            .filter(F.col("pat.PatientID").isNull())
            .count()
        )

        self.assertEqual(
            invalid,
            0,
            f"{invalid} conditions reference invalid patients"
        )


# Execute tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestHealthcareDataQuality)
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Fail notebook if any test failed
if not result.wasSuccessful():
    raise Exception("Data Quality Unit Tests Failed")

print("All Data Quality Unit Tests Passed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Run tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestHealthcareDataQuality)
runner = unittest.TextTestRunner(verbosity=2)

result = runner.run(suite)

# Capture summary
total_tests = result.testsRun
failures = len(result.failures)
errors = len(result.errors)
passed = total_tests - failures - errors

test_summary = {
    "TotalTests": total_tests,
    "Passed": passed,
    "Failures": failures,
    "Errors": errors,
    "Status": "PASS" if result.wasSuccessful() else "FAIL"
}

print(test_summary)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import json
from notebookutils import mssparkutils

mssparkutils.notebook.exit(json.dumps(test_summary))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
