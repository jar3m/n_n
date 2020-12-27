#!/usr/bin/python3
import json
from ctypes import *
import os

class t_kon(Structure):
    _fields_ = [("val", c_int)]

class t_lyrinfo(Structure):
    _fields_ = [("size", c_int), ("layer_type", c_int), ("actv", c_int)]


class t_nn_cfg(Structure):
    _fields_ = [
        ("type", c_int),
        ("eta", c_float),
        ("n_in", c_int),
        ("n_out", c_int),
        ("oactv", c_int),
        ("n_hdn", c_int),
        ("hinfo", POINTER(t_lyrinfo)),
    ]


class Prometheus(object):
    def __init__(self):
        self.config_file = "iris.json"

    def parse_config(self):
        with open("iris.json") as conf:
            config_dict = json.load(conf)
            print(config_dict)
            config_dict = config_dict["neural_nw_config"]
            hl_props = list(config_dict["hl_prop"])
            print(hl_props)
            for index in range(config_dict["num_hidden_layers"]):
                hl_props[index]["actv_fn"] = "Relu"
            print(hl_props)
            self.num_hlayers = config_dict["num_hidden_layers"]
            self.neural_nw_type = config_dict["neural_nw_type"]
            self.num_input = config_dict["num_input"]
            self.num_output = config_dict["num_output"]


p1 = Prometheus()
p1.parse_config()
neural_nw_library = CDLL(
    "/home/harsha/Blind_Centaur/project/nn/nn_p/n_n/neural_network/bin/neural_network.so"
)
get_nn_config = neural_nw_library.get_nn_config
get_nn_config.restype = POINTER(t_nn_cfg)
# create_nn = neural_nw_library.create_neural_network
# train_nn = neural_nw_library.train_network
# predict_nn = neural_nw_library.predict_network
# destroy_nn = neural_nw_library.destroy_neural_network

conf = get_nn_config(c_int(3), c_float(6.9))
print(conf)
print(conf.contents.eta)
print(conf.contents.type)
print(conf.contents.n_in)
print(conf.contents.n_out)
print(conf.contents.n_hdn)
print(conf.contents.hinfo.contents.size)
