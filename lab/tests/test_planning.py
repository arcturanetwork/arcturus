import unittest

from capstone.agent.planning import Task, evaluate_plan, fixed_workflow, flexible_planner


class PlanningTests(unittest.TestCase):
    def test_both_approaches_cover_known_publish_task(self):
        task = Task("publish", True, True)
        self.assertTrue(evaluate_plan(task, fixed_workflow(task))["success"])
        self.assertTrue(evaluate_plan(task, flexible_planner(task))["success"])

    def test_workflow_verifies_while_planner_synthesizes(self):
        task = Task("summarize", True, False)
        fixed_plan = fixed_workflow(task)
        flexible_plan = flexible_planner(task)
        self.assertIn("verify_sources", fixed_plan)
        self.assertNotIn("verify_sources", flexible_plan)
        self.assertIn("synthesize", flexible_plan)

    def test_planner_handles_ambiguous_intent_without_writing(self):
        task = Task("ambiguous", False, False)
        result = evaluate_plan(task, flexible_planner(task))
        self.assertTrue(result["success"])
        self.assertFalse(result["unauthorized_write"])


if __name__ == "__main__":
    unittest.main()
