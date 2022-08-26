from modules.pre_processing.sample.ratio_sample import ratio_sample
from modules.pre_processing.sample.size_sample import size_sample
from modules.pre_processing.sample.stratified_ratio_sample import stratified_ratio_sample
from modules.pre_processing.sample.stratified_size_sample import stratified_size_sample
from modules.pre_processing.sample.weight_sample import weight_sample


def test_ratio_sample():
    params = {"params.input.1.dir": "./data/6001.pickle", "params.output.dir": "./data/ratio_sample",
              "params.ratio": "0.5",
              "params.withReplacement": "True"}
    ratio_sample(params)


def test_size_sample():
    params = {"params.input.1.dir": "./data/6001.pickle", "params.output.dir": "./data/size_sample", "params.size": "2",
              "params.withReplacement": "True"}
    size_sample(params)


def test_stratified_ratio_sample():
    params = {"params.input.1.dir": "./data/6001.pickle", "params.output.dir": "./data/stratified_ratio_sample",
              "params.strataRatios": "M:0.5,F:0.5",
              "params.withReplacement": "True", "params.strataCol": "gender"}
    stratified_ratio_sample(params)


def test_stratified_size_sample():
    params = {"params.input.1.dir": "./data/6001.pickle", "params.output.dir": "./data/stratified_size_sample",
              "params.strataSizes": "M:2,F:1",
              "params.withReplacement": "True", "params.strataCol": "gender"}
    stratified_size_sample(params)


def test_weight_sample():
    params = {"params.input.1.dir": "./data/6001.pickle", "params.output.dir": "./data/weight_sample",
              "params.ratio": "0.5",
              "params.weightCol": "age"}
    weight_sample(params)


if __name__ == '__main__':
    test_ratio_sample()
    test_size_sample()
    test_stratified_ratio_sample()
    test_stratified_size_sample()
    test_weight_sample()
