import json
import requests
import pandas
from operator import itemgetter
from itertools import groupby

from plantpredict.plant_predict_entity import PlantPredictEntity
from plantpredict.utilities import convert_json, camel_to_snake, snake_to_camel
from plantpredict.error_handlers import handle_refused_connection, handle_error_response


class Module(PlantPredictEntity):
    """
    The :py:mod:`Module` entity models all of the characteristics of a photovoltaic solar module (panel).
    """
    def create(self):
        """
        **POST** */Module*

        Creates a new :py:mod:`plantpredict.Module` entity in the PlantPredict database using the attributes assigned to
        the local object instance. Automatically assigns the resulting :py:attr:`id` to the local object instance.
        See the minimum required attributes (below) necessary to successfully create a new
        :py:mod:`plantpredict.Module`. Note that the full scope of attributes is not limited to the minimum required set.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes for successful Module creation
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    name; str; Name of module file
                    model; str; Model number/name of module (can be the same as :py:attr:`name`)
                    manufacturer; str; Module manufacturer
                    length; float; Long side of the module. Must be between :py:data:`0.0` and :py:data:`10000.0` - units :py:data:`[mm]`.
                    width; float; Short side of the module. Must be between :py:data:`0.0` and :py:data:`10000.0` - units :py:data:`[mm]`.
                    cell_technology_type; int; Represents the cell technology type (CdTe, poly c-Si PERC, etc). Use :py:mod:`plantpredict.enumerations.CellTechnologyTypeEnum`.
                    pv_model; int; Represents the 1-diode model type (1-Diode, 1-Diode with recombination). Use :py:mod:`plantpredict.enumerations.PVModelTypeEnum`.
                    construction_type; int; Represents the module construction (Glass-Glass, Glass-Backsheet). Use :py:mod:`plantpredict.enumerations.ConstructionTypeEnum`.
                    stc_short_circuit_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_open_circuit_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_mpp_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_mpp_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_power_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    stc_short_circuit_current_temp_coef; float; Must be between :py:data:`-0.3` and :py:data:`2.0` - units :py:data:`[%/deg-C]`.
                    stc_open_circuit_voltage_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    saturation_current_at_stc; float; Must be between :py:data:`1e-13` and :py:data:`1e-6` - units :py:data:`[A]`.
                    diode_ideality_factor_at_stc; float; Must be between :py:data:`0.1` and :py:data:`5.0` - unitless.
                    linear_temp_dependence_on_gamma; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    exponential_dependency_on_shunt_resistance; float; Must be between :py:data:`1.0` and :py:data:`100.0` - unitless.
                    series_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100.0` - units :py:data:`[Ohms]`
                    dark_shunt_resistance; float; Must be between :py:data:`100.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    shunt_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    bandgap_voltage; float; Must be between :py:data:`0.5` and :py:data:`4.0` - units :py:data:`[V]`.
                    heat_absorption_coef_alpha_t; float; Must be between :py:data:`0.1` and :py:data:`1.0`.
                    reference_irradiance; float; Must be between :py:data:`400.0` and :py:data:`1361.0` - units :py:data:`[W/m^2]`.
                    built_in_voltage; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`3.0` - units :py:data:`[V]`.
                    recombination_parameter; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`30.0` - units :py:data:`[V]`

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                First, import the plantpredict library and create an instance of :py:mod:`plantpredict.api.Api` in your
                Python session, to authenticate as shown in Step 3 of :ref:`authentication_oauth2`. Then instantiate a
                local :py:mod:`plantpredict.module.Module` object.

                .. code-block:: python

                    module_to_create = plantpredict.Module()

                Populate the Module's require attributes by either directly assigning them...

                .. code-block:: python

                    from plantpredict.enumerations import CellTechnologyTypeEnum, PVModelTypeEnum, ConstructionTypeEnum

                    module_to_create.name = "Test Module"
                    module_to_create.model = "Test Module"
                    module_to_create.manufacturer = "Solar Company"
                    module_to_create.length = 2009
                    module_to_create.width = 1232
                    module_to_create.cell_technology_type = CellTechnologyTypeEnum.CDTE
                    module_to_create.pv_model = PVModelTypeEnum.ONE_DIODE_RECOMBINATION
                    module_to_create.construction_type = ConstructionTypeEnum.GLASS_GLASS
                    module_to_create.stc_short_circuit_current = 2.54
                    module_to_create.stc_open_circuit_voltage = 219.2
                    module_to_create.stc_mpp_current = 2.355
                    module_to_create.stc_mpp_voltage = 182.55
                    module_to_create.stc_power_temp_coef = -0.32
                    module_to_create.stc_short_circuit_current_temp_coef = 0.04
                    module_to_create.stc_open_circuit_voltage_temp_coef = -0.28
                    module_to_create.saturation_current_at_stc = 2.415081e-12
                    module_to_create.diode_ideality_factor_at_stc = 1.17
                    module_to_create.linear_temp_dependence_on_gamma = -0.08
                    module_to_create.exponential_dependency_on_shunt_resistance = 5.5
                    module_to_create.series_resistance_at_stc = 5.277
                    module_to_create.dark_shunt_resistance = 6400
                    module_to_create.shunt_resistance_at_stc = 6400
                    module_to_create.bandgap_voltage = 1.5
                    module_to_create.heat_absorption_coef_alpha_t = 0.9
                    module_to_create.reference_irradiance = 1000

                    # required for modules with recombination
                    module_to_create.built_in_voltage = 0.9
                    module_to_create.recombination_parameter = 0.9

                ...OR via dictionary assignment.

                .. code-block:: python

                    module_to_create.__dict__ = {
                        "name": "Test Module",
                        "model": "Test Module",
                        "manufacturer": "Solar Company",
                        "length": 2009,
                        "width": 1232,
                        "cell_technology_type": CellTechnologyTypeEnum.CDTE,
                        "pv_model": PVModelTypeEnum.ONE_DIODE_RECOMBINATION,
                        "construction_type": ConstructionTypeEnum.GLASS_GLASS,
                        "stc_short_circuit_current": 2.54,
                        "stc_open_circuit_voltage": 219.2,
                        "stc_mpp_current": 2.355,
                        "stc_mpp_voltage": 182.55,
                        "stc_power_temp_coef": -0.32,
                        "stc_short_circuit_current_temp_coef": 0.04,
                        "stc_open_circuit_voltage_temp_coef": -0.28,
                        "saturation_current_at_stc": 2.415081e-12,
                        "diode_ideality_factor_at_stc": 1.17,
                        "linear_temp_dependence_on_gamma": -0.08,
                        "exponential_dependency_on_shunt_resistance": 5.5,
                        "dark_shunt_resistance": 6400,
                        "shunt_resistance_at_stc": 6400,
                        "bandgap_voltage": 1.5,
                        "heat_absorption_coef_alpha_t": 0.9,
                        "reference_irradiance": 1000,
                        "built_in_voltage": 0.9,
                        "recombination_parameter": 0.9
                    }

                Create a new module in the PlantPredict database, and observe that the Module now has a unique database
                identifier.

                .. code-block:: python

                    module_to_create.create()

                    print(module_to_create.id)

        :return: A dictionary containing the module id.
        :rtype: dict
        """
        self.create_url_suffix = "/Module"

        # PlantPredict API requires 2 different fields for short circuit current to successfully create a Module.
        # this line of code streamlines Module creation by only requiring the user to define
        # "stc_short_circuit_current" (2018-09-21; things may have changed since then)
        self.short_circuit_current_at_stc = self.stc_short_circuit_current
        self.linear_temp_dependence_on_isc = self.stc_short_circuit_current_temp_coef

        # if values that are simply calculated from required parameters are not specified, calculate them
        if not hasattr(self, 'area') or self.area == 0:
            self.area = (self.length/1000.0)*(self.width/1000.0)
        if not hasattr(self, 'stc_efficiency') or self.stc_efficiency == 0:
            self.stc_efficiency = self.stc_max_power / (self.area * 1000.0)

        return super(Module, self).create()

    def delete(self):
        """
        **DELETE** */Module/* :py:attr:`id`

        Deletes an existing :py:mod:`plantpredict.Module` entity in the PlantPredict database according to the
        :py:attr:`id` of the local object instance.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                First, import the plantpredict library and create an instance of :py:mod:`plantpredict.api.Api` in your
                Python session, to authenticate as shown in Step 3 of :ref:`authentication_oauth2`. Then instantiate a
                local :py:mod:`plantpredict.module.Module` object with the :py:attr:`id` of the target Module in the
                PlantPredict database.

                .. code-block:: python

                    module_to_delete = plantpredict.Module(id=99999)

                Delete the Module.

                .. code-block:: python

                    module_to_delete.delete()

        :return: A dictionary {"is_successful": True}.
        :rtype: dict
        """
        self.delete_url_suffix = "/Module/{}".format(self.id)
        return super(Module, self).delete()

    def get(self):
        """
        **GET** */Module/* :py:attr:`id`

        Retrieves an existing :py:mod:`plantpredict.Module` entity from the PlantPredict database according to the
        :py:attr:`id` of the local object instance, and automatically assigns all of its attributes to the local object
        instance.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                First, import the plantpredict library and create an instance of :py:mod:`plantpredict.api.Api` in your
                Python session, to authenticate as shown in Step 3 of :ref:`authentication_oauth2`. Then instantiate a
                local :py:mod:`plantpredict.module.Module` object with the :py:attr:`id` of the target module in the
                PlantPredict database.

                .. code-block:: python

                    module_to_get = plantpredict.Module(id=99999)

                Retrieve the Module from the PlantPredict database.

                .. code-block:: python

                    module_to_get.get()

                This will automatically assign all of that Module's attributes to the local object instance. All of the
                attributes are now readily accessible in the local Python session.

                .. code-block:: python

                    module_name = module_to_get.name
                    Isc = module_to_get.stc_short_circuit_current

        :return: A dictionary containing all of the retrieved Module attributes. (Matches the result of calling
                 `self.__dict__` after calling this method).
        :rtype: dict
        """
        self.get_url_suffix = "/Module/{}".format(self.id)
        return super(Module, self).get()

    def update(self):
        """
        **PUT** */Module*

        Updates an existing :py:mod:`plantpredict.Module` entity in PlantPredict using the full attributes of the local
        object instance. Calling this method is most commonly preceded by instantiating a local instance of
        :py:mod:`plantpredict.Module` with a specified :py:attr:`id`, calling :py:meth:`plantpredict.Module.get()`,
        and changing any attributes locally.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                First, import the plantpredict library and create an instance of :py:mod:`plantpredict.api.Api` in your
                Python session, to authenticate as shown in Step 3 of :ref:`authentication_oauth2`. Then instantiate a
                local :py:mod:`plantpredict.module.Module` object with the :py:attr:`id` of the target module in the
                PlantPredict database.

                .. code-block:: python

                    module_to_update = plantpredict.Module(id=99999)

                Retrieve the Module from the PlantPredict database.

                .. code-block:: python

                    module_to_update.get()

                This will automatically assign all of that Module's attributes to the local object instance. Any/all
                of the attributes can now be modified locally.

                .. code-block:: python

                    module.name = "New Name"
                    module.shunt_resistance_at_stc = 8000

                Persist (update) the local changes to the PlantPredict database.

                .. code-block:: python

                    module.update()

        :return: A dictionary {"is_successful": True}.
        :rtype: dict
        """
        self.update_url_suffix = "/Module"
        return super(Module, self).update()

    @handle_refused_connection
    @handle_error_response
    def generate_single_diode_parameters_default(self):
        """
        **POST** */Module/Generator/GenerateSingleDiodeParametersDefault*

        Generates single-diode parameters from module electrical characteristics available on any standard
        manufacturers' module datasheet. Detailed documentation on the algorithm and assumptions can be found
        `here <https://plantpredict.com/algorithm/module-file-generator/#756-2>`_. (Note: The values in the table
        titled "Defaulted Inputs" are used in the algorithm and returned in the response of this method). An example of
        using this method in practice can be found in :ref:`example_usage`.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    cell_technology_type; int; Represents the cell technology type (CdTe, poly c-Si PERC, etc). Use :py:mod:`plantpredict.enumerations.CellTechnologyTypeEnum`.
                    pv_model; int; Represents the 1-diode model type (1-Diode, 1-Diode with recombination). Use :py:mod:`plantpredict.enumerations.PVModelTypeEnum`.
                    number_of_cells_in_series; int; Number of cells in one string of cells - unitless
                    reference_irradiance; float; Must be between :py:data:`400.0` and :py:data:`1361.0` - units :py:data:`[W/m^2]`. However, the calculation is always made at :py:data:`1000 W/m^2`.
                    reference_temperature; float; Must be between :py:data:`-20.0` and :py:data:`80.0` - units :py:data:`[deg-C]`. However, the calculation is always made at :py:data:`25 deg-C`.
                    stc_max_power; float; Must be between :py:data:`0.0` and :py:data:`1000.0` - units :py:data:`[W]`.
                    stc_short_circuit_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_open_circuit_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_mpp_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_mpp_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_power_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    stc_short_circuit_current_temp_coef; float; Must be between :py:data:`-0.3` and :py:data:`2.0` - units :py:data:`[%/deg-C]`.

        .. container:: toggle

            .. container:: header

                **Generated Parameters**

            .. container:: generated_parameters

                .. csv-table:: Generated Parameters
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    series_resistance_at_stc; float; units :py:data:`[Ohms]`
                    maximum_series_resistance; float; units :py:data:`[Ohms]`
                    recombination_parameter; float; units :py:data:`[V]`
                    maximum_recombination_parameter; float; units :py:data:`[V]`
                    shunt_resistance_at_stc; float; units :py:data:`[Ohms]`
                    exponential_dependency_on_shunt_resistance; float; Defaulted to 5.5 - unitless
                    dark_shunt_resistance; float; units :py:data:`[Ohms]`
                    saturation_current_at_stc; float; units :py:data:`[A]`
                    diode_ideality_factor_at_stc; float; unitless
                    linear_temp_dependence_on_gamma; float; units :py:data:`[%/deg-C]`
                    light_generated_current; float; units :py:data:`[A]`

        :return: Dictionary mirroring local module object with newly generated parameters.
        :rtype: dict
        """
        response = requests.post(
            url=self.api.base_url + "/Module/Generator/GenerateSingleDiodeParametersDefault",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

        self.__dict__.update(convert_json(json.loads(response.content), camel_to_snake))

        return response

    @handle_refused_connection
    @handle_error_response
    def generate_single_diode_parameters_advanced(self):
        """
        **POST** */Module/Generator/GenerateSingleDiodeParametersAdvanced*

        Solves for unknown single-diode parameters from module electrical characteristics and known single-diode
        parameters. This method is considered "advanced" because it requires more inputs to generate the remaining
        single-diode parameters. Whereas, the "default" method
        :py:meth:`plantpredict.Module.generate_single_diode_parameters_default` is relatively basic in that it requires
        less inputs and automatically calculates more of the parameters. An example of using this method in practice
        can be found in :ref:`example_usage`.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    cell_technology_type; int; Represents the cell technology type (CdTe, poly c-Si PERC, etc). Use :py:mod:`plantpredict.enumerations.CellTechnologyTypeEnum`.
                    pv_model; int; Represents the 1-diode model type (1-Diode, 1-Diode with recombination). Use :py:mod:`plantpredict.enumerations.PVModelTypeEnum`.
                    number_of_cells_in_series; int; Number of cells in one string of cells - unitless
                    reference_irradiance; float; Must be between :py:data:`400.0` and :py:data:`1361.0` - units :py:data:`[W/m^2]`. However, the calculation is always made at :py:data:`1000 W/m^2`.
                    reference_temperature; float; Must be between :py:data:`-20.0` and :py:data:`80.0` - units :py:data:`[deg-C]`. However, the calculation is always made at :py:data:`25 deg-C`.
                    stc_max_power; float; Must be between :py:data:`0.0` and :py:data:`1000.0` - units :py:data:`[W]`.
                    stc_short_circuit_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_open_circuit_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_mpp_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_mpp_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_power_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    stc_short_circuit_current_temp_coef; float; Must be between :py:data:`-0.3` and :py:data:`2.0` - units :py:data:`[%/deg-C]`.
                    series_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100.0` - units :py:data:`[Ohms]`
                    shunt_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    dark_shunt_resistance; float; Must be between :py:data:`100.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    recombination_parameter; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`30.0`
                    exponential_dependency_on_shunt_resistance; float; Must be between :py:data:`1.0` and :py:data:`100.0` - unitless.
                    bandgap_voltage; float; Must be between :py:data:`0.5` and :py:data:`4.0` - units :py:data:`[V]`.
                    built_in_voltage; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`3.0` - units :py:data:`[V]`.

        .. container:: toggle

            .. container:: header

                **Generated Parameters**

            .. container:: generated_parameters

                .. csv-table:: Generated Parameters
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    maximum_series_resistance; float; units :py:data:`[Ohms]`
                    maximum_recombination_parameter; float; units :py:data:`[V]`
                    saturation_current_at_stc; float; units :py:data:`[A]`
                    diode_ideality_factor_at_stc; float; unitless
                    linear_temp_dependence_on_gamma; float; units :py:data:`[%/deg-C]`
                    light_generated_current; float; units :py:data:`[A]`

        :return: Dictionary mirroring local module object with newly generated parameters.
        :rtype: dict
        """
        response = requests.post(
            url=self.api.base_url + "/Module/Generator/GenerateSingleDiodeParametersAdvanced",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

        self.__dict__.update(convert_json(json.loads(response.content), camel_to_snake))

        return response

    @handle_refused_connection
    @handle_error_response
    def calculate_effective_irradiance_response(self):
        """
        **POST** */Module/Generator/CalculateEffectiveIrradianceResponse*

        Calculates the relative efficiency for any number of irradiance conditions with respect to performance at :py:data:`1000 W/m^2` for a given temperature. Detailed
        documentation on this calculation can be found `here
        <https://plantpredict.com/algorithm/module-file-generator/#effective-irradiance-response-eir-calculation>`_.
        Unlike other of the :py:mod:`plantpredict.Module` methods related to generating module files, this method only returns
        a dictionary, and does not also auto-assign any attributes to the local object.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    effective_irradiance_response; list of dict; Contains irradiance/temperature conditions at which to calculate relative efficiency. See example code below for usage.
                    cell_technology_type; int; Represents the cell technology type (CdTe, poly c-Si PERC, etc). Use :py:mod:`plantpredict.enumerations.CellTechnologyTypeEnum`.
                    pv_model; int; Represents the 1-diode model type (1-Diode, 1-Diode with recombination). Use :py:mod:`plantpredict.enumerations.PVModelTypeEnum`.
                    number_of_cells_in_series; int; Number of cells in one string of cells - unitless
                    reference_irradiance; float; Must be between :py:data:`400.0` and :py:data:`1361.0` - units :py:data:`[W/m^2]`. However, only the irradiance values provided in :py:attr:`effective_irradiance_response are used in this calculation.
                    reference_temperature; float; Must be between :py:data:`-20.0` and :py:data:`80.0` - units :py:data:`[deg-C]`. However, only the temperature values provided in :py:attr:`effective_irradiance_response are used in this calculation.
                    stc_max_power; float; Must be between :py:data:`0.0` and :py:data:`1000.0` - units :py:data:`[W]`.
                    stc_short_circuit_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_open_circuit_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_mpp_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_mpp_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_power_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    stc_short_circuit_current_temp_coef; float; Must be between :py:data:`-0.3` and :py:data:`2.0` - units :py:data:`[%/deg-C]`.
                    series_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100.0` - units :py:data:`[Ohms]`
                    shunt_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    dark_shunt_resistance; float; Must be between :py:data:`100.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    recombination_parameter; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`30.0`
                    exponential_dependency_on_shunt_resistance; float; Must be between :py:data:`1.0` and :py:data:`100.0` - unitless.
                    bandgap_voltage; float; Must be between :py:data:`0.5` and :py:data:`4.0` - units :py:data:`[V]`.
                    built_in_voltage; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`3.0` - units :py:data:`[V]`.
                    saturation_current_at_stc; float; Must be between :py:data:`1e-13` and :py:data:`1e-6` - units :py:data:`[A]`.
                    diode_ideality_factor_at_stc; float; Must be between :py:data:`0.1` and :py:data:`5.0` - unitless.
                    linear_temp_dependence_on_gamma; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    light_generated_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                First, import the plantpredict library and create an instance of :py:mod:`plantpredict.api.Api` in your
                Python session, to authenticate as shown in Step 3 of :ref:`authentication_oauth2`. Then instantiate a
                local :py:mod:`plantpredict.module.Module` object as shown in previous examples. Then, assuming that all
                of the other required attributes have been assigned to the local object, assign the attribute
                :py:attr:`effective_irradiance_response` as follows (this determines which conditions the relative
                efficiencies will be calculated at):

                .. code-block:: python

                    module.effective_irradiance_response = [
                        {'temperature': 25, 'irradiance': 1000},
                        {'temperature': 25, 'irradiance': 800},
                        {'temperature': 25, 'irradiance': 600},
                        {'temperature': 25, 'irradiance': 400},
                        {'temperature': 25, 'irradiance': 200}
                    ]

                *Important note: For each dictionary in :py:attr:`effective_irradiance_response`, there is an optional
                field (in addition to py:attr:`temperature` and py:attr:`irradiance`), :py:attr:`relative_efficiency`.
                For this method, that field does not have to be defined - it is used for
                :py:meth:`optimize_series_resistance` to be used as a target for tuning the series resistance. The EIR
                calculated by this method will be different from the target. In the context of creating a new module
                file, a user would probably want to compare the model-calculated EIR (determined from this method), to
                the target relative efficiencies in :py:attr:`effective_irradiance_response`, which is why they have
                :py:attr:`temperature` and :py:attr:`irradiance` in common.*

                Call this method to generate the model-calculated effective irradiance response.

                .. code-block:: python

                    module.calculate_effective_irradiance_response()

                Which returns the following sample response (a relative efficiency of 0.99 represents 99% or -1%
                efficiency relative to :py:data:`[W/m^2]` at the same temperature):

                .. code-block:: python

                    [
                        {'temperature': 25, 'irradiance': 1000, 'relative_efficiency': 1.0},
                        {'temperature': 25, 'irradiance': 800, 'relative_efficiency': 1.02},
                        {'temperature': 25, 'irradiance': 600, 'relative_efficiency': 1.001},
                        {'temperature': 25, 'irradiance': 400, 'relative_efficiency': 0.99},
                        {'temperature': 25, 'irradiance': 200, 'relative_efficiency': 0.97}
                    ]

        :return: A list of dictionaries containing the calculated relative efficiencies (see Example Code above).
        :rtype: list of dict
        """
        return requests.post(
            url=self.api.base_url + "/Module/Generator/CalculateEffectiveIrradianceResponse",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

    @handle_refused_connection
    @handle_error_response
    def optimize_series_resistance(self):
        """
        **POST** */Module/Generator/OptimizeSeriesResistance*

        While this method can be called independently, it is most commonly used after first calling
        :py:meth:`plantpredict.Module.generate_single_diode_parameters_advanced` or
        :py:meth:`plantpredict.Module.generate_single_diode_parameters_default`. Automatically "tunes"
        :py:attr:`series_resistance_at_stc` to bring the model-calculated effective irradiance
        (EIR) response close to a user-specified target EIR. Also recalculates single-diode parameters dependent on
        :py:attr:`series_resistance_at_stc`. Detailed documentation on the algorithm used to accomplish this can be
        found `here
        <https://plantpredict.com/algorithm/module-file-generator/#optimize-series-resistance-to-match-eir-algorithm>`_.
        An example of using this method in practice can be found in :ref:`example_usage`.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    effective_irradiance_response; list of dict; List of dictionaries each containing temperature, irradiance, and the target efficiency relative to STC at those conditions.
                    cell_technology_type; int; Represents the cell technology type (CdTe, poly c-Si PERC, etc). Use :py:mod:`plantpredict.enumerations.CellTechnologyTypeEnum`.
                    pv_model; int; Represents the 1-diode model type (1-Diode, 1-Diode with recombination). Use :py:mod:`plantpredict.enumerations.PVModelTypeEnum`.
                    number_of_cells_in_series; int; Number of cells in one string of cells - unitless
                    reference_irradiance; float; Must be between :py:data:`400.0` and :py:data:`1361.0` - units :py:data:`[W/m^2]`. While required, this value isn't used in the calculation.
                    reference_temperature; float; Must be between :py:data:`-20.0` and :py:data:`80.0` - units :py:data:`[deg-C]`. While required, this value isn't used in the calculation.
                    stc_max_power; float; Must be between :py:data:`0.0` and :py:data:`1000.0` - units :py:data:`[W]`.
                    stc_short_circuit_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_open_circuit_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_mpp_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_mpp_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_power_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    stc_short_circuit_current_temp_coef; float; Must be between :py:data:`-0.3` and :py:data:`2.0` - units :py:data:`[%/deg-C]`.
                    series_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100.0` - units :py:data:`[Ohms]`
                    shunt_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    dark_shunt_resistance; float; Must be between :py:data:`100.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    recombination_parameter; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`30.0`
                    exponential_dependency_on_shunt_resistance; float; Must be between :py:data:`1.0` and :py:data:`100.0` - unitless.
                    bandgap_voltage; float; Must be between :py:data:`0.5` and :py:data:`4.0` - units :py:data:`[V]`.
                    built_in_voltage; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`3.0` - units :py:data:`[V]`.
                    saturation_current_at_stc; float; Must be between :py:data:`1e-13` and :py:data:`1e-6` - units :py:data:`[A]`.
                    diode_ideality_factor_at_stc; float; Must be between :py:data:`0.1` and :py:data:`5.0` - unitless.
                    linear_temp_dependence_on_gamma; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    light_generated_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`

        :return: Dictionary mirroring local module object with newly generated parameters.
        :rtype: dict
        """
        response = requests.post(
            url=self.api.base_url + "/Module/Generator/OptimizeSeriesResistance",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

        self.__dict__.update(convert_json(json.loads(response.content), camel_to_snake))

        return response

    @staticmethod
    def _parse_key_iv_points_template(file_path, sheet_name=None):
        """
        Parses the PlantPredict standard template for Key IV Points input and returns a JSON-serializable
        data structure.

        :param file_path: Full path to .xlsx file containing Key IV points data.
        :type file_path: str
        :param sheet_name: Sheet name containing data (only required if using file with multiple Excel sheets).
        :type sheet_name: str
        :return: List of dictionaries containing data in appropriate structure for process_key_iv_points() method.
        :rtype: list of dict
        """
        xl = pandas.ExcelFile(file_path)
        sheet_idx = 0 if not sheet_name else xl.sheet_names.index(sheet_name)
        xls_data = xl.parse(xl.sheet_names[sheet_idx], index_col=None).to_dict('records')

        key_iv_points_data = []
        for d in xls_data:
            key_iv_points_data.append({
                "temperature": d["Temperature [deg-C]"],
                "irradiance": d["Irradiance [W/m2]"],
                "short_circuit_current": d["Isc [A]"],
                "mpp_current": d["Imp [A]"],
                "open_circuit_voltage": d["Voc [V]"],
                "mpp_voltage": d["Vmp [V]"],
                "max_power": d["Pmp [W]"],
            })

        return key_iv_points_data

    @handle_refused_connection
    @handle_error_response
    def process_key_iv_points(self, file_path=None, key_iv_points_data=None):
        """
        **POST** */Module/Generator/ProcessKeyIVPoints*

        Processes "Key IV Points" data, either from a :download:`file template <_static/PlantPredict_KeyIVPointsTemplate.xlsx>` or
        similar data structure. This is used as a pre-processing step to module file generation - it returns the minimum
        required fields for :py:meth:`plantpredict.generate_single_diode_parameters_default`. It also automatically
        assigns the resulting attributtes to the local object instance of :py:mod:`plantpredict.Module`. Detailed
        algorithmic documentation for this method can be found `here
        <https://plantpredict.com/algorithm/module-file-generator/#processing-key-i-v-points>`_. See "Example Code"
        below for sample usage and "Generated Parameters" for the resulting attributes assigned to the local object
        instance.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                If the user is using the Excel template, usage of this method is straightforward:

                .. code-block:: python

                    module = plantpredict.Module()
                    module.process_key_iv_points(file_path="path_to_key_iv_points_template.xlsx")

                However, the user can also manually construct the data structure and call the method as follows:

                .. code-block:: python

                    input_data = [
                        {
                            "temperature": 15,
                            "irradiance": 1000,
                            "short_circuit_current": 0.174,
                            "open_circuit_voltage": 83.71,
                            "mpp_current": 0.150,
                            "mpp_voltage": 70.28,
                            "max_power": 10.56,
                        },
                        {
                            "temperature": 25,
                            "irradiance": 1000,
                            "short_circuit_current": 1.749,
                            "open_circuit_voltage": 89.71,
                            "mpp_current": 1.590,
                            "mpp_voltage": 72.04,
                            "max_power": 114.52,
                        },
                        {
                            "temperature": 25,
                            "irradiance": 800,
                            "short_circuit_current": 1.399,
                            "open_circuit_voltage": 88.85,
                            "mpp_current": 1.272,
                            "mpp_voltage": 72.20,
                            "max_power": 91.85,
                        },
                        {
                            "temperature": 25,
                            "irradiance": 600,
                            "short_circuit_current": 1.049,
                            "open_circuit_voltage": 87.75,
                            "mpp_current": 0.951,
                            "mpp_voltage": 72.75,
                            "max_power": 68.68,
                        },
                        {
                            "temperature": 25,
                            "irradiance": 400,
                            "short_circuit_current": 0.700,
                            "open_circuit_voltage": 86.27,
                            "mpp_current": 0.630,
                            "mpp_voltage": 71.92,
                            "max_power": 45.29,
                        },
                        {
                            "temperature": 25,
                            "irradiance": 200,
                            "short_circuit_current": 0.350,
                            "open_circuit_voltage": 83.67,
                            "mpp_current": 0.311,
                            "mpp_voltage": 70.32,
                            "max_power": 21.88,
                        },
                            "temperature": 50,
                            "irradiance": 1000,
                            "short_circuit_current": 1.768,
                            "open_circuit_voltage": 83.05,
                            "mpp_current": 1.599,
                            "mpp_voltage": 65.71,
                            "max_power": 105.07,
                        }
                    ]

                    module.process_key_iv_points(key_iv_points_data=input_data)

                While the only *required* temperature/irradiance conditions is STC (25 deg-C / 1000 W/m^2), more input
                data is required to generate temperature coefficients and effective irradiance response (see Generated
                Parameters).

        .. container:: toggle

            .. container:: header

                **Generated Parameters**

            .. container:: generated_parameters

                The following parameters are automatically assigned as attributes to the local instance of :py:class:`plantpredict.Module`.

                .. csv-table:: Generated Parameters
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    stc_short_circuit_current; float; Always returned with minimum required input (data at STC) - units :py:data:`[A]`
                    stc_open_circuit_voltage; float; Always returned with minimum required input (data at STC) - units :py:data:`[V]`
                    stc_mpp_current; float; Always returned with minimum required input (data at STC) - units :py:data:`[A]`
                    stc_mpp_voltage; float; Always returned with minimum required input (data at STC) - units :py:data:`[V]`
                    stc_max_power; float; Always returned with minimum required input (data at STC) - units :py:data:`[W]`
                    stc_short_circuit_current_temp_coef; float; Only returned if data provided at :py:data:`1000 W/m^2` and at least one temperature other than :py:data:`25 deg-C` - units :py:data:`[%/deg-C]`
                    stc_open_circuit_voltage_temp_coef; float; Only returned if data provided at :py:data:`1000 W/m^2` and at least one temperature other than :py:data:`25 deg-C` - units :py:data:`[%/deg-C]`
                    stc_power_temp_coef; float; Only returned if data provided at :py:data:`1000 W/m^2` and at least one temperature other than :py:data:`25 deg-C` - units :py:data:`[%/deg-C]`
                    effective_irradiance_response; dict; Only returned if data provided at multiple irradiances for a single temperature - see example output below for contents.

            .. container:: generated_parameters_dict

                The following is an example of the dictionary output (mirrors "Generated Parameters").

                .. code-block:: python

                    {
                        "stc_short_circuit_current": 1.7592,
                        "stc_open_circuit_voltage": 90.2189,
                        "stc_mpp_current": 1.6084,
                        "stc_mpp_voltage": 72.4938,
                        "stc_short_circuit_current_temp_coef": 0.0519,
                        "stc_open_circuit_voltage_temp_coef": -0.3081,
                        "stc_power_temp_coef": -0.3535,
                        "effective_irradiance_response": [
                            {"temperature": 25, "irradiance": 1000, "relative_efficiency": 1.0},
                            {"temperature": 25, "irradiance": 800, "relative_efficiency": 1.0039},
                            {"temperature": 25, "irradiance": 600, "relative_efficiency": 1.0032},
                            {"temperature": 25, "irradiance": 400, "relative_efficiency": 0.9925},
                            {"temperature": 25, "irradiance": 200, "relative_efficiency": 0.9582},
                        ]
                    }

        :param file_path: File path to the .xlsx template for Key IV Points (input option 1).
        :type file_path: str
        :param key_iv_points_data: List of dictionaries containing module electrical characteristics at STC and other temperature/irradiance conditions (input option 2).
        :type key_iv_points_data: lists of dict
        :return: Dictionary containing STC electrical parameters, temperature coefficients, and effective irradiance response, depending on the scope of the input data provided (see "Generated Parameters" above).
        :rtype: dict
        """
        # if the input is the .xlsx template, parse it
        if not file_path and not key_iv_points_data:
            raise ValueError(
                "Either a file path to the .xslx template for Key IV Points input or the properly formatted " 
                "JSON-serializable data structure for Key IV Points input must be assigned as input. See the Python "
                "SDK documentation (https://plantpredict-python.readthedocs.io/en/latest/) for more information."
            )
        elif file_path and key_iv_points_data:
            raise ValueError(
                "Only one input option may be specified."
            )

        # if the user specifies a file_path to the .xlsx template, parse it
        elif file_path:
            key_iv_points_data = self._parse_key_iv_points_template(file_path)

        response = requests.post(
            url=self.api.base_url + "/Module/Generator/ProcessKeyIVPoints",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=[convert_json(d, snake_to_camel) for d in key_iv_points_data]
        )

        self.__dict__.update(convert_json(json.loads(response.content), camel_to_snake))

        return response

    @staticmethod
    def _parse_full_iv_curves_template(file_path, sheet_name=None):
        """
        Locally parses the PlantPredict standard template for Full IV Curves input and returns a JSON-serializable
        data structure.

        :param file_path: Full path to .xslx file containing Full IV Curve data.
        :type file_path: str
        :param sheet_name: Sheet name containing data (only required if using file with multiple Excel sheets).
        :type sheet_name: str
        :return: List of dictionaries containing data in appropriate structure for process_full_iv_curves() method.
        :rtype: list of dict
        """
        xl = pandas.ExcelFile(file_path)
        sheet_idx = 0 if not sheet_name else xl.sheet_names.index(sheet_name)
        xls_data = xl.parse(xl.sheet_names[sheet_idx], index_col=None).to_dict('records')

        grouper = itemgetter("Temperature [deg-C]", "Irradiance [W/m2]")
        full_iv_curves_data = []
        for key, grp in groupby(sorted(xls_data, key=grouper), grouper):
            temp_dict = dict(zip(["Temperature [deg-C]", "Irradiance [W/m2]"], key))

            iv_points = [(item["I [A]"], item["V [V]"]) for item in grp]
            full_iv_curves_data.append({
                "temperature": temp_dict["Temperature [deg-C]"],
                "irradiance": temp_dict["Irradiance [W/m2]"],
                "data_points": [{"current": iv[0], "voltage": iv[1]} for iv in iv_points]
            })

        return full_iv_curves_data

    @handle_refused_connection
    @handle_error_response
    def process_iv_curves(self, file_path=None, iv_curve_data=None):
        """
        **POST** */Module/Generator/ProcessIVCurves*

        Processes any number of full IV Curve measurements, either from a :download:`file template
        <_static/PlantPredict_FullIVCurvesTemplate.xlsx>` or similar data structure. This is used as a pre-processing
        step to module file generation - it returns the extracted electrical characteristics at the set of
        temperature/irradiance conditions corresponding to those of the provided IV Curves. The output data structure
        matches the exact data input structure for :py:meth:`plantpredict.Module.process_key_iv_points`. (The
        methods are meant to be used in succession in order to effectively extract electrical characteristics at STC,
        temperature coefficients, and effective irradiance response from a set of IV curves). Detailed algorithmic
        documentation for this method can be found `here
        <https://plantpredict.com/algorithm/module-file-generator/#processing-full-i-v-curves>`_. See "Example Code"
        below for sample usage.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                If the user is using the Excel template, usage of this method is straightforward:

                .. code-block:: python

                    module = plantpredict.Module()
                    module.process_iv_curves(file_path="path_to_iv_curves_template.xlsx")

                However, the user can also manually construct the data structure and call the method as follows:

                .. code-block:: python

                    input_data = [
                        {
                            "temperature": 25,
                            "irradiance": 1000,
                            "data_points": [
                                {"current": 9.43, "voltage": 0.0},
                                # ... insert at least 40 total IV points ...
                                {"current": 0.0, "voltage": 46.39}
                            ]
                        }
                    ]

                    module.process_iv_curves(iv_curve_data=input_data)

                Which will return a data structure:

                .. code-block:: python

                    [
                        {
                            "temperature": 25,
                            "irradiance": 1000,
                            "short_circuit_current": 9.43,
                            "open_circuit_voltage": 46.39,
                            "mpp_current": 8.9598,
                            "mpp_voltage": 38.1285,
                            "max_power": 341.6237
                        }
                    ]

                Reminder: While only one IV curve is provided in the example, multiply IV curves can be supplied.

        :param file_path: File path to the .xlsx template for Full IV Curves. (At least 40 points are required for each IV curve.)
        :type file_path: str
        :param iv_curve_data: List of dictionaries, each representing an IV curve at a particular temperature/irradiance. (At least 40 points are required for each IV curve.)
        :type iv_curve_data: list dict
        :return: List of dictionaries, each containing extracted module electrical characteristics corresponding to the IV curve provided at a particular temperature/irradiance condition.
        :rtype: list of dict
        """
        # if the input is the .xlsx template, parse it
        if not file_path and not iv_curve_data:
            raise ValueError(
                "Either a file path to the .xslx template for Full IV Curves input or the properly formatted " 
                "JSON-serializable data structure for Key IV Points input must be assigned as input. See the Python "
                "SDK documentation (https://plantpredict-python.readthedocs.io/en/latest/) for more information."
            )
        elif file_path and iv_curve_data:
            raise ValueError("Only one input option may be specified.")

        # if the user specifies a file_path to the .xlsx template, parse it
        elif file_path:
            iv_curve_data = self._parse_full_iv_curves_template(file_path)

        response = requests.post(
            url=self.api.base_url + "/Module/Generator/ProcessIVCurves",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=[convert_json(d, snake_to_camel) for d in iv_curve_data]
        )

        return [convert_json(d, camel_to_snake) for d in json.loads(response.content)]

    @handle_refused_connection
    @handle_error_response
    def generate_iv_curve(self, num_iv_points=100):
        """
        **POST** */Module/Generator/GenerateIVCurve*

        Generates an IV curve given An example of using this method in practice can be found in :ref:`example_usage`.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    cell_technology_type; int; Represents the cell technology type (CdTe, poly c-Si PERC, etc). Use :py:mod:`plantpredict.enumerations.CellTechnologyTypeEnum`.
                    pv_model; int; Represents the 1-diode model type (1-Diode, 1-Diode with recombination). Use :py:mod:`plantpredict.enumerations.PVModelTypeEnum`.
                    number_of_cells_in_series; int; Number of cells in one string of cells - unitless
                    reference_irradiance; float; Must be between :py:data:`400.0` and :py:data:`1361.0` - units :py:data:`[W/m^2]`. The IV curve will represent this irradiance.
                    reference_temperature; float; Must be between :py:data:`-20.0` and :py:data:`80.0` - units :py:data:`[deg-C]`. The IV curve will represent this temperature.
                    stc_max_power; float; Must be between :py:data:`0.0` and :py:data:`1000.0` - units :py:data:`[W]`.
                    stc_short_circuit_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_open_circuit_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_mpp_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`.
                    stc_mpp_voltage; float; Must be between :py:data:`0.4` and :py:data:`1000.0` - units :py:data:`[V]`.
                    stc_power_temp_coef; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    stc_short_circuit_current_temp_coef; float; Must be between :py:data:`-0.3` and :py:data:`2.0` - units :py:data:`[%/deg-C]`.
                    series_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100.0` - units :py:data:`[Ohms]`
                    shunt_resistance_at_stc; float; Must be between :py:data:`0.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    dark_shunt_resistance; float; Must be between :py:data:`100.0` and :py:data:`100000.0` - units :py:data:`[Ohms]`.
                    recombination_parameter; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`30.0`
                    exponential_dependency_on_shunt_resistance; float; Must be between :py:data:`1.0` and :py:data:`100.0` - unitless.
                    bandgap_voltage; float; Must be between :py:data:`0.5` and :py:data:`4.0` - units :py:data:`[V]`.
                    built_in_voltage; float; Required only if :py:attr:`pv_model` is :py:data:`plantpredict.enumerations.PVModelTypeEnum.ONE_DIODE_RECOMBINATION`. Must be between :py:data:`0.0` and :py:data:`3.0` - units :py:data:`[V]`.
                    saturation_current_at_stc; float; Must be between :py:data:`1e-13` and :py:data:`1e-6` - units :py:data:`[A]`.
                    diode_ideality_factor_at_stc; float; Must be between :py:data:`0.1` and :py:data:`5.0` - unitless.
                    linear_temp_dependence_on_gamma; float; Must be between :py:data:`-3.0` and :py:data:`3.0` - units :py:data:`[%/deg-C]`.
                    light_generated_current; float; Must be between :py:data:`0.1` and :py:data:`100.0` - units :py:data:`[A]`

        .. container:: toggle

            .. container:: header

                **Example Output**

            .. container:: example_output

                .. code-block:: python

                    [
                        {"current": 9.43, "voltage": 0.0},
                        # ... list will be equal in length to num_iv_points ...
                        {"current": 0.0, "voltage": 46.39}
                    ]

        :param num_iv_points: Number of IV points to generate (defaults to 100).
        :type num_iv_points: int
        :return: List of IV generated IV points (See "Example Output")
        :rtype: list
        """
        self.num_iv_points = num_iv_points

        return requests.post(
            url=self.api.base_url + "/Module/Generator/GenerateIVCurve",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

    @handle_error_response
    @handle_refused_connection
    def calculate_basic_data_at_conditions(self, temperature, irradiance):
        """

        :return:
        """
        return self.process_iv_curves(iv_curve_data=[{
            "temperature": temperature,
            "irradiance": irradiance,
            "data_points": self.generate_iv_curve()
        }])

    # @handle_error_response
    # @handle_refused_connection
    # def generate_single_diode_parameters_advanced_bulk(self, modules):
    #    """
    #
    #    :param modules:
    #    :return:
    #    """
    #    return requests.post(
    #        url=self.api.base_url + "/Module/Generator/GenerateSingleDiodeParametersAdvancedBulk",
    #        headers={"Authorization": "Bearer " + self.api.access_token},
    #        json=convert_json_list(modules, snake_to_camel)
    #    )

    #@handle_error_response
    #@handle_refused_connection
    #def optimize_series_resistance_bulk(self, modules):
    #    """
    #
    #   :param modules:
    #    :return:
    #    """
    #    return requests.post(
    #        url=self.api.base_url + "/Module/Generator/OptimizeSeriesResistanceBulk",
    #        headers={"Authorization": "Bearer " + self.api.access_token},
    #        json=convert_json_list(modules, snake_to_camel)
    #    )
