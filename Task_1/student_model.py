from utils import check_marks
class Student:
    def __init__(self,student_id,level_5_modules,level_6_modules):
        self.student_id = student_id
        self.level_5_modules = {}
        self.level_6_modules = {}
    def add_module(self,module,module_code,mark):
        module_code_split = module_code.split('-')
        credit = module_code_split[1]
        year = module_code_split[2]
        if year == '2':
            self.level_5_modules[module] = (int(credit),mark)
        elif year == '3':
            self.level_6_modules[module] = (int(credit),mark)
        #print(f"Level 5 Modules: {self.level_5_modules}")
        #print(f"Level 6 Modules: {self.level_6_modules}")
    def calculate_level_5_average(self):
        # Group modules by credit value
        modules_by_credit = {}
        for module, (credit, mark) in self.level_5_modules.items():
            if credit not in modules_by_credit:
                modules_by_credit[credit] = []
            modules_by_credit[credit].append(mark)
        
        # Sort each credit group by mark (descending)
        for credit in modules_by_credit:
            modules_by_credit[credit].sort(reverse=True)
        
        total_credits = 0
        weighted_marks = []
        
        # Strategy: Add best marks prioritizing 30-credit, then 15-credit
        # Try to get as close to 100 as possible
        
        # First, add best 30-credit modules
        if 30 in modules_by_credit:
            for mark in modules_by_credit[30]:
                if total_credits + 30 <= 100:
                    if check_marks(mark) != "Invalid":
                        total_credits += 30
                        weighted_marks.append(mark * 30)
        
        # Then add best 15-credit modules
        if 15 in modules_by_credit:
            for mark in modules_by_credit[15]:
                if total_credits + 15 <= 100:
                    if check_marks(mark) != "Invalid":
                        total_credits += 15
                        weighted_marks.append(mark * 15)
                        
        if total_credits == 0:  # Avoid division by zero
            return 0, 0
        average = sum(weighted_marks) / total_credits
        return average, total_credits
            
                
        
            
        
    def calculate_level_6_average(self):
        pass