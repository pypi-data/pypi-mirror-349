import re


class Formula:
    """A class to parse and manipulate chemical formulas. This class provides
    methods to sort, filter, and analyze chemical.

    Examples
    --------
    >>> formula = Formula("NdSi2")
    >>> formula.parsed_formula
    [('Nd', 1.0), ('Si', 2.0)]
    >>> formula.element_count
    2
    >>> formula.get_normalized_formula()
    'Nd1.0Si2.0'
    >>> formula.get_normalized_parsed_formula()
    [('Nd', 0.333333), ('Si', 0.666667)]
    >>> formula.get_normalized_indices()
    """

    def __init__(self, formula: str):
        self.formula = formula
        self.parsed_formula = self._parse_formula(formula)

    @staticmethod
    def order_by_alphabetical(formulas: list[str], reverse=False) -> list[str]:
        """Sort formulas alphabetically.

        Examples
        --------
        >>> formulas = ["AB2", "AB", "BC2D2", "BBC2"]
        >>> Formula.order_by_alphabetical(formulas)
        ["AB", "AB2", "BBC2", "BC2D2"]
        """
        return sorted(formulas, reverse=reverse)

    @staticmethod
    def count(formulas: list[str]) -> int:
        """Count the number of formulas in a list.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.count(formulas)
        4
        """
        return len(formulas)

    @staticmethod
    def count_unique(
        formulas: list[str],
    ) -> int:
        """Count the number of unique formulas in a list.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.count_unique(formulas)
        4
        """
        return len(set(formulas))

    @staticmethod
    def count_individual(
        formulas: list[str],
    ) -> dict[str, int]:
        """Count the number of occurrences of each formula in a list of
        formulas.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.count_formulas(formulas)
        {"NdSi2": 1, "ThOs": 1, "NdSi2Th2": 1, "YNdThSi2": 1}
        """
        return {formula: formulas.count(formula) for formula in formulas}

    @staticmethod
    @staticmethod
    def count_by_composition(
        formulas: list[str],
    ) -> dict[int, int]:
        """Count the number of formulas in each composition category.

        Examples
        --------
        >>>
        formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.count_formulas_by_composition(formulas)
        {2: 2, 3: 1, 4: 1}
        """
        sorted_formulas = Formula.filter_by_composition(formulas)
        return {k: len(v) for k, v in sorted_formulas.items()}

    @staticmethod
    def get_unique_formulas(
        formulas: list[str],
    ) -> set[str]:
        """Get unique formulas from a list of formulas.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "ThOs"]
        >>> Formula.get_unique_formulas(formulas)
        {"NdSi2", "ThOs"}
        """
        return set(formulas)

    @staticmethod
    def get_unique_elements(formulas: list[str]) -> set[str]:
        """Get unique elements from a list of formulas.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.get_unique_elements(formulas)
        {"Nd", "Si", "Th", "Os", "Y"}
        """
        elements = set()
        for formula in formulas:
            parsed_formula = Formula(formula).parsed_formula
            for element, _ in parsed_formula:
                elements.add(element)
        return elements

    @staticmethod
    def get_element_count(formulas: list[str]) -> dict[str, int]:
        """Get the count of each element in a list of formulas. Do not consider
        the stoichiometric value.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.get_element_count(formulas)
        {"Nd": 3, "Si": 3, "Th": 3, "Os": 1, "Y": 1}
        """
        element_count = {}
        for formula in formulas:
            parsed_formula = Formula(formula).parsed_formula
            for element, _ in parsed_formula:
                if element not in element_count:
                    element_count[element] = 0
                element_count[element] += 1
        return element_count

    @staticmethod
    def _parse_formula(formula: str) -> list[tuple[str, float]]:
        pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
        parsed = re.findall(pattern, formula)
        return [
            (element, float(index) if index else 1.0)
            for element, index in parsed
        ]

    @staticmethod
    def build_formula_from_parsed(parsed_formula) -> str:
        """Convert the parsed formula into a string. If the index can be
        converted to 1 (int), it will be removed.

        Examples
        --------
        >>> parsed_formula = [("Nd", 1.0), ("Si", 2.0)]
        >>> Formula.build_formula_from_parsed(parsed_formula)
        "NdSi2"
        """
        formula_string = ""
        for element, index in parsed_formula:
            if index.is_integer() and int(index) != 1:
                formula_string += f"{element}{int(index)}"
            elif index.is_integer() and int(index) == 1:
                formula_string += f"{element}"
            else:
                formula_string += f"{element}{index}"
        return formula_string

    @staticmethod
    def filter_by_composition(
        formulas: list[str],
    ) -> dict[int, list[str]]:
        """Sort formulas into categories based on their composition.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.filter_by_composition(formulas)
        {2: ["NdSi2", "ThOs"], 3: ["NdSi2Th2"], 4: ["YNdThSi2"]}
        """
        sorted_formulas = {}

        for formula in formulas:
            element_count = Formula(formula).element_count
            if element_count not in sorted_formulas:
                sorted_formulas[element_count] = []
            sorted_formulas[element_count].append(formula)
        return sorted_formulas

    @staticmethod
    def filter_by_single_composition(
        formulas: list[str], composition: int
    ) -> list[str]:
        """Filter formulas by the given composition type.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> Formula.filter_by_single_composition(formulas, 2)
        ["NdSi2", "ThOs"]
        """
        return [
            formula
            for formula in formulas
            if Formula(formula).element_count == composition
        ]

    @staticmethod
    def filter_by_elements_containing(
        formulas: list[str], elements: list[str]
    ) -> list[str]:
        """Filter formulas by a list of elements.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> elements = ["Nd", "Si"]
        >>> Formula.filter_by_elements(formulas, elements)
        ["NdSi2", "NdSi2Th2", "YNdThSi2"]
        """
        filtered_formulas = []
        for formula in formulas:
            parsed_formula = Formula(formula).parsed_formula
            if all(element in dict(parsed_formula) for element in elements):
                filtered_formulas.append(formula)
        return filtered_formulas

    @staticmethod
    def filter_by_elements_matching(
        formulas: list[str], elements: list[str]
    ) -> list[str]:
        """Filter formulas by a list of elements but the specified elements
        should be only contained.

        Examples
        --------
        >>> formulas = ["NdSi2", "ThOs", "NdSi2Th2", "YNdThSi2"]
        >>> elements = ["Nd", "Si"]
        >>> filter_by_elements(formulas, elements)
        ["NdSi2"]
        """
        filtered_formulas = []
        for formula in formulas:
            parsed_formula = Formula(formula).parsed_formula
            if all(element in dict(parsed_formula) for element in elements):
                if len(parsed_formula) == len(elements):
                    filtered_formulas.append(formula)
        return filtered_formulas

    @staticmethod
    def count_duplicates(formulas: list[str]) -> dict[str, int]:
        """Count the number of duplicates in a list of formulas.

        Examples
        --------
        >>> formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
        >>> Formula.count_duplicates(formulas)
        {"NdSi2": 2, "NdSi2Th2": 2}
        """
        duplicates = {}
        for formula in formulas:
            if formula not in duplicates:
                duplicates[formula] = 0
            duplicates[formula] += 1
        return {k: v for k, v in duplicates.items() if v > 1}

    @staticmethod
    def count_by_formula(formulas: list[str], formula_to_count: str) -> int:
        """Count the number of occurrences of a specific formula in a list of
        formulas.

        Examples
        --------
        >>> formulas = ["NdSi2", "NdSi2", "NdSi2Th2", "NdSi2Th2", "ThOs"]
        >>> Formula.count_by_formula(formulas, "NdSi2")
        2
        """
        return formulas.count(formula_to_count)

    def _normalized(self, decimals: int = 6) -> str:
        index_sum = sum(self.indices)
        normalized = [
            (element, count / index_sum)
            for element, count in self.parsed_formula
        ]
        return "".join(
            f"{element}{format(index, f'.{decimals}f')}"
            for element, index in normalized
        )

    @property
    def elements(self) -> list[str]:
        """Get the list of elements in the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.elements
        ["Nd", "Si"]
        """
        return [element for element, _ in self.parsed_formula]

    @property
    def indices(self) -> list[float]:
        """Get the list of indices in the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.indices
        [1.0, 2.0]
        """
        return [index for _, index in self.parsed_formula]

    @property
    def element_count(self) -> int:
        """Get the number of unique elements in the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.element_count
        2
        """
        return len(self.parsed_formula)

    @property
    def max_min_avg_index(self) -> tuple[float, float, float]:
        """Get the max, min, and avg index of the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.max_min_avg_index
        (2.0, 1.0, 1.5)
        """
        indices = self.indices
        return max(indices), min(indices), sum(indices) / len(indices)

    def get_normalized_indices(self, decimals=6) -> list[float]:
        """Get the normalized indices of the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.get_normalized_indices()
        [0.333333, 0.666667]
        >>> formula.get_normalized_indices(2)
        [0.33, 0.67]
        """
        total = sum(self.indices)
        return [round(index / total, decimals) for index in self.indices]

    def get_normalized_formula(self, decimals=6) -> str:
        """Get the normalized formula of the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.get_normalized_formula()
        "Nd0.333333Si0.666667"
        >>> formula.get_normalized_formula(2)
        "Nd0.33Si0.67"
        """
        return self._normalized(decimals=decimals)

    def get_normalized_parsed_formula(
        self, decimals=6
    ) -> list[tuple[str, float]]:
        """Get the normalized parsed formula of the formula.

        Examples
        --------
        >>> formula = Formula("NdSi2")
        >>> formula.get_normalized_parsed_formula()
        [("Nd", 0.333333), ("Si", 0.666667)]
        >>> formula.get_normalized_parsed_formula(2)
        [("Nd", 0.33), ("Si", 0.67)]
        """
        normalized = self._normalized(decimals=decimals)
        return self._parse_formula(normalized)
