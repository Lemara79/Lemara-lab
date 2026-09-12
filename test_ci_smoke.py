import os
from idlelib.iomenu import encoding

import yaml

def test_yaml_file_exists():
    """验证YAML文件存在"""
    current_dir=os.path.dirname(os.path.abspath(__file__))
    yaml_path=os.path.join(current_dir,"test_data.yaml")
    assert os.path.exists(yaml_path),f"YAML文件不存在:{yaml_path}"

def test_load_test_data():
    """验证能正确读取YAML数据"""
    current_dir=os.path.dirname(os.path.abspath(__file__))
    yaml_path=os.path.join(current_dir,"test_data.yaml")
    with open(yaml_path,"r",encoding="utf-8") as f:
        data=yaml.safe_load(f)
    assert "login_test_data" in data
    assert len(data["login_tset_data"])>0