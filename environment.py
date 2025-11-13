class Environment:
    def __init__(self, width=7, height=7):
        self.width = width
        self.height = height
        # 0 = free, 1 = obstacle
        self.grid = [[0 for _ in range(height)] for _ in range(width)]

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and not self.is_obstacle(x, y)

    def is_obstacle(self, x, y):
        return self.grid[x][y] == 1

    def toggle_obstacle(self, x, y):
        """change between cell and obstacle"""
        if self.is_obstacle(x, y):
            self.grid[x][y] = 0
        else:
            self.grid[x][y] = 1

