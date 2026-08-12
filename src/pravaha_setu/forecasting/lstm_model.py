"""LSTM-based rainfall-runoff inflow forecaster for Koyna, Warna, and
Radhanagari.

Reference: Kratzert, F. et al. (2018). Rainfall-runoff modelling using
Long Short-Term Memory (LSTM) networks. Hydrol. Earth Syst. Sci., 22,
6005-6022. https://doi.org/10.5194/hess-22-6005-2018

See also: García-Feal, O. et al. (2022), comparing ML techniques
(including LSTM) for reservoir outflow forecasting.
https://doi.org/10.5194/nhess-22-3859-2022

TODO (Module 3): implement a PyTorch LSTM model, training loop, and Optuna
hyperparameter tuning. Consider the NeuralHydrology library before building
the training pipeline from scratch (see CLAUDE.md > Tech stack).
"""
