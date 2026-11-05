from io import StringIO
import pytest
from src.data_loader import load_csv, DatasetValidationError

def test_load_csv_standardises_headers():
    df=load_csv(StringIO("Job Title,Skills Required,Location\nAnalyst,Python; SQL,Pune\n"))
    assert {"title","skills","city"}.issubset(df.columns)

def test_empty_csv_is_explained():
    with pytest.raises(DatasetValidationError, match="empty"):
        load_csv(StringIO(""))

def test_missing_analysis_columns_is_explained():
    with pytest.raises(DatasetValidationError, match="recognised"):
        load_csv(StringIO("foo,bar\n1,2\n"))
