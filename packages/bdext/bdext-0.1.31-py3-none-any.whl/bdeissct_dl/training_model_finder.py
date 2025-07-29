import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

from bdeissct_dl import MODEL_FINDER_PATH
from bdeissct_dl.bdeissct_model import MODELS
from bdeissct_dl.model_serializer import save_model_keras, save_scaler_joblib, save_scaler_numpy, load_scaler_numpy
from bdeissct_dl.training import fit_model, get_X_columns, calc_validation_fraction
from bdeissct_dl.tree_encoder import SCALING_FACTOR

BATCH_SIZE = 1024

pd.set_option('display.max_columns', None)

EPOCHS = 10000


def build_model(n_x, n_y, optimizer=None, loss=None, metrics=None):
    """
    Build a FFNN of funnel shape (64-32-16-max(n_y, 8) neurons), and a n_y-neuron output layer (model probabilities).
    We use a 50% dropout.
    This architecture follows teh PhyloDeep paper [Voznica et al. Nature 2022].

    :param n_x: input size (number of features)
    :param optimizer: by default Adam with learning rate of 0.001
    :param loss: loss function, by default categorical crossentropy
    :param metrics: evaluation metrics, by default ['accuracy']
    :return: the model instance: tf.keras.models.Sequential
    """


    model = tf.keras.models.Sequential(name="FFNN_MF")
    model.add(tf.keras.layers.InputLayer(shape=(n_x,), name='input_layer'))
    model.add(tf.keras.layers.Dense(n_y << 4, activation='elu', name=f'layer1_dense{n_y << 4}_elu'))
    model.add(tf.keras.layers.Dropout(0.5, name='dropout1_50'))
    model.add(tf.keras.layers.Dense(n_y << 3, activation='elu', name=f'layer2_dense{n_y << 3}_elu'))
    model.add(tf.keras.layers.Dropout(0.5, name='dropout2_50'))
    model.add(tf.keras.layers.Dense(n_y << 2, activation='elu', name=f'layer3_dense{n_y << 2}_elu'))
    # model.add(tf.keras.layers.Dropout(0.5, name='dropout3_50'))
    model.add(tf.keras.layers.Dense(n_y << 1, activation='elu', name=f'layer4_dense{n_y << 1}_elu'))
    model.add(tf.keras.layers.Dense(n_y, activation='softmax', name=f'output_dense{n_y}_softmax'))
    model.summary()

    if loss is None:
        loss = tf.keras.losses.CategoricalCrossentropy()
    if optimizer is None:
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    if metrics is None:
        metrics = ['accuracy']

    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model


def get_test_data(df=None, path=None):
    if df is None:
        df = pd.read_csv(path)
    feature_columns = get_X_columns(df.columns)
    X = df.loc[:, feature_columns].to_numpy(dtype=float, na_value=0)
    # Standardization of the input features with a standard scaler
    X = load_scaler_numpy(MODEL_FINDER_PATH, suffix='x').transform(X)
    return X


def get_data_characteristics(paths=None, scaler_x=None):
    feature_columns = None
    n_examples = 0
    # First pass: calculate mean and var
    for path in paths:
        df = pd.read_csv(path)
        if feature_columns is None:
            feature_columns = get_X_columns(df.columns)
        X = df.loc[:, feature_columns].to_numpy(dtype=float, na_value=0)
        n_examples += len(df)
        print(X.shape)
        if scaler_x:
            scaler_x.partial_fit(X)
    return feature_columns, n_examples


def get_train_data(labels, paths=None, scaler_x=None, chunk_size=512):

    feature_columns = None

    # second pass: transform X
    for (path, label) in zip(paths, labels):
        for df in pd.read_csv(path, chunksize=chunk_size):
            if feature_columns is None:
                feature_columns = get_X_columns(df.columns)
            X = df.loc[:, feature_columns].to_numpy(dtype=float, na_value=0)
            if scaler_x:
                X = scaler_x.transform(X)
            y_label = np.zeros(len(MODELS), dtype=int)
            if label in MODELS:
                y_label[MODELS.index(label)] = 1
            Y = np.broadcast_to(y_label, (len(df), len(MODELS)))
            yield X, Y


def main():
    """
    Entry point for DL model training with command-line arguments.
    :return: void
    """
    import argparse

    parser = \
        argparse.ArgumentParser(description="Train a BDCT model finder.")
    parser.add_argument('--train_data', nargs='+', type=str,
                        help="paths to the files where the encoded training data "
                             "for each model are stored (all data in one file must correspond to the same epi model)")
    parser.add_argument('--train_labels', nargs='+', type=str, choices=MODELS,
                        help="labels (epi model names) corresponding to the training data files (same order)")
    parser.add_argument('--model_path', required=False, default=MODEL_FINDER_PATH, type=str,
                        help="path to the folder where the trained model should be stored. "
                             "The model will be stored at this path.")
    params = parser.parse_args()

    model_path = params.model_path
    os.makedirs(model_path, exist_ok=True)
    scaler_x = StandardScaler()
    feature_columns, n_examples = get_data_characteristics(paths=params.train_data, scaler_x=scaler_x)
    n_x = len(feature_columns)
    n_y = len(MODELS)

    output_signature = (
        tf.TensorSpec(shape=(None, n_x), dtype=tf.float32),
        tf.TensorSpec(shape=(None, n_y), dtype=tf.int32)
    )

    ds = tf.data.Dataset.from_generator(
        lambda: get_train_data(labels=params.train_labels, paths=params.train_data, scaler_x=scaler_x),
        output_signature=output_signature
    )
    ds = ds.shuffle(buffer_size=10_000)
    # ds = ds.batch(BATCH_SIZE)
    # ds = ds.repeat()
    ds = ds.prefetch(tf.data.AUTOTUNE)

    model = build_model(n_x=n_x, n_y=n_y)

    val_fraction = calc_validation_fraction(n_examples)

    # early stopping to avoid overfitting
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=100)

    # Training of the Network, with an independent validation set
    model.fit(ds, verbose=1, epochs=EPOCHS, validation_split=val_fraction,
              batch_size=BATCH_SIZE, callbacks=[early_stop])

    print(f'Saving the trained model to {model_path}...')

    save_model_keras(model, model_path)
    save_scaler_joblib(scaler_x, model_path, suffix='x')
    save_scaler_numpy(scaler_x, model_path, suffix='x')


if '__main__' == __name__:
    main()
