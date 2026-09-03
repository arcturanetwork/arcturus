import unittest
from capstone.agent.orchestration import AgentMessage, AgentRole, Feedback, FeedbackStore, MessageKind, OrchestrationError, Orchestrator

def researcher(message):
    return AgentMessage.create("researcher","verifier",MessageKind.RESULT,{"sources":["urn:source:1"]},
                               message.remaining_hops-1,message.correlation_id)
def verifier(_message): return None

class OrchestrationTests(unittest.TestCase):
    def setUp(self):
        self.system = Orchestrator([AgentRole("researcher",frozenset({MessageKind.TASK}),researcher),
                                    AgentRole("verifier",frozenset({MessageKind.RESULT}),verifier)])
    def test_typed_route_preserves_correlation_and_decrements_budget(self):
        initial = AgentMessage.create("orchestrator","researcher",MessageKind.TASK,{"query":"x"},3)
        transcript = self.system.route(initial)
        self.assertEqual(len(transcript),2); self.assertEqual(transcript[0].correlation_id,transcript[1].correlation_id)
        self.assertEqual(transcript[1].remaining_hops,2)
    def test_unaccepted_message_kind_is_rejected(self):
        with self.assertRaises(OrchestrationError):
            self.system.route(AgentMessage.create("x","researcher",MessageKind.APPROVAL_REQUEST,{},2))
    def test_non_decreasing_budget_is_rejected(self):
        def bad(message): return AgentMessage.create("bad","verifier",MessageKind.RESULT,{},message.remaining_hops,message.correlation_id)
        system = Orchestrator([AgentRole("bad",frozenset({MessageKind.TASK}),bad),AgentRole("verifier",frozenset({MessageKind.RESULT}),verifier)])
        with self.assertRaisesRegex(OrchestrationError,"did not decrease"):
            system.route(AgentMessage.create("x","bad",MessageKind.TASK,{},2))
    def test_feedback_is_structured_and_aggregated(self):
        store = FeedbackStore(); store.add(Feedback("case-1","human-1",4,"groundedness","good citation")); store.add(Feedback("case-2","human-2",2,"groundedness","weak source"))
        self.assertEqual(store.summary()["groundedness"],3)
        with self.assertRaises(ValueError): store.add(Feedback("case-3","human",8,"safety","bad scale"))

if __name__ == "__main__": unittest.main()

