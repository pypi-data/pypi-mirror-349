import unittest
from unittest.mock import patch, mock_open
from clarifai.runners.models.model_builder import (
    ModelBuilder,
    DEFAULT_DOWNLOAD_CHECKPOINT_WHEN,
)

mock_data = """
checkpoints:
  type: huggingface
  repo_id: test_repo
model:
  user_id: test_user
  app_id: test_app
  id: test_model
  model_type_id: test_type
inference_compute_info:
  cpu_limit: "2"
  cpu_memory: "4Gi"
  num_accelerators: 0
"""


class TestModelBuilder(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=mock_data)
    @patch("os.path.exists")
    @patch("os.listdir")
    def test_validate_folder(self, mock_listdir, mock_exists, mock_open_file):
        mock_exists.return_value = True
        mock_listdir.return_value = ["config.yaml", "1", "requirements.txt"]

        builder = ModelBuilder(folder="test_folder", validate_api_ids=False)
        validated_folder = builder._validate_folder("test_folder")
        self.assertIn("test_folder", validated_folder)

    def test_default_download_checkpoint_when(self):
        self.assertEqual(DEFAULT_DOWNLOAD_CHECKPOINT_WHEN, "runtime")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="checkpoints:\n  type: huggingface\n  repo_id: test_repo\n",
    )
    @patch("os.path.exists")
    @patch("yaml.safe_load")
    def test_load_config(self, mock_yaml_load, mock_exists, mock_open_file):
        mock_exists.return_value = True
        mock_yaml_load.return_value = {
            "checkpoints": {"type": "huggingface", "repo_id": "test_repo"}
        }
        config = ModelBuilder._load_config("config.yaml")
        self.assertIn("checkpoints", config)
        self.assertEqual(config["checkpoints"]["type"], "huggingface")

    @patch("shutil.copy")
    @patch("os.path.exists")
    def test_backup_config(self, mock_exists, mock_copy):
        mock_exists.side_effect = [True, False]  # config exists, backup does not
        ModelBuilder._backup_config("config.yaml")
        mock_copy.assert_called_once_with("config.yaml", "config.yaml.bak")

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.safe_dump")
    def test_save_config(self, mock_yaml_dump, mock_open_file):
        config = {"key": "value"}
        ModelBuilder._save_config("config.yaml", config)
        mock_yaml_dump.assert_called_once_with(config, mock_open_file())

    def test_validate_config_model(self):
        builder = ModelBuilder(folder="test_folder", validate_api_ids=False)
        builder.config = {"model": {}}
        try:
            builder._validate_config_model()
        except AssertionError:
            self.fail("_validate_config_model raised AssertionError unexpectedly!")

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_validate_folder_missing_config(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["1", "requirements.txt"]

        builder = ModelBuilder(folder="test_folder", validate_api_ids=False)
        with self.assertRaises(AssertionError):
            builder._validate_folder("test_folder")


if __name__ == "__main__":
    unittest.main()
