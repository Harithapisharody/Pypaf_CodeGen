
import re
def generate_algorithm(code):
    """
    Generate a step-by-step algorithm from the given Python code.
    """
    steps = ["Step 1: Start"]
    lines = code.split('\n')
    step_no = 2
    loop_depth = 0

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        # Function definitions
        if stripped_line.startswith("def "):
            func_name = stripped_line.split('(')[0].replace('def ', '').strip()
            params = stripped_line.split('(')[1].split(')')[0]
            steps.append(f"Step {step_no}: Define the function '{func_name}'  take inputs: {params}.")
            step_no+=1
        # Variable assignment (excluding return and comparison)
        elif "=" in stripped_line and not stripped_line.startswith(("#", "if", "elif", "else", "return","print(")) and "==" not in stripped_line:
            # Handle input calls separately
            if "input(" in stripped_line:
                # Extract the prompt string inside the input function
                match = re.search(r'input\((\".*?\")\)', stripped_line)
                if match:
                    prompt = match.group(1)  # Extract the prompt inside quotes
                    var = stripped_line.split('=')[0].strip()
                    steps.append(f"Step {step_no}: Prompt the user to {prompt} to variable '{var}'.")
                    step_no += 1
            else:
                var = stripped_line.split('=')[0].strip()
                value = stripped_line.split('=')[1].strip()
                steps.append(f"Step {step_no}: Assign value '{value}' to the variable '{var}'.")
                step_no+=1
        elif "return" in stripped_line:
            if "==" in stripped_line:
                # Handle return statements separately
                parts = stripped_line.split("==")
                left = parts[0].strip().replace("return", "").strip()
                right = parts[1].strip().replace(")","").strip()
                steps.append(f"Step {step_no}: Compare '{left}' == '{right}' and return result")
                step_no+=1

            else:
                return_value = stripped_line.replace("return ", "").strip()
                steps.append(f"Step {step_no}: Return the result as {return_value}.")
                step_no+=1

        # If conditions
        elif stripped_line.startswith(("if", "elif", "else")):
            if stripped_line.startswith("if"):
                condition = stripped_line[3:].strip().rstrip(":")
                steps.append(f"Step {step_no}: Check if the condition '{condition}' is true.")
                step_no+=1

            elif stripped_line.startswith("elif"):
                condition = stripped_line[5:].strip().rstrip(":")
                steps.append(f"Step {step_no}: If previous condition was false, check if '{condition}' is true.")
                step_no+=1
            elif stripped_line.startswith("else"):
                steps.append(f"Step {step_no}: If previous conditions were false, execute the else block.")
                step_no+=1

        # For loops
        elif stripped_line.startswith("for "):
    # Split loop line into components
            loop_part = stripped_line.split("in")[0].replace("for", "").strip()
            range_part = stripped_line.split("in")[1].strip().rstrip(":")  # Extract range part like "range(4)" or "range(1, 5)"
    
    # Handle multiple loop variables (e.g., i, j)
            loop_variables = [var.strip() for var in loop_part.split(",")]
    
    # Parse range values
            range_values = range_part.replace("range", "").strip("()").split(",")
            try:
                start = range_values[0].strip() if len(range_values) > 0 else "0"
                end = range_values[1].strip() if len(range_values) > 1 else "end"
                step = range_values[2].strip() if len(range_values) > 2 else "1"

                step_direction = "decreasing" if step.startswith("-") else "increasing"

        # Generate step description
                if loop_depth == 0:
                    
                        steps.append(
                        f"Step {step_no}: Iterate a for loop using variables {', '.join(loop_variables)} "
                        f"from {start} to {end} with {step_direction} step size of {step}."
                        )
                        step_no+=1
                    
            except Exception as e:
                print(f"Error evaluating range values: {e}")

            

            # Handle nested loops
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("for "):
                    next_loop_variable = next_line.split(" ")[1]
                    next_range_part = next_line.split("in")[1].strip().rstrip(":")
                    steps.append(f"Step {step_no}: Nested loop using '{next_loop_variable}' with range {next_range_part}.")
                    step_no += 1
                    i += 1
            loop_depth += 1

        # Handle print statements
        elif "print(" in stripped_line:
            match = re.search(r'print\((.*)\)', stripped_line)
            if match:
                value_to_print = match.group(1).strip()  # Extract the content inside print()
                if value_to_print == "":
                    steps.append(f"Step {step_no}: print() statement moves the output to the next line")
                    step_no+=1
                else:
                    steps.append(f"Step {step_no}: Print the statement {value_to_print}.")
                    step_no+=1

        # While loops
        elif stripped_line.startswith("while "):
            condition = stripped_line[6:].strip().rstrip(":")
            steps.append(f"Step {step_no}: Start a while loop that continues as long as the condition '{condition}' is true.")
            step_no += 1

        elif "import" in stripped_line:
            steps.append(f"Step {step_no}:{stripped_line}.")
            step_no+=1
        # Other executable statements
        elif stripped_line and not stripped_line.startswith("#"):
            steps.append(f"Step {step_no}: Execute {stripped_line}.")
            step_no+=1
        
        # Handle loop exit (decrease loop depth)
        elif stripped_line == "":
            loop_depth = max(0, loop_depth - 1)

        
        elif stripped_line.startswith("#") or stripped_line == "":
            continue
        
        

    steps.append(f"Step {step_no}: Stop")
    algorithm = "\n".join(steps)
    return algorithm
