import re


def decorate_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and attr != '__init__':
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def camel_to_snake(key):
    camel_pat = re.compile(r'([A-Z])')
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), key)


def snake_to_camel(key):
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), key)


MANUAL_KEY_FIXES = {
    "camel_to_snake": {
        "k_m_l": "kml",
        "s_t_c": "stc",
        "STC": "stc",
        "i_a_m": "iam",
        "power_plant": "powerplant",
        "p_o_a": "poa",
        "back_tracking": "backtracking",
        "back_side": "backside",
        "k_v_a": "kva",
        "transformerkva_rating": "transformer_kva_rating",
        "inverterkva": "inverter_kva",
        "usek_v_a": "use_kva_",
        "m_v": "mv",
        "e_s_s": "ess",
        "k_w": "_kw",
        "m_p_p": "mpp",
        "d_c": "dc",
        "p_c_s": "pcs",
        "uiamd": "uiam_d",
        "uiamg": "uiam_g",
        "ashraeiam": "ashrae_iam",
        "stcmpp": "stc_mpp",
        "a_c": "ac",
        "u_t_c": "utc",
        "g_h_i": "ghi",
        "d_h_i": "dhi",
        "d_n_i": "dni",
        "poa_i": "poai",
        "g_c_r": "gcr",
        "bi_faciality": "bifaciality",
        "poairradinace": "global_poa_irradiance",
        "g_teff": "gt_eff",
        "time_stamp": "timestamp",
        "i_v": "iv",
        "po_a_insolation": "poa_insolation",
        "light_generatedcurrent": "light_generated_current",
        "bo_s": "bos",
        "sandiaconductive": "sandia_conductive",
        "sandiaconvective": "sandia_convective",
        "l_i_d": "lid",
        "at25": "at_25",
        "l_g_i_a": "lgia",
        "number_of_conducters_per_phase": "number_of_conductors_per_phase",      # misspelled in PlantPredict backend
        "cool996": "cool_996",
        "heat996": "heat_996",
        "max50_year": "max_50_year",
        "min50_year": "min_50_year",
        "p_q": "pq",
        "kvacurves": "kva_curves",
        "k_va": "kva"
    },
    "snake_to_camel": {
        "powerplant": "powerPlant",
        "backtracking": "backTracking",
        "backsideMismatch": "backSideMismatch",
        "numberOfConductorsPerPhase": "numberOfConductersPerPhase"              # misspelled in PlantPredict backend
    }
}


def convert_json(d, convert_function):
    """
    Convert a nested dictionary from one convention to another. Prepares payload for http request.
    Args:
        d (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.

    """
    # "api" object is not serializable, so remove it from http request
    dict_copy = d.copy()
    dict_copy.pop("api", None)

    new = {}
    for k, v in dict_copy.items():
        new_v = v
        if isinstance(v, dict):
            new_v = convert_json(v, convert_function)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                if isinstance(x, dict):
                    new_v.append(convert_json(x, convert_function))

        new_key = convert_function(k)

        # manual fixes
        for key, val in MANUAL_KEY_FIXES[convert_function.__name__].items():
            if key in new_key:
                if not (key == "d_c" and new_key == "light_generated_current"):       # edge case
                    new_key = new_key.replace(key, val)

        # this removes the underscore given to a snake case when the first character in the camel case is capital
        new_key = new_key[1:] if new_key[0] == "_" else new_key

        new[new_key] = new_v

    return new


def convert_json_list(l, convert_function):
    new_list = []
    for d in l:
        # "api" object is not serializable, so remove it from http request
        dict_copy = d.copy()
        dict_copy.pop("api", None)

        new = {}
        for k, v in dict_copy.items():
            new_v = v
            if isinstance(v, dict):
                new_v = convert_json(v, convert_function)
            elif isinstance(v, list):
                new_v = list()
                for x in v:
                    if isinstance(x, dict):
                        new_v.append(convert_json(x, convert_function))

            new_key = convert_function(k)

            # manual fixes
            for key, val in MANUAL_KEY_FIXES[convert_function.__name__].items():
                if key in new_key:
                    if not (key == "d_c" and new_key == "light_generated_current"):       # edge case
                        new_key = new_key.replace(key, val)

            # this removes the underscore given to a snake case when the first character in the camel case is capital
            new_key = new_key[1:] if new_key[0] == "_" else new_key

            new[new_key] = new_v

        new_list.append(new)

    return new_list
