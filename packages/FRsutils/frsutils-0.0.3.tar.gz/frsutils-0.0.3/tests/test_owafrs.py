# import numpy as np

# import sys
# import os
# import syntetic_data_for_tests as sds

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FRsutils/core')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FRsutils/core/models')))

# from owafrs import OWAFRS
# import tnorms as tn
# import implicators as imp


# def test_owafrs_approximations_reichenbach_imp_product_tnorm():
#     data_dict = sds.syntetic_dataset_factory().ITFRS_testing_dataset()
#     # expected_lowerBound = data_dict["Reichenbach_lowerBound"]
#     # expected_upperBound = data_dict["prod_tn_upperBound"]
#     sim_matrix = data_dict["sim_matrix"]
#     y = data_dict["y"]

#     model = OWAFRS(sim_matrix,
#                      y, 
#                      tnorm=tn.tn_product, 
#                      implicator=imp.imp_reichenbach,
#                      lower_app_weights_method = 'inf_weights_linear',
#                      upper_app_weights_method = 'sup_weights_linear')
#     lower = model.lower_approximation()
#     upper = model.upper_approximation()

#     assert lower.shape == (5,)
#     assert upper.shape == (5,)
#     assert np.all((0.0 <= lower) & (lower <= 1.0))
#     assert np.all((0.0 <= upper) & (upper <= 1.0))

#     closeness_LB = np.isclose(lower, expected_lowerBound)
#     assert np.all(closeness_LB), "outputs are not the expected values"

#     closeness_UB = np.isclose(upper, expected_upperBound)
#     assert np.all(closeness_UB), "outputs are not the expected values"