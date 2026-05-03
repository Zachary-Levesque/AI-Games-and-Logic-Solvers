import sys
from pathlib import Path


from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create a new CSP crossword generator.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font_path = Path(__file__).resolve().parent / "assets" / "fonts" / "OpenSans-Regular.ttf"
        font = ImageFont.truetype(str(font_path), 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        bbox = draw.textbbox((0, 0), letters[i][j], font=font)
                        w = bbox[2] - bbox[0]
                        h = bbox[3] - bbox[1]
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for var, words in self.domains.items():
            self.domains[var] = {word for word in words if len(word) == var.length}

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps.get((x, y))
        if overlap is None:
            return False

        x_index, y_index = overlap
        revised = False
        removable = set()
        for x_word in self.domains[x]:
            if not any(x_word[x_index] == y_word[y_index] for y_word in self.domains[y]):
                removable.add(x_word)

        if removable:
            self.domains[x] -= removable
            revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = list(arcs) if arcs is not None else [
            (var, neighbor)
            for var in self.domains
            for neighbor in self.crossword.neighbors(var)
        ]

        while queue:
            (x, y) = queue.pop(0)
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False

                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((x, neighbor))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        for var in assignment:
            if list(assignment.values()).count(assignment[var]) > 1:
                return False

        for (x, y) in self.crossword.overlaps:
            if self.crossword.overlaps[(x, y)] and x in assignment and y in assignment:
                cors = self.crossword.overlaps[(x, y)]
                if assignment[x][cors[0]] != assignment[y][cors[1]]:
                    return False
            
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_cost = []

        for word in self.domains[var]:
            eliminated = 0
            unassigned_neighbors = list(filter(lambda neighbor: neighbor not in assignment , self.crossword.neighbors(var)))
            for neighbor in unassigned_neighbors:
                for n_word in self.domains[neighbor]:
                    cors = self.crossword.overlaps[(var, neighbor)]
                    if len(word) > cors[0] and len(n_word) > cors[1]:
                        if word[cors[0]] != n_word[cors[1]]:
                            eliminated += 1
            word_cost.append((word, eliminated))

        sorted_word_cost = sorted(word_cost, key=lambda item: item[1])
        ordered_domain_values = list(map(lambda word: word[0], sorted_word_cost))

        return ordered_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        all_variables = self.crossword.variables.copy()
        unassigned_variables = list(filter(lambda var: var not in assignment, all_variables))
        smallest_domain_variables = sorted(unassigned_variables, key=lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x))))

        unassigned_variable = smallest_domain_variables.pop(0) # With best heuristic value
        return unassigned_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = word
            if self.consistent(new_assignment):
                assignment[var] = word
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
