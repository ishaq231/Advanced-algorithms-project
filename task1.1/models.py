from dataclasses import dataclass


@dataclass(frozen=True)
class Module:
    module_code: str
    module_name: str
    credits: int
    year: int
    mark: float

    @classmethod
    def from_code(cls, module_code, module_name, mark):
        parts = module_code.split('-')
        if len(parts) < 3:
            raise ValueError(f"Invalid module code format: {module_code}")

    
        credits = int(parts[1])
        year = int(parts[2])
        mark_value = float(mark)

        return cls(
            module_code=module_code,
            module_name=module_name,
            credits=credits,
            year=year,
            mark=mark_value,
        )

    @property
    def is_passed(self):
        return self.mark >= 40

    @property
    def is_valid_mark(self):
        return 0 <= self.mark <= 100


class DegreeResult:
    def weighted_average(self, modules):
        valid_modules = [module for module in modules if module.is_valid_mark]
        total_credits = sum(module.credits for module in valid_modules)
        if total_credits == 0:
            return 0.0

        weighted_sum = sum(module.mark * module.credits for module in valid_modules)
        return weighted_sum / total_credits

    def level_5_best_100_average(self, level_5_modules):
        valid_modules = [module for module in level_5_modules if module.is_valid_mark]
        sorted_modules = sorted(valid_modules, key=lambda module: module.mark, reverse=True)

        used_modules = {}
        total_credits = 0
        weighted_sum = 0.0

        for module in sorted_modules:
            if total_credits >= 100:
                break

            available = 100 - total_credits
            credits_to_use = min(module.credits, available)
            if credits_to_use <= 0:
                continue

            total_credits += credits_to_use
            weighted_sum += module.mark * credits_to_use
            used_modules[module.module_name] = module.mark

        average = (weighted_sum / total_credits) if total_credits > 0 else 0.0
        return average, used_modules

    def final_mark(self, level_5_average, level_6_average, has_fail):
        if has_fail:
            return 0.0
        return ((level_6_average * 3) + level_5_average) / 4


class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.degree_result = DegreeResult()
        self.level_5_modules = []
        self.level_6_modules = []
        self.level_5_average = 0.0
        self.level_6_average = 0.0
        self.final_mark = 0.0
        self.has_fail = False
        self.failed_modules = []
        self.level_5_modules_used = {}

    def add_module(self, module_name, module_code, mark):
        module = Module.from_code(module_code, module_name, mark)
        self.add_module_instance(module)

    def add_module_instance(self, module):
        if not isinstance(module, Module):
            raise TypeError("Expected a Module instance")

        if not module.is_passed:
            self.has_fail = True
            self.failed_modules.append(module.module_name)

        if module.year == 2:
            self.level_5_modules.append(module)
        elif module.year == 3:
            self.level_6_modules.append(module)

    def calculate_level_5_average(self):
        self.level_5_average, self.level_5_modules_used = self.degree_result.level_5_best_100_average(
            self.level_5_modules
        )

    def calculate_level_6_average(self):
        self.level_6_average = self.degree_result.weighted_average(self.level_6_modules)

    def final_mark_calc(self):
        self.final_mark = self.degree_result.final_mark(
            self.level_5_average,
            self.level_6_average,
            self.has_fail,
        )
        return self.final_mark

