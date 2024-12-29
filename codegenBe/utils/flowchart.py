from graphviz import Digraph

def generate_flowchart(algorithm):
    """
    Generate a flowchart based on the provided algorithm.
    """
    steps = algorithm.split("\n")
    flowchart = Digraph(format='png')
    flowchart.attr('node', shape='oval')  # Default shape is oval

    flowchart.node('start', 'Start')
    prev_node = 'start'

    decision_stack = []  # Stack to handle connections for decision nodes
    loop_stack = []      # Stack to manage loops

    for step in steps:
        step_text = step.split(": ", 1)[-1].strip()
        
        if not step_text:  # Skip empty steps or lines
            continue
        
        # Skip the first step "Start"
        if step_text.lower() == "start":
            continue
        
        # If the step is "Stop", add the 'End' node and connect it
        elif step_text.lower() == "stop":
            flowchart.node('end', 'End')
            flowchart.edge(prev_node, 'end')
            break

        shape = 'box'  # Default shape for regular steps
        node_id = f"step_{prev_node}"

        # Handling Input/Output (e.g., Prompt the user)
        if "Prompt the user" in step_text or "inputs" in step_text or "print" in step_text.lower():
            shape = 'parallelogram'  # Input/Output
            node_id = f"input_{prev_node}"
            simplified_text = f"{step_text.split('Prompt the user:')[-1]}"  # Extract specific value
        
        # Handling Decision (e.g., if condition)
        elif "if" in step_text.lower():
            shape = 'diamond'  # Decision node
            node_id = f"decision_{prev_node}"
            decision_stack.append(prev_node)  # Push current node to stack
            simplified_text = f"Decision: {step_text.split('If')[-1].strip()}"
            
        # Handling Loop (e.g., while or iterate)
        elif "while" in step_text.lower() or "iterate" in step_text.lower():
            shape = 'box'  # Loop condition
            node_id = f"loop_{prev_node}"
            loop_stack.append(prev_node)  # Push loop start to stack
            simplified_text = f"Loop: {step_text.split('Iterate')[-1].strip()}"
        
        # Default case (regular steps like assignment, etc.)
        else:
            simplified_text = f"Step: {step_text}"

        flowchart.node(node_id, simplified_text, shape=shape)
        flowchart.edge(prev_node, node_id)
        prev_node = node_id

        # Handle decision branching
        if "Check if" in step_text or "If" in step_text:
            # If statement with Yes/No branches
            flowchart.edge(node_id, 'end', label="No")  # Add No branch by default
            flowchart.edge(node_id, prev_node, label="Yes")  # Add Yes branch

        # Handle loop closure
        if "End while" in step_text or "End loop" in step_text:
            if loop_stack:
                loop_start = loop_stack.pop()
                flowchart.edge(prev_node, loop_start, label="Loop Back")  # Loop back to start

    # Save the flowchart as a PNG
    flowchart_filename = 'static/flowchart'
    flowchart.render(flowchart_filename, format='png')

    return flowchart_filename