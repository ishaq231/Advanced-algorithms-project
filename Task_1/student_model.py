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
    def add_module(self,module,module_code,mark):
        module_code_split = module_code.split('-')
        credit = module_code_split[1]
        year = module_code_split[2]
        
        # Check if this module is a fail
        if mark < 40:
            self.has_fail = True
        
        if year == '2':
            self.level_5_modules[module] = (int(credit),mark)
        elif year == '3':
            self.level_6_modules[module] = (int(credit),mark)
        #print(f"Level 5 Modules: {self.level_5_modules}")
        #print(f"Level 6 Modules: {self.level_6_modules}")
    def calculate_level_5_average(self):
        # Create a list of (mark, credit) tuples from all modules
        modules_list = []
        for module, (credit, mark) in self.level_5_modules.items():
            if check_marks(mark) != "Invalid":  # Exclude invalid marks
                modules_list.append((mark, credit))
        
        # Sort by mark in descending order (highest marks first)
        modules_list.sort(reverse=True, key=lambda x: x[0])
        
        total_credits = 0
        weighted_marks = []
        
        for mark, credit in modules_list:
            if total_credits >= 100:
                break
            
            # Check if adding this module would exceed 100 credits
            if total_credits + credit <= 100:
                # Add the full module
                total_credits += credit
                weighted_marks.append(mark * credit)
            else:
                # Add partial credits to reach exactly 100
                remaining_credits = 100 - total_credits
                total_credits += remaining_credits
                # Use proportional weighted mark: mark * remaining_credits
                weighted_marks.append(mark * remaining_credits)
                break  # We've reached 100 credits
        average = sum(weighted_marks) / total_credits
        self.level_5_average = average
        
    def calculate_level_6_average(self):
        modules_list = []
        for module, (credit, mark) in self.level_6_modules.items():
            if check_marks(mark) != "Invalid":  # Exclude invalid marks
                modules_list.append((mark, credit))
        
        total_credits = 0
        weighted_marks = []
        
        for mark, credit in modules_list:
            # Add the full module
            total_credits += credit
            weighted_marks.append(mark * credit)
        average = sum(weighted_marks) / total_credits
        self.level_6_average = average
    
    def final_mark_calc(self):
        # If student failed any module, they don't get a degree
        if self.has_fail:
            self.final_mark = 0
            return 0
        
        final_mark = ((self.level_6_average * 3) + self.level_5_average)/4
        self.final_mark = final_mark 