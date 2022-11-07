import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
class fuzzylogicsignals:
    def __init__(self):
        count = ctrl.Antecedent(np.arange(0, 11, 1), 'count')
        count_change = ctrl.Antecedent(np.arange(-10, 11, 1), 'count change')
        time = ctrl.Consequent(np.arange(0, 31, 1), 'time', defuzzify_method='centroid')

        # Generate fuzzy membership functions
        least = count['least'] = fuzz.trapmf(count.universe, [0,0, 1, 3])
        less = count['less'] = fuzz.trimf(count.universe, [1, 3, 5])
        normal = count['normal'] = fuzz.trimf(count.universe, [3, 5, 7])
        many = count['many'] = fuzz.trimf(count.universe, [5, 7, 9])
        very_much = count['very_much'] = fuzz.trapmf(count.universe, [7, 9,10, 10])

        # count_change['greatly_decreased'] = fuzz.trapmf(count_change.universe,[-10, -10, -7,-3])
        # count_change['decreased'] = fuzz.trimf(count_change.universe,[-6, -3, 0])
        # count_change['constant'] = fuzz.trimf(count_change.universe, [3, 3, 3])
        # count_change['increased'] = fuzz.trimf(count_change.universe, [0, 3, 6])
        # count_change['greatly_increased'] = fuzz.trapmf(count_change.universe, [3, 7, 10, 10])

        count_change['greatly_decreased'] = fuzz.trapmf(count_change.universe, [-10,-10, -3, -1])
        count_change['decreased'] = fuzz.trimf(count_change.universe, [-6, -3, 0])
        count_change['constant'] = fuzz.trimf(count_change.universe, [-3, 0, 3])
        count_change['increased'] = fuzz.trimf(count_change.universe,  [0, 3, 6])
        count_change['greatly_increased'] = fuzz.trapmf(count_change.universe, [3, 7, 10, 10])

        time['very_briefly'] = fuzz.trapmf(time.universe, [0,5,7, 12])
        time['briefly'] = fuzz.trimf(time.universe, [7, 12,17])
        time['medium'] = fuzz.trimf(time.universe,  [12, 17, 22])
        time['long'] = fuzz.trimf(time.universe,  [17, 22, 27])
        time['very_long'] = fuzz.trapmf(time.universe, [22, 26, 30, 30])

        rule1 = ctrl.Rule(count['least'] & count_change['greatly_decreased'] , time['very_briefly'])
        rule2 = ctrl.Rule(count['least'] & count_change['decreased'] , time['very_briefly'])
        rule3 = ctrl.Rule(count['least'] & count_change['constant'] , time['very_briefly'])
        rule4 = ctrl.Rule(count['least'] & count_change['increased'] , time['very_briefly'])
        rule5 = ctrl.Rule(count['least'] & count_change['greatly_increased'] , time['very_briefly'])

        rule6 = ctrl.Rule(count['less'] & count_change['greatly_decreased'] , time['very_briefly'])
        rule7 = ctrl.Rule(count['less'] & count_change['decreased'] , time['briefly'])
        rule8 = ctrl.Rule(count['less'] & count_change['constant'] , time['briefly'])
        rule9 = ctrl.Rule(count['less'] & count_change['increased'] , time['briefly'])
        rule10 = ctrl.Rule(count['less'] & count_change['greatly_increased'] , time['briefly'])

        rule11 = ctrl.Rule(count['normal'] & count_change['greatly_decreased'] , time['briefly'])
        rule12 = ctrl.Rule(count['normal'] & count_change['decreased'] , time['medium'])
        rule13 = ctrl.Rule(count['normal'] & count_change['constant'] , time['medium'])
        rule14 = ctrl.Rule(count['normal'] & count_change['increased'] , time['medium'])
        rule15 = ctrl.Rule(count['normal'] & count_change['greatly_increased'] , time['long'])

        rule16 = ctrl.Rule(count['many'] & count_change['greatly_decreased'] , time['long'])
        rule17 = ctrl.Rule(count['many'] & count_change['decreased'] , time['long'])
        rule18 = ctrl.Rule(count['many'] & count_change['constant'] , time['long'])
        rule19 = ctrl.Rule(count['many'] & count_change['increased'] , time['long'])
        rule20 = ctrl.Rule(count['many'] & count_change['greatly_increased'] , time['very_long'])

        rule21 = ctrl.Rule(count['very_much'] & count_change['greatly_decreased'] , time['very_long'])
        rule22 = ctrl.Rule(count['very_much'] & count_change['decreased'] , time['very_long'])
        rule23 = ctrl.Rule(count['very_much'] & count_change['constant'] , time['very_long'])
        rule24 = ctrl.Rule(count['very_much'] & count_change['increased'] , time['very_long'])
        rule25 = ctrl.Rule(count['very_much'] & count_change['greatly_increased'] , time['very_long'])

        self.input_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, 
        rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25]) 

    def fuzzytime(self, count, change_count):
        sim = ctrl.ControlSystemSimulation(self.input_ctrl)
        sim.input['count'] = count
        sim.input['count change'] = change_count
        sim.compute()
        out = sim.output['time']
        print(np.round(out,2))
        return np.round(out,2)

