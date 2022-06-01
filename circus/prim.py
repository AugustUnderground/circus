""" Primitive Device Models for Design Space transformation """

import numpy as np
import torch as pt
import joblib as jl
from expression import pipe, compose

class PrimitiveDevice:
    """ Primitive Device Model """
    def __init__( self, path: str
                , params_x: [str], params_y: [str]
                , trafo_x: [str] , trafo_y: [str] ):
        """
        Construct Primitive Device Model
        Arguments:
            `path`:     Path must contain `scale.X`, `scale.Y` and `model.pt`.
            `params_x`: List of Input parameters.
            `params_y`: List of Output parameters.
            `trafo_x`:  List of Input parameters that will be transformed.
            `trafo_y`:  List of Output parameters taht will be transformed.
        """
        self.params_x = params_x
        self.params_y = params_y

        self.mask_x   = np.array([int(px in trafo_x) for px in self.params_x])
        self.mask_y   = np.array([int(py in trafo_y) for py in self.params_y])

        self.scaler_x = jl.load(f"{path}/scale.X")
        self.scaler_y = jl.load(f"{path}/scale.Y")
        self.scale_x  = self.scaler_x.transform
        self.scale_y  = self.scaler_y.inverse_transform

        self.trafo_x  = lambda X: (np.log10( np.abs(X)
                                           , where = (np.abs(X) > 0)
                                           ) * self.mask_x
                                  ) + (X * (1 - self.mask_x))
        self.trafo_y  = lambda Y: (np.power(10, Y) * self.mask_y
                                  ) + (Y * (1 - self.mask_y))

        self.model    = pt.jit.load(f"{path}/model.pt").cpu().eval()

    def predict(self, X: np.array) -> np.array:
        """
        Make a Prediciton.
        Arguments:
            `X`: Array of input parameters.
        """
        with pt.no_grad():
            return pipe( X
                       , np.nan_to_num
                       , self.trafo_x
                       , self.scale_x
                       , np.float32
                       , pt.from_numpy
                       , self.model
                       , pt.Tensor.numpy
                       , self.scale_y
                       , self.trafo_y
                       , np.nan_to_num
                       , )
