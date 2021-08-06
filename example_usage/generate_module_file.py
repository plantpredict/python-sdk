"""This file contains the code for "Generate a module file from module datasheet" in the "Example Usage" section of the
documentation located at https://plantpredict-python.readthedocs.io."""

import plantpredict
from plantpredict.enumerations import CellTechnologyTypeEnum, PVModelTypeEnum, ConstructionTypeEnum

# authenticate using API credentials
api = plantpredict.Api(
    username="insert username here",
    password="insert password here",
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# instantiate a local Module object
module = api.module()

# assign basic module parameters from the manufacturer's datasheet or similar data source
module.cell_technology_type = CellTechnologyTypeEnum.CDTE
module.number_of_cells_in_series = 264
module.pv_model = PVModelTypeEnum.ONE_DIODE_RECOMBINATION
module.reference_temperature = 25
module.reference_irradiance = 1000
module.stc_max_power = 430.0
module.stc_short_circuit_current = 2.54
module.stc_open_circuit_voltage = 219.2
module.stc_mpp_current = 2.355
module.stc_mpp_voltage = 182.55
module.stc_power_temp_coef = -0.32
module.stc_short_circuit_current_temp_coef = 0.04
module.stc_open_circuit_voltage_temp_coef = -0.28

# generate single diode parameters using the default algorithm/assumptions
# (see https://plantpredict.com/algorithm/module-file-generator/ for more information)
module.generate_single_diode_parameters_default()

# at this point, the user could simply add the remaining required fields and save the new Module. alternatively, the
# user can tune the module's single diode parameters to achieve (close to) a desired effective irradiance
# response (EIR)/low-light performance. the first step is to define target relative efficiencies at specified
# irradiance
module.effective_irradiance_response = [
    {'temperature': 25, 'irradiance': 1000, 'relative_efficiency': 1.0},
    {'temperature': 25, 'irradiance': 800, 'relative_efficiency': 1.0029},
    {'temperature': 25, 'irradiance': 600, 'relative_efficiency': 1.0003},
    {'temperature': 25, 'irradiance': 400, 'relative_efficiency': 0.9872},
    {'temperature': 25, 'irradiance': 200, 'relative_efficiency': 0.944}
]

# how a user tunes the module's performance is relatively open-ended, but a good place to start is using
# PlantPredict's "Optimize Series Resistance" algorithm (see https://plantpredict.com/algorithm/module-file-generator/
# for more information). this will automatically change the series resistance to generate an EIR closer to the target.
module.optimize_series_resistance()

# at any point the user can check the current model-calculated EIR to compare it to the target
calculated_effective_irradiance_response = module.calculate_effective_irradiance_response()

# additionally, an IV curve can be generated for the module for reference
iv_curve_at_stc = module.generate_iv_curve(num_iv_points=250)

# the initial series resistance optimization might not achieve an EIR close enough to the target. the user can modify
# any parameter, re-optimize series resistance or just recalculate dependent parameters, and check EIR repeatedly.
# this is the open-ended portion of module file generation. Important Note: after modifying parameters, if the user
# does not re-optimize series resistance, the "generate_single_diode_parameters_advanced" method must be called to
# re-calculate saturation_current_at_stc, diode_ideality_factor_at_stc, light_generated_current, and
# linear_temperature_dependence_on_gamma.
module.shunt_resistance_at_stc = 8000
module.dark_shunt_resistance = 9000
module.generate_single_diode_parameters_advanced()
new_eir = module.calculate_effective_irradiance_response()

# once the user is satisfied with the module parameters and performance, assign other required fields
module.name = "Test Module"
module.model = "Test Module"
module.manufacturer = "Solar Company"
module.length = 2009
module.width = 1232
module.heat_absorption_coef_alpha_t = 0.9
module.construction_type = ConstructionTypeEnum.GLASS_GLASS

# create module in the PlantPredict database
module.create()
