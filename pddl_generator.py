def extract_state_to_pddl(environment, robots, packages, output_file="problem.pddl"):
    """
    Generates a file problem.pddl with the state of the anvironment at the moment.
    """
    with open(output_file, "w") as f:
        f.write("(define (problem warehouse-delivery)\n")
        f.write(" (:domain warehouse)\n\n")

        # Objects
        f.write(" (:objects\n")
        for robot in robots:
            f.write(f"  {robot.id} - robot\n")
        for pkg in packages:
            f.write(f"  {pkg.id} - package\n")
        for x in range(environment.width):
            for y in range(environment.height):
                if not environment.is_obstacle(x, y):
                    f.write(f"  zone_{x}_{y} - location\n")
        f.write(" )\n\n")

        # Initial state 
        f.write(" (:init\n")
        for robot in robots:
            x, y = robot.position
            f.write(f"  (at-robot {robot.id} zone_{x}_{y})\n")
            f.write(f"  (robot-free {robot.id})\n")
        for pkg in packages:
            x, y = pkg.position
            f.write(f"  (at-package {pkg.id} zone_{x}_{y})\n")
        for x in range(environment.width):
            for y in range(environment.height):
                if not environment.is_obstacle(x, y):
                    for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < environment.width and 0 <= ny < environment.height:
                            if not environment.is_obstacle(nx, ny):
                                f.write(f"  (connected zone_{x}_{y} zone_{nx}_{ny})\n")
        f.write(" )\n\n")

        # Goal 
        f.write(" (:goal\n  (and\n")
        for pkg in packages:
            dx, dy = pkg.destination
            f.write(f"   (at-package {pkg.id} zone_{dx}_{dy})\n")
        f.write("  )\n )\n)\n")

    print(f"File {output_file} generated correctly.")

