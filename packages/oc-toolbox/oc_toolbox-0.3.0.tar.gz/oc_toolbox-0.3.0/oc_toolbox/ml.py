from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def business_cost(
    y: np.ndarray, y_pred: np.ndarray, cost_matrix: Optional[Dict[str, float]] = None
) -> float:
    """
    Computes the total business cost based on a user-defined cost matrix.

    This function calculates the number of true positives (TP), false positives (FP),
    true negatives (TN), and false negatives (FN), then applies the cost matrix
    to determine the overall cost of the model's predictions.

    Parameters
    ----------
    y : np.ndarray
        True binary labels.
    y_pred : np.ndarray
        Predicted binary labels.
    cost_matrix : dict, optional
        Dictionary specifying the cost associated with each prediction type:
        {"TP": float, "FP": float, "TN": float, "FN": float}.
        Default is {"TP": 0, "FP": 1, "TN": 0, "FN": 1}.

    Returns
    -------
    float
        The total business cost of the model's predictions.

    Notes
    -----
    - Useful for modeling scenarios where misclassifications have different consequences.
    - Can be used for cost-sensitive learning or model evaluation.
    """
    if cost_matrix is None:
        cost_matrix = {"TP": 0, "FP": 1, "TN": 0, "FN": 1}

    TP = np.sum((y_pred == 1) & (y == 1))
    FP = np.sum((y_pred == 1) & (y == 0))
    TN = np.sum((y_pred == 0) & (y == 0))
    FN = np.sum((y_pred == 0) & (y == 1))

    total_cost = (
        TP * cost_matrix["TP"]
        + FP * cost_matrix["FP"]
        + TN * cost_matrix["TN"]
        + FN * cost_matrix["FN"]
    )

    return total_cost


def create_cnn_model(
    cnn_model: Optional[str] = "ResNet50",
    data_augmented: Optional[bool] = False,
    density: Optional[int] = 1024,
    dropout: Optional[float] = 0.5,
    input_size: Optional[Tuple[int, int]] = (224, 224),
    num_classes: Optional[int] = 4,
    optimizer: Optional[str] = "adam",
    trainable: Optional[bool] = False,
) -> Any:
    from tensorflow.keras import layers

    _layers = []

    if data_augmented:
        _layers += [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomTranslation(0.1, 0.1),
            layers.RandomContrast(0.1),
            # layers.Rescaling(
            #     1.0 / 127.5,
            #     offset=-1.0,
            # ),
        ]

    if cnn_model == "VGG16":
        from tensorflow.keras.applications.vgg16 import VGG16

        cnn_model_cls = VGG16

    elif cnn_model == "ResNet50":
        from tensorflow.keras.applications.resnet50 import ResNet50

        cnn_model_cls = ResNet50
    else:
        raise ValueError(
            f"Unknown CNN model: {cnn_model}. Supported models are 'VGG16' and 'ResNet50'."
        )

    model0 = cnn_model_cls(
        include_top=False,
        input_shape=(input_size[0], input_size[1], 3),
        weights="imagenet",
    )

    for _l in model0.layers:
        _l.trainable = trainable

    _layers += [
        model0,
        layers.GlobalAveragePooling2D(),
        layers.Dense(density, activation="relu"),
        layers.Dropout(dropout),
        layers.Dense(num_classes, activation="softmax"),
    ]

    from tensorflow.keras.models import Sequential

    model = Sequential(_layers)

    # compilation du modèle
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"],
    )

    return model


class PandasStandardScaler(TransformerMixin):
    """
    A wrapper around StandardScaler that returns a pandas DataFrame
    with preserved column names after scaling.

    This transformer behaves like scikit-learn's StandardScaler, but ensures
    that the output remains a pandas DataFrame with the same column names.

    Parameters
    ----------
    **kwargs : dict
        Additional keyword arguments passed to `sklearn.preprocessing.StandardScaler`.

    Attributes
    ----------
    scaler : StandardScaler
        The underlying scikit-learn scaler.
    feature_names : pd.Index
        The feature names extracted from the input DataFrame.
    is_fitted_ : bool
        Flag indicating whether the scaler has been fitted.
    """

    def __init__(self, **kwargs):
        self.scaler = StandardScaler(**kwargs)

    def fit(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> "PandasStandardScaler":
        """
        Fits the scaler to the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            The input features to scale.
        y : pd.Series, optional
            Not used. Included for compatibility.

        Returns
        -------
        PandasStandardScaler
            The fitted scaler instance.
        """
        self.scaler.fit(X)
        self.feature_names = X.columns
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input DataFrame using the fitted scaler.

        Parameters
        ----------
        X : pd.DataFrame
            The input features to transform.

        Returns
        -------
        pd.DataFrame
            A DataFrame of scaled values with the original column names.
        """
        X_scaled = self.scaler.transform(X)
        return pd.DataFrame(X_scaled, columns=self.feature_names, index=X.index)


class NumericSelector(BaseEstimator, TransformerMixin):
    """
    Transformer that selects only numeric columns from a pandas DataFrame.

    This transformer can be used in a preprocessing pipeline to isolate
    numerical features before applying numerical-specific transformations
    such as scaling or imputation.

    Attributes
    ----------
    numeric_columns : pd.Index
        The names of the numeric columns selected during fitting.
    is_fitted_ : bool
        Indicates whether the transformer has been fitted.
    """

    def fit(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None, **kwargs
    ) -> "NumericSelector":
        """
        Identifies numeric columns in the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame.
        y : pd.Series, optional
            Not used. Included for compatibility with pipelines.
        **kwargs : dict
            Additional arguments (ignored).

        Returns
        -------
        NumericSelector
            The fitted transformer.
        """
        self.numeric_columns = X.select_dtypes(include=[np.number]).columns
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Transforms the input DataFrame by selecting only numeric columns.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame to transform.
        y : pd.Series, optional
            Not used. Included for compatibility with pipelines.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing only the numeric columns.
        """
        return X[self.numeric_columns]


class PandasSimpleImputer(TransformerMixin):
    """
    Wrapper around scikit-learn's SimpleImputer that preserves pandas column names.

    This transformer applies simple imputation (mean, median, most frequent, or constant)
    to missing values and returns a DataFrame instead of a NumPy array, retaining
    the original column names.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments passed to `sklearn.impute.SimpleImputer`.

    Attributes
    ----------
    imputer : SimpleImputer
        The underlying SimpleImputer instance.
    feature_names : pd.Index
        Column names of the input DataFrame.
    is_fitted_ : bool
        Indicates whether the imputer has been fitted.
    """

    def __init__(self, **kwargs):
        self.imputer = SimpleImputer(**kwargs)

    def fit(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> "PandasSimpleImputer":
        """
        Fits the SimpleImputer to the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            Input features with possible missing values.
        y : pd.Series, optional
            Not used. Included for pipeline compatibility.

        Returns
        -------
        PandasSimpleImputer
            The fitted imputer.
        """
        self.imputer.fit(X)
        self.feature_names = X.columns
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input DataFrame by imputing missing values.

        Parameters
        ----------
        X : pd.DataFrame
            Input features to transform.

        Returns
        -------
        pd.DataFrame
            A new DataFrame with imputed values and original column names.
        """
        X_imputed = self.imputer.transform(X)
        return pd.DataFrame(X_imputed, columns=self.feature_names, index=X.index)


class ThresholdClassifier(BaseEstimator, ClassifierMixin):
    """
    Wrapper classifier that applies a custom decision threshold on the predicted probabilities.

    This meta-classifier wraps a base binary classifier and overrides its default threshold
    of 0.5 for classifying instances. It is useful when optimizing for business constraints
    such as precision, recall, or cost-based decisions.

    Parameters
    ----------
    base_model : ClassifierMixin
        A fitted scikit-learn compatible binary classifier with a `predict_proba` method.
    threshold : float, optional
        The probability threshold to classify instances as positive (default is 0.5).

    Attributes
    ----------
    is_fitted_ : bool
        Indicates whether the model has been fitted.
    """

    def __init__(
        self, base_model: Optional[ClassifierMixin] = None, threshold: float = 0.5
    ):
        self.base_model = base_model
        self.threshold = threshold

    def fit(self, X, y=None):
        """
        Fits the base model to the training data.

        Parameters
        ----------
        X : array-like
            Training features.
        y : array-like
            Target labels.

        Returns
        -------
        self : ThresholdClassifier
            The fitted classifier.
        """
        self.base_model.fit(X, y)
        self.is_fitted_ = True
        return self

    def predict(self, X) -> np.ndarray:
        """
        Predicts binary class labels using the custom threshold.

        Parameters
        ----------
        X : array-like
            Input features to classify.

        Returns
        -------
        numpy.ndarray
            Binary predictions (0 or 1) based on the specified threshold.
        """
        proba = self.base_model.predict_proba(X)[:, 1]
        return (proba >= self.threshold).astype(int)

    def predict_proba(self, X) -> np.ndarray:
        """
        Returns predicted probabilities from the base model.

        Parameters
        ----------
        X : array-like
            Input features.

        Returns
        -------
        numpy.ndarray
            Probabilities for both classes (shape: [n_samples, 2]).
        """
        return self.base_model.predict_proba(X)

    def get_params(self, deep: bool = True) -> dict:
        """
        Returns parameters for this estimator.

        Parameters
        ----------
        deep : bool, optional
            Whether to return parameters of nested objects (default: True).

        Returns
        -------
        dict
            Parameters of the classifier.
        """
        return {"base_model": self.base_model, "threshold": self.threshold}

    def set_params(self, **params):
        """
        Sets parameters for this estimator.

        Parameters
        ----------
        **params : dict
            Parameter names mapped to their new values.

        Returns
        -------
        self : ThresholdClassifier
            The updated classifier.
        """
        for param, value in params.items():
            setattr(self, param, value)
        return self
