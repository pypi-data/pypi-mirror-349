import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

from bdeissct_dl import MODEL_PATH
from bdeissct_dl.bdeissct_model import MODEL2TARGET_COLUMNS, QUANTILES, LA, PSI, UPSILON, X_C, KAPPA, F_E, F_S, \
    X_S, TARGET_COLUMNS_BDCT, PI_E, PI_I, PI_S, PI_IC, PI_SC, PI_EC
from bdeissct_dl.model_serializer import save_model_keras, save_scaler_joblib, save_scaler_numpy
from bdeissct_dl.pinball_loss import MultiQuantilePinballLoss
from bdeissct_dl.tree_encoder import SCALING_FACTOR, STATS

BATCH_SIZE = 4096

pd.set_option('display.max_columns', None)

EPOCHS = 10000


FEATURE_COLUMNS = [_ for _ in STATS if _ not in {'n_trees', 'n_tips', 'n_inodes', 'len_forest',
                                                 LA, PSI,
                                                 UPSILON, X_C, KAPPA,
                                                 F_E,
                                                 F_S, X_S,
                                                 PI_E, PI_I, PI_S,
                                                 PI_EC, PI_IC, PI_SC,
                                                 SCALING_FACTOR}]


def build_model(n_x, n_y=4, optimizer=None, loss=None, metrics=None, quantiles=QUANTILES):
    """
    Build a FFNN of funnel shape (64-32-16-8 neurons), and a 4-neuron output layer (BD-CT unfixed parameters).
    We use a 50% dropout after each internal layer.
    This architecture follows teh PhyloDeep paper [Voznica et al. Nature 2022].

    :param n_x: input size (number of features)
    :param optimizer: by default Adam with learning rate 0f 0.001
    :param loss: loss function, by default MAPE
    :param metrics: evaluation metrics, by default ['accuracy', 'mape']
    :return: the model instance: tf.keras.models.Sequential
    """


    model = tf.keras.models.Sequential(name="FFNN")
    n_q = len(quantiles)
    n_out = n_y * n_q
    model.add(tf.keras.layers.InputLayer(shape=(n_x,), name='input_layer'))
    model.add(tf.keras.layers.Dense(n_out << 4, activation='elu', name=f'layer1_dense{n_out << 4}_elu'))
    model.add(tf.keras.layers.Dropout(0.5, name='dropout1_50'))
    model.add(tf.keras.layers.Dense(n_out << 3, activation='elu', name=f'layer2_dense{n_out << 3}_elu'))
    model.add(tf.keras.layers.Dropout(0.5, name='dropout2_50'))
    model.add(tf.keras.layers.Dense(n_out << 2, activation='elu', name=f'layer3_dense{n_out << 2}_elu'))
    # model.add(tf.keras.layers.Dropout(0.5, name='dropout3_50'))
    model.add(tf.keras.layers.Dense(n_out << 1, activation='elu', name=f'layer4_dense{n_out << 1}_elu'))
    model.add(tf.keras.layers.Dense(n_out, activation='linear', name=f'output_dense{n_out}_linear'))
    model.summary()

    if loss is None:
        loss = MultiQuantilePinballLoss(quantiles)
    if optimizer is None:
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    if metrics is None:
        metrics = ['accuracy']

    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model


def calc_validation_fraction(m):
    if m <= 1e4:
        return 0.2
    elif m <= 1e5:
        return 0.1
    return 0.01


def get_X_columns(columns):
    return FEATURE_COLUMNS


def get_test_data(dfs=None, paths=None, scaler_x=None):
    if not dfs:
        dfs = [pd.read_csv(path) for path in paths]
    feature_columns = get_X_columns(dfs[0].columns)

    Xs, SFs = [], []
    for df in dfs:
        SFs.append(df.loc[:, SCALING_FACTOR].to_numpy(dtype=float, na_value=0))
        Xs.append(df.loc[:, feature_columns].to_numpy(dtype=float, na_value=0))

    X = np.concat(Xs, axis=0)
    SF = np.concat(SFs, axis=0)

    # Standardization of the input features with a standard scaler
    if scaler_x:
        X = scaler_x.transform(X)

    return X, SF


def get_data_characteristics(paths=None, target_columns=TARGET_COLUMNS_BDCT, scaler_x=None, scaler_y=None):
    feature_columns = None
    n_examples = 0
    # First pass: calculate mean and var
    for path in paths:
        df = pd.read_csv(path)
        if feature_columns is None:
            feature_columns = get_X_columns(df.columns)
        X = df.loc[:, feature_columns].to_numpy(dtype=float, na_value=0)
        Y = df.loc[:, target_columns].to_numpy(dtype=float, na_value=0)
        n_examples += len(df)
        print(X.shape, Y.shape)
        if scaler_x:
            scaler_x.partial_fit(X)
        if scaler_y:
            scaler_y.partial_fit(Y)
    return feature_columns, n_examples


def get_train_data(paths=None, target_columns=TARGET_COLUMNS_BDCT, scaler_x=None, scaler_y=None, chunk_size=512):
    feature_columns = None
    # second pass: transform X, Y
    for path in paths:
        for df in pd.read_csv(path, chunksize=chunk_size):
            if feature_columns is None:
                feature_columns = get_X_columns(df.columns)
            X = df.loc[:, feature_columns].to_numpy(dtype=float, na_value=0)
            if scaler_x:
                X = scaler_x.transform(X)
            Y = df.loc[:, target_columns].to_numpy(dtype=float, na_value=0)
            if scaler_y:
                Y = scaler_y.transform(Y)
            yield X, Y


def main():
    """
    Entry point for DL model training with command-line arguments.
    :return: void
    """
    import argparse

    parser = \
        argparse.ArgumentParser(description="Train a BDCT model.")
    parser.add_argument('--train_data', type=str, nargs='+',
                        help="path to the file where the encoded training data are stored")
    parser.add_argument('--model_name', required=True, type=str,
                        help="model name")
    parser.add_argument('--model_path', required=False, default=MODEL_PATH, type=str,
                        help="path to the folder where the trained model should be stored. "
                             "The model will be stored at this path in the folder corresponding to the model name.")
    params = parser.parse_args()

    model_path = os.path.join(params.model_path, params.model_name)

    os.makedirs(model_path, exist_ok=True)
    scaler_x, scaler_y = StandardScaler(), StandardScaler() #MinMaxScaler()
    target_columns = MODEL2TARGET_COLUMNS[params.model_name]
    feature_columns, n_examples = get_data_characteristics(paths=params.train_data, target_columns=target_columns,
                                                           scaler_x=scaler_x, scaler_y=scaler_y)
    n_x = len(feature_columns)
    n_y = len(target_columns)

    output_signature = (
        tf.TensorSpec(shape=(None, n_x), dtype=tf.float32),
        tf.TensorSpec(shape=(None, n_y), dtype=tf.int32)
    )

    ds = tf.data.Dataset.from_generator(
        lambda: get_train_data(paths=params.train_data, target_columns=target_columns,
                               scaler_x=scaler_x, scaler_y=scaler_y),
        output_signature=output_signature
    )
    ds = ds.shuffle(buffer_size=10_000)
    # ds = ds.batch(BATCH_SIZE)
    # ds = ds.repeat()
    ds = ds.prefetch(tf.data.AUTOTUNE)

    model = build_model(n_x=n_x, n_y=n_y)

    val_fraction=calc_validation_fraction(n_examples)

    #early stopping to avoid overfitting
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=100)

    #Training of the Network, with an independent validation set
    model.fit(ds, verbose=1, epochs=EPOCHS, validation_split=val_fraction,
              batch_size=BATCH_SIZE, callbacks=[early_stop])

    print(f'Saving the trained model to {model_path}...')

    save_model_keras(model, model_path)
    save_scaler_joblib(scaler_x, model_path, suffix='x')
    save_scaler_numpy(scaler_x, model_path, suffix='x')
    save_scaler_joblib(scaler_y, model_path, suffix='y')
    save_scaler_numpy(scaler_y, model_path, suffix='y')


if '__main__' == __name__:
    main()
