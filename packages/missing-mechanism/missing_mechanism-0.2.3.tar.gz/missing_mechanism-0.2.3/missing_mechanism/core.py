import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.impute import MissingIndicator, SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression


def impute_simple(df, column, method='mean'):
    if method == 'mean':
        df[column] = df[column].fillna(df[column].mean())
    elif method == 'median':
        df[column] = df[column].fillna(df[column].median())
    else:
        df[column] = df[column].fillna(df[column].mode()[0])
    return df

def impute_predictive(df, column, model_type='regressor'):
    known = df[df[column].notnull()]
    unknown = df[df[column].isnull()]
    X_train = known.drop(columns=[column])
    y_train = known[column]
    X_pred = unknown.drop(columns=[column])

    X_train = X_train.select_dtypes(include=[int, float])
    X_pred = X_pred.select_dtypes(include=[int, float])

    model = RandomForestRegressor() if model_type == 'regressor' else RandomForestClassifier()

    if not X_train.empty and not X_pred.empty:
        model.fit(X_train, y_train)
        df.loc[df[column].isnull(), column] = model.predict(X_pred)
    else:
        df[column] = df[column].fillna(df[column].mode()[0])
    return df

def impute_mice(df, column):
    known = df[df[column].notnull()]
    unknown = df[df[column].isnull()]
    X_train = known.drop(columns=[column])
    y_train = known[column]
    X_pred = unknown.drop(columns=[column])

    X_train = X_train.select_dtypes(include=[int, float])
    X_pred = X_pred.select_dtypes(include=[int, float])

    model = LinearRegression()
    if not X_train.empty and not X_pred.empty:
        model.fit(X_train, y_train)
        df.loc[df[column].isnull(), column] = model.predict(X_pred)
    else:
        df[column] = df[column].fillna(df[column].mode()[0])
    return df

def identify_missing_mechanism(df, columns_to_ignore=[], low_threshold=5, high_threshold=20, prefer='mean'):
    report = []

    df = df.drop(columns=columns_to_ignore, errors='ignore')

    for column in df.columns:
        if df[column].isnull().sum() == 0:
            continue

        missing_count = df[column].isnull().sum()
        total = len(df[column])
        missing_percent = (missing_count / total) * 100

        try:
            chi2, p_value, _, _ = chi2_contingency(pd.crosstab(df[column].isnull(), columns='count'))
        except:
            p_value = 0.0

        mechanism = "MCAR" if p_value > 0.05 else "MAR/MNAR"
        method_used = None

        try:
            if mechanism == "MCAR" and missing_percent <= low_threshold:
                df = impute_simple(df, column, method=prefer)
                method_used = f"Simple-{prefer}"
            elif mechanism == "MAR/MNAR" and missing_percent > high_threshold:
                model_type = 'regressor' if pd.api.types.is_numeric_dtype(df[column]) else 'classifier'
                df = impute_predictive(df, column, model_type=model_type)
                method_used = f"Predictive-{model_type}"
            elif pd.api.types.is_numeric_dtype(df[column]) and missing_percent > high_threshold:
                df = impute_mice(df, column)
                method_used = "MICE"
            else:
                df = impute_simple(df, column, method=prefer)
                method_used = f"Fallback-Simple-{prefer}"
        except Exception as e:
            print(f"❌ Error in imputation for {column}: {e}")
            method_used = "Error-Fallback"
            df[column] = df[column].fillna(df[column].mode()[0])

        report.append({
            'Column': column,
            'Missing Count': missing_count,
            'Missing %': round(missing_percent, 2),
            'Mechanism': mechanism,
            'Imputation Method': method_used
        })

        print(f"📊 Column: {column}")
        print(f"   → Missing: {missing_count} ({missing_percent:.2f}%)")
        print(f"   → Mechanism: {mechanism}")
        print(f"   → Imputation Method: {method_used}")

    report_df = pd.DataFrame(report)
    report_df.to_csv("mechanism_report.csv", index=False)
    print("✅ Mechanism analysis report saved as 'mechanism_report.csv'.")

    return df 
