# langxchange/model_maker.py

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Union
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score


class ModelMakerHelper:
    """
    Train and tune a RandomForestRegressor to predict student performance,
    with automatic hyperparameter search to reduce over/under-fitting.

    Example:
        mm = ModelMakerHelper()
        metrics = mm.train(
            df,
            feature_cols=["Score_prev", "Attendance_pct"],
            target_col="Score",
            tune_params={
                "n_estimators": [50, 100, 200],
                "max_depth": [5, 10, 20],
                "min_samples_leaf": [1, 2, 4]
            },
            cv=3
        )
        preds_df = mm.predict(df_new)
    """

    def __init__(
        self,
        random_state: int = 42,
        base_params: Optional[Dict] = None
    ):
        """
        random_state: for reproducibility
        base_params: passed to RandomForestRegressor constructor
        """
        self.random_state = random_state
        self.base_params = base_params or {"n_estimators": 100, "random_state": random_state, "oob_score": True}
        self.model = RandomForestRegressor(**self.base_params)
        self.fitted = False
        self.feature_cols: List[str] = []
        self.target_col: str = ""

    def train(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
        target_col: str,
        test_size: float = 0.2,
        tune_params: Optional[Dict[str, List]] = None,
        cv: int = 3,
        **fit_kwargs
    ) -> Dict[str, Union[float, Dict]]:
        """
        Train the RandomForest model, optionally tuning hyperparameters.

        Args:
          df: DataFrame with your training data.
          feature_cols: List of column names to use as features.
          target_col: Column to predict.
          test_size: Fraction for hold-out set.
          tune_params: If provided, dict of param_grid for GridSearchCV.
          cv: Number of folds for cross-validation.
          fit_kwargs: Extra args to .fit()

        Returns:
          metrics: {
            "mse": float, "r2": float,
            "best_params": dict (if tuning) or {},
            "oob_score": float (if available)
          }
        """
        self.feature_cols = feature_cols
        self.target_col = target_col

        X = df[feature_cols].values
        y = df[target_col].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )

        best_params = {}
        # Hyperparameter tuning
        if tune_params:
            grid = GridSearchCV(
                estimator=self.model,
                param_grid=tune_params,
                cv=cv,
                scoring="neg_mean_squared_error",
                n_jobs=-1
            )
            grid.fit(X_train, y_train)
            self.model = grid.best_estimator_
            best_params = grid.best_params_
        else:
            self.model.fit(X_train, y_train, **fit_kwargs)

        # If we have oob_score available
        oob = getattr(self.model, "oob_score_", None)

        # Evaluate on test set
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2  = r2_score(y_test, y_pred)

        self.fitted = True

        return {
            "mse": mse,
            "r2": r2,
            "oob_score": oob,
            "best_params": best_params
        }

    def predict(
        self,
        df: pd.DataFrame,
        as_dataframe: bool = True
    ) -> Union[np.ndarray, pd.DataFrame]:
        """
        Predict using the trained model. Must call train() first.

        Args:
          df: New DataFrame containing feature_cols.
          as_dataframe: If True, returns df + prediction column.

        Returns:
          np.ndarray or pd.DataFrame with an extra column "pred_<target_col>"
        """
        if not self.fitted:
            raise RuntimeError("ModelMakerHelper: call train() before predict()")

        X_new = df[self.feature_cols].values
        preds = self.model.predict(X_new)

        if as_dataframe:
            out = df.copy().reset_index(drop=True)
            out[f"pred_{self.target_col}"] = preds
            return out

        return preds
