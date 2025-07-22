from langgraph.graph import StateGraph, END
from .state import CharacterState
from .nodes.perceive import perceive_node
from .nodes.think import think_node
from .nodes.act import act_node
from .nodes.update_db import update_db_node

workflow = StateGraph(CharacterState)

# Add nodes
workflow.add_node("perceive", perceive_node)
workflow.add_node("think", think_node)
workflow.add_node("act", act_node)
workflow.add_node("update_db", update_db_node)

# Build graph
workflow.set_entry_point("perceive")
workflow.add_edge("perceive", "think")
workflow.add_edge("think", "act")
workflow.add_edge("act", "update_db")
workflow.add_edge("update_db", END)

# Compile the graph
app = workflow.compile()
