import pytest
from irish_pipeline.config import load_config

def test_load_config(tmp_path):
    # Create a temporary config file
    cfg = tmp_path / "c.yaml"
    cfg.write_text("foo:1")
    d = load_config(str(cfg))
    assert d["foo"] == 1