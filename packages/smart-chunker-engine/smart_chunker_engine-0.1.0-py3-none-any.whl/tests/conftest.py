import warnings

def pytest_configure(config):
    warnings.filterwarnings(
        "ignore",
        message=".*force_all_finite.*",
        category=FutureWarning,
        module="sklearn"
    )
    warnings.filterwarnings(
        "ignore",
        message=".*ensure_all_finite.*",
        category=FutureWarning,
        module="sklearn"
    ) 