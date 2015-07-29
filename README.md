# Example for working with the synchronized brainwave dataset

Here's an example, along with a few support libraries, on how to work with data from the [synchronized brainwave dataset](biosense.berkeley.edu/indra_mids_5_15_dlpage/).

## TODO

- Subjects 13-30 don't have readings where we expect them to have readings. Why?

## Core API

`feature_vector_generator(subject_num, time0, time1)`

Returns a generator of feature vectors for the given subject between time0 and time1.

Optionally, this can take a third argument, `sq`, which defines a threshold signal quality to be eligible in a feature vector.

## Notes

Of particular note is lib/featurevectorgenerator.py, which contains most of logic around building feature vectors. (The rest is from @wazaahhh's [brainlib](https://github.com/wazaahhh/brainlib)).

Running example.py requires scikit-learn and numpy, plus dateutil for parsing dates from the source .csv files. You should be able to `pip install` all of these on your platform.
