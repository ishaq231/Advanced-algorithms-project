from utils import check_marks
class Student:
    def __init__(self,student_id):
        self.student_id = student_id
        self.level_5_modules = {}
        self.level_5_average = 0
        self.level_6_modules = {}
        self.level_6_average = 0
        self.final_mark = 0
        self.has_fail = False  # Flag to track if any module is failed
        self.failed_modules = []  # List to store failed modules (if needed)
        self.level_5_modules_used = {}  # Modules actually used for Level 5 (best 100 credits)
    def add_module(self,module,module_code,mark):
        module_code_split = module_code.split('-')
        credit = module_code_split[1]
        year = module_code_split[2]
        
        # Check if this module is a fail
        if mark < 40:
            self.has_fail = True
            self.failed_modules.append(module)
        
        if year == '2':
            self.level_5_modules[module] = (int(credit),mark)
        elif year == '3':
            self.level_6_modules[module] = (int(credit),mark)
        #print(f"Level 5 Modules: {self.level_5_modules}")
        #print(f"Level 6 Modules: {self.level_6_modules}")
    def calculate_level_5_average(self):
        # Create a list of (module_name, mark, credit) tuples from all modules
        # Filter out invalid marks (marks should be between 0-100)
        modules_list = [(module, mark, credit) for module, (credit, mark) in self.level_5_modules.items() if 0 <= mark <= 100]
        
        # Sort by mark in descending order (highest marks first)
        modules_list.sort(reverse=True, key=lambda x: x[1])
        
        total_credits = 0
        weighted_sum = 0
        self.level_5_modules_used = {}  # Reset the modules used
        
        for module, mark, credit in modules_list:
            if total_credits >= 100:
                break
            
            # Check if adding this module would exceed 100 credits
            if total_credits + credit <= 100:
                # Add the full module
                total_credits += credit
                weighted_sum += mark * credit
                self.level_5_modules_used[module] = mark
            else:
                # Add partial credits to reach exactly 100
                remaining_credits = 100 - total_credits
                total_credits += remaining_credits
                weighted_sum += mark * remaining_credits
                self.level_5_modules_used[module] = mark
                break  # We've reached 100 credits
        
        self.level_5_average = weighted_sum / total_credits if total_credits > 0 else 0
        
    def calculate_level_6_average(self):
        # Direct calculation without intermediate list - more memory efficient
        total_credits = 0
        weighted_sum = 0
        
        for module, (credit, mark) in self.level_6_modules.items():
            if 0 <= mark <= 100:  # Exclude invalid marks
                total_credits += credit
                weighted_sum += mark * credit
        
        self.level_6_average = weighted_sum / total_credits if total_credits > 0 else 0
    
    def final_mark_calc(self):
        # If student failed any module, they don't get a degree
        if self.has_fail:
            self.final_mark = 0
            return 0
        
        final_mark = ((self.level_6_average * 3) + self.level_5_average)/4
        self.final_mark = final_mark 
        
