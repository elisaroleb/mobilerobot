import subprocess
import os

def call_planner(domain_file="domain.pddl", problem_file="problem.pddl", output_file="plan.txt"):
    """
    Executes Fast Donward and saves the resutlting plan. 
    """
    try:
        cmd = [
            "python",
            "downward/fast-downward.py",
            domain_file,
            problem_file,
            "--search",
            "astar(lmcut())"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if "Solution found" in result.stdout:
            print("Plan succesufully found.")
            if os.path.exists("sas_plan"):
                os.rename("sas_plan", output_file)
            return True
        else:
            print("No plan founded.")
            print(result.stdout)
            return False

    except Exception as e:
        print(f"Error executing the planifier: {e}")
        return False
