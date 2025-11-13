import pygame
from pddl_generator import extract_state_to_pddl
from planner_interface import call_planner
from plan_executor import PlanExecutor

CELL_SIZE = 80
MARGIN = 80

class GUI:
    def __init__(self, environment, robots, packages):
        pygame.init()
        self.env = environment
        self.robots = robots
        self.packages = packages

        self.width = environment.width * CELL_SIZE
        self.height = environment.height * CELL_SIZE + MARGIN
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Warehouse Simulator - Part 2")

        # colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 100, 255)
        self.ORANGE = (255, 165, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 180, 0)
        self.BLUE2 = (70, 130, 180)

        # buttons
        self.buttons = {
            "extract": pygame.Rect(10, self.height - 60, 150, 35),
            "reset": pygame.Rect(170, self.height - 60, 100, 35),
            "plan": pygame.Rect(280, self.height - 60, 100, 35),
            "execute": pygame.Rect(390, self.height - 60, 150, 35),
        }

    def draw(self):
        self.screen.fill(self.WHITE)

        # drawing the grid
        for x in range(self.env.width):
            for y in range(self.env.height):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = self.GRAY if self.env.is_obstacle(x, y) else self.WHITE
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)

        # drawing the packages
        for pkg in self.packages:
            x, y = pkg.position
            pygame.draw.circle(
                self.screen, self.ORANGE,
                (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 15
            )
            # drawing the destinations
            dx, dy = pkg.destination
            pygame.draw.circle(
                self.screen, self.RED,
                (dx * CELL_SIZE + CELL_SIZE // 2, dy * CELL_SIZE + CELL_SIZE // 2), 8, 2
            )

        # drawing the robot
        for robot in self.robots:
            x, y = robot.position
            pygame.draw.circle(
                self.screen, self.BLUE,
                (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 22
            )

        # drawing the buttons 
        self._draw_buttons()
        pygame.display.flip()

    def _draw_buttons(self):
        font = pygame.font.Font(None, 26)
        for key, rect in self.buttons.items():
            color = self.GREEN if key in ["extract", "reset"] else self.BLUE2
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            label = {
                "extract": "Extract State",
                "reset": "Reset",
                "plan": "Plan",
                "execute": "Execute Plan"
            }[key]
            text = font.render(label, True, self.WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        """Detects clicks in buttons and executes the determine actions"""
        if self.buttons["extract"].collidepoint(pos):
            print("Extracting current state...")
            extract_state_to_pddl(self.env, self.robots, self.packages)

        elif self.buttons["reset"].collidepoint(pos):
            print("Resetting simulation...")
            for r in self.robots:
                r.position = (0, 0)
            print("Robot reset.")

        elif self.buttons["plan"].collidepoint(pos):
            print("Running planner...")
            call_planner()

        elif self.buttons["execute"].collidepoint(pos):
            print("Executing plan...")
            executor = PlanExecutor(self.env, self.robots, self.packages, gui=self)
            executor.execute_plan()

