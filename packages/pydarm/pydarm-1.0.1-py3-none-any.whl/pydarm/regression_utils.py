import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.optimizers.schedules import InverseTimeDecay
import gpflow as gpf
import numpy as np
import os
import matplotlib.pyplot as plt


class EarlyStoppingCallback(tf.keras.callbacks.Callback):
    """
    This class allows GPFlow to interrupt the training
    when the monitored metric (e.g. loss function)
    has stopped improving
    """

    def __init__(
        self,
        model,
        directory,
        monitor="loss",
        patience=0,
        restore_best_weights=True
    ):
        super(EarlyStoppingCallback, self).__init__()
        self.model = model
        self.directory = directory
        self.monitor = monitor
        self.patience = patience
        self.restore_best_weights = restore_best_weights
        self.best_epoch = None
        self.wait = 0
        self.stopped_epoch = 0
        self.best = np.Inf if "loss" in monitor else -np.Inf
        self.continue_training = True

    def monitor_op(self, current, best):
        if "loss" in self.monitor:
            # If the change in loss is very small, don't update best epoch
            diff = best - current
            if diff <= 0.5:
                return False
            else:
                return current < best
        else:
            pass

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if current is None:
            raise ValueError(f"Monitoring metric \
                             '{self.monitor}' is not available.")

        if self.monitor_op(current, self.best):
            self.best_epoch = epoch
            self.best = current
            self.wait = 0
            if self.restore_best_weights:
                if not os.path.exists(self.directory):
                    os.makedirs(self.directory)
                checkpoint = tf.train.Checkpoint(model=self.model)
                checkpoint.save(f'{self.directory}/model.ckpt')
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.continue_training = False
                print(f"Epoch {epoch}: Early stopping")
                if self.restore_best_weights:
                    print(f"Restoring model weights from epoch {self.best_epoch}.")
                    checkpoint = tf.train.Checkpoint(model=self.model)
                    checkpoint.restore(f'{self.directory}/model.ckpt-1')

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            print(f"Epoch {self.stopped_epoch+1}: Early stopping")


def create_GP_model(X, M=100):
    """
    This method creates an SVGP model.
    Citation: https://proceedings.mlr.press/v38/hensman15
    See https://tiao.io/post/sparse-variational-gaussian-processes/

    Parameters
    ----------
    X : array-like (Nx1)
        Frequency array based upon which the inducing
        variables are selected
    M : int (default 100)
        Number of inducing variables for each f_i
        (passing all samples slows down the fit)
    """
    # Likelihood chosen based on the following tutorial for varying-noise data:
    # https://gpflow.github.io/GPflow/2.4.0/notebooks/advanced/heteroskedastic.html
    likelihood = gpf.likelihoods.HeteroskedasticTFPConditional(
        distribution_class=tfp.distributions.Normal,  # Gaussian Likelihood
        # Exponential Transform, since the scale needs to be positive
        scale_transform=tfp.bijectors.Exp()
    )
    k1 = gpf.kernels.SquaredExponential()
    k2 = gpf.kernels.SquaredExponential()
    kernel = gpf.kernels.SeparateIndependent(
        [
            k1,  # This is k1, the kernel of f1
            k2,  # this is k2, the kernel of f2
        ]
    )

    # Initial inducing points position Z
    Z = np.linspace(X.min(), X.max(), num=M)[
        :, None
    ]  # Z must be of shape [M, 1]
    inducing_variable = (
        gpf.inducing_variables.SeparateIndependentInducingVariables(
            [
                gpf.inducing_variables.InducingPoints(Z),  # This is U1 = f1(Z1)
                gpf.inducing_variables.InducingPoints(Z),  # This is U2 = f2(Z2)
            ]
        )
    )
    # Future devs: could use `exact GPR` (i.e. no natural gradient optimisation needed)
    # https://gpflow.github.io/GPflow/2.9.1/api/gpflow/models/gpr/index.html
    model = gpf.models.SVGP(
        kernel=kernel,
        likelihood=likelihood,
        inducing_variable=inducing_variable,
        num_latent_gps=likelihood.latent_dim,
    )
    return model


def make_diagnostic_plot(model,
                         X,
                         Y,
                         epoch,
                         loss_fn,
                         meas,
                         output_dir_diagnostics):
    """
    Make diagnotic plots for specific training epochs.
    The envelope is shown with overlaid training points
    and the value of the loss function is reported.

    Parameters
    ----------
    X : array-like (Nx1)
        Frequency array
    Y: array-like (Nx1)
        Response array
    model: tensor-flow object
        GPFlow model
    epoch: int
        Current epoch
    loss_fn: float
        Value of the current Loss function
    meas: str
        Option between 'mag' or 'phase'
    output_dir_diagnostics: str
        Name of the output folder
    """
    Ymean, Yvar = model.predict_y(X)
    Ymean = Ymean.numpy().squeeze()
    Ystd = tf.sqrt(Yvar).numpy().squeeze()
    # Turning off LaTeX here, since it causes errors on the cluster
    plt.rcParams.update({
            "text.usetex": False
        })
    plt.figure(figsize=(15, 4))
    Xplot = np.exp(X.copy())
    x = Xplot.squeeze()
    lb = (Ymean - Ystd).squeeze()
    ub = (Ymean + Ystd).squeeze()
    plt.fill_between(
        x,
        lb,
        ub,
        color="silver",
        alpha=0.95,
        label="1-sigma uncertainty",
    )
    plt.plot(x, lb, color="silver")
    plt.plot(x, ub, color="silver")
    plt.plot(Xplot, Ymean, color="black")
    plt.scatter(Xplot, Y, color="gray", alpha=0.3, marker='.')
    plt.ylim(-10, 10)
    plt.xlim(10, 5000)
    plt.xscale("log")
    # TODO: add gps time stamp and date to title
    plt.title(f"Epoch {epoch} - Loss: {loss_fn: .4f}")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel(f'TF {meas}')
    plt.legend(loc="best")
    plt.savefig(
        os.path.join(
            output_dir_diagnostics,
            f"diagnostics_plots/log_training_{meas}_epoch{epoch}.png",
        ),
        bbox_inches="tight",
        pad_inches=0.2,
    )
    plt.close()


def train_GP_parameters(X,
                        Y,
                        model,
                        meas,
                        output_dir_diagnostics,
                        patience=5,
                        logging_freq=1,
                        epochs=50,
                        initial_lr=0.1,
                        gamma=0.1,
                        jitter=1e-4):
    """
    Train SVGP model parameters according to the data with
    Natural Gradient and Adam Optimizer. These optimisers
    have themselves hyper-parameters that can be varied.

    Parameters
    ----------
    X : array-like (Nx1)
        Frequency array
    Y: array-like (Nx1)
        Response array
    model: tensor-flow object
        GPFlow model
    meas: str
        Option between 'mag' or 'phase'
    output_dir_diagnostics: str
        Name of the output folder
    patience : int, default 5
        Number of epochs with no improvement after which training will be stopped.
        See https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/EarlyStopping#args
    logging_freq : int, default 1
        GPR training epochs logging frequency, i.e. how often to generate a diagnostic plot.
    epochs : int, default 50
        Maximum number of training epochs to perform.
    initial_lr: float, default 0.1
        Initial learning rate of Adam Optimiser.
        See https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam
    gamma: float, default 0.1
        Fixed `step size' of Natural Gradient.
        See https://gpflow.github.io/GPflow/2.9.1/api/gpflow/optimizers/index.html#gpflow-optimizers-naturalgradient  # noqa E501
        Also see https://arxiv.org/pdf/1803.09151 for a study of `step size` choice.
    jitter: float, default 1e-4
        Amount of jitter to add to the training instance.
        See https://gpflow.github.io/GPflow/develop/api/gpflow/index.html#gpflow-default-jitter
    """
    gpf.utilities.set_trainable(model.q_mu, False)
    gpf.utilities.set_trainable(model.q_sqrt, False)
    data = (X, Y)
    loss_fn = model.training_loss_closure(data)
    variational_vars = [(model.q_mu, model.q_sqrt)]
    natgrad_opt = gpf.optimizers.NaturalGradient(gamma=gamma)

    # Progressively lowers the learning rate, this helps preventing numerical issues
    # See https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/schedules/InverseTimeDecay
    lr = InverseTimeDecay(
        initial_lr,
        decay_steps=1,
        decay_rate=0.5,
        staircase=True)
    adam_vars = model.trainable_variables
    adam_opt = tf.keras.optimizers.legacy.Adam(lr)

    @tf.function
    def optimisation_step():
        natgrad_opt.minimize(loss_fn, variational_vars)
        adam_opt.minimize(loss_fn, adam_vars)
    # Jitter helps preventing numerical instabilities in the covariance matrix
    gpf.config.set_config(gpf.config.Config(jitter=jitter))
    # The patience parameter determines how many epochs to wait for the loss
    # to improve (decrease) before interrupting the training.
    callbacks = [
        EarlyStoppingCallback(
            model, f'{output_dir_diagnostics}/gp_model_{meas}', monitor="loss",
            patience=patience, restore_best_weights=True
        )
    ]
    if output_dir_diagnostics != '.':
        with open(f"{output_dir_diagnostics}/diagnostics_plots/training_log_{meas}.txt", "a") as f:
            f.write(f"Training started for {meas}..\n")
            f.close()
    for epoch in range(1, epochs + 1):
        try:
            optimisation_step()
            # if this is triggered it means the Loss is too unstable (i.e. NaN)
        except tf.errors.InvalidArgumentError:
            if output_dir_diagnostics != '.':
                with open(f"{output_dir_diagnostics}/diagnostics_plots/training_log_{meas}.txt", "a") as f:  # noqa E501
                    f.write(f"Optimisation step failed \
                        because the loss was {loss_fn().numpy()}, setting best_epoch=0\n")
                    f.close()
                return 0
        for callback in callbacks:
            callback.on_epoch_end(
                epoch, logs={"loss": loss_fn().numpy()}
            )  # Update callback state

        if not callbacks[0].continue_training:
            # The stopping condition is reached early if loss function
            # hasn't improved compared to previous epoch
            break
        if epoch % logging_freq == 0 and epoch > 0:
            if output_dir_diagnostics != '.':
                with open(f"{output_dir_diagnostics}/diagnostics_plots/training_log_{meas}.txt", "a") as f:  # noqa E501
                    f.write(f"Epoch {epoch} - Loss: {loss_fn().numpy(): .4f}\n")
                    f.close()
                make_diagnostic_plot(model, X, Y, epoch, loss_fn().numpy(), meas, output_dir_diagnostics)  # noqa E501
    if output_dir_diagnostics != '.':
        with open(f"{output_dir_diagnostics}/diagnostics_plots/training_log_{meas}.txt", "a") as f:
            f.write(f"Done! Best epoch: {epoch-patience} - Loss: {loss_fn().numpy(): .4f}\n")
            f.write("\n")
            f.close()

    return epoch-patience


def quantile_based_sampling(dataset, sample_size):
    """
    Downsamples the full array of Response functions (1000x100)
    to a smaller array of size (sample_sizex100) for GPR fitting.
    This function is not currently in use.
    """
    num_samples, _ = dataset.shape
    # Calculate the quantiles based on the sample size
    # (+2 since we ignore 0 and 1 quantiles)
    quantiles = np.linspace(0, 1, sample_size+2, endpoint=False)[1:]
    # Initialize an empty list to store the downsampled data
    downsampled_data = []
    # Sample from each quantile
    for quantile in quantiles:
        quantile_index = int(quantile * num_samples)
        sampled_data = dataset[quantile_index]
        downsampled_data.append(sampled_data)
    # Concatenate the sampled data along the first axis
    downsampled_data = np.stack(downsampled_data)
    return downsampled_data
