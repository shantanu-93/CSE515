"""
Multimedia Web Databases - Fall 2019: Project Group 17
Authors:
1. Sumukh Ashwin Kamath
2. Rakesh Ramesh
3. Baani Khurana
4. Karishma Joseph
5. Shantanu Gupta
6. Kanishk Bashyam

This is a module for performing dimensionality reduction on images
"""
import time

import numpy as np
from sklearn.decomposition import NMF

from classes.global_constants import GlobalConstants
from classes.mongo import MongoWrapper


class DimensionReduction:
    """
    Class for performing Dimensionality Reduction
    """
    def __init__(self, extractor_model, dimension_reduction_model, k_value):
        self.constants = GlobalConstants()
        self.mongo_wrapper = MongoWrapper(self.constants.Mongo().DB_NAME)
        self.extractor_model = extractor_model
        self.dimension_reduction_model = dimension_reduction_model
        self.k_value = k_value
        pass

    def get_object_feature_matrix(self):
        vector_list = []
        cursor = self.mongo_wrapper.find(self.extractor_model.lower(), {}, {'_id': 0})
        if self.extractor_model == 'LBP':
            for rec in cursor:
                vector_list.append(rec['featureVector'].split(','))
            return np.array(vector_list).astype(np.float)
        else:
            for rec in cursor:
                vector_list.append(rec['featureVector'])
            return np.array(vector_list)

    def execute(self):
        """Performs dimensionality reduction"""
        return getattr(DimensionReduction, self.dimension_reduction_model.lower())(self)

    def pca(self):
        pass

    def svd(self):
        pass

    def nmf(self):
        constants = self.constants.Nmf()
        data = self.get_object_feature_matrix()
        if data is not None:
            model = NMF(n_components=self.k_value, beta_loss=constants.BETA_LOSS_FROB
                        , init=constants.INIT_MATRIX, random_state=0)
            w = model.fit_transform(data)
            h = model.components_
            tt1 = time.time()
            for i in range(h.shape[0]):
                print("Latent Feature: {}\n{}".format(i + 1, sorted(((i, v) for i, v in enumerate(h[i])),
                                                                    key=lambda x: x[1], reverse=True)))

            print("\n\nTime Taken for NMF {}\n".format(time.time() - tt1))
            return w, h

    def lda(self):
        pass