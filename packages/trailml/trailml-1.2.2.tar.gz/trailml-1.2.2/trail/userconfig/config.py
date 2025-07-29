import yaml

from trail.exception.config import InvalidConfigurationError


class Config:
    def __init__(self, path, parent, config):
        self.path = path
        self.parent = parent
        self.config = config

    def __getattr__(self, key):
        key = self._snake_to_camel(key)

        try:
            return self.config[key]
        except KeyError as e:
            raise InvalidConfigurationError(
                self._get_missing_option_message(key)
            ) from e

    def save(self):
        if self.parent:
            self.parent.save()
        else:
            with open(self.path, "w") as f:
                yaml.dump(self.config, f, sort_keys=False)

    def _get_missing_option_message(self, key):
        return (
            f"Configuration option '{key}' required but not found. "
            f"Refer to README.md to learn more about required options."
        )

    @staticmethod
    def _snake_to_camel(snake):
        parts = snake.split("_")

        return parts[0] + "".join(i.capitalize() for i in parts[1:])


class MainConfig(Config):
    def __init__(self, config_path, config=None):
        if config is None:
            config = {}

        super().__init__(path=config_path, parent=None, config=config)

    @staticmethod
    def from_file(config_path: str):
        with open(config_path, "r") as f:
            try:
                config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise InvalidConfigurationError(
                    f"Error loading configuration file: {e}"
                ) from e

            return MainConfig(config_path, config=config)

    def merge(self, project_id, parent_experiment_id):
        project_config = self.config["projects"]
        if project_id:
            project_config["id"] = project_id
        if parent_experiment_id:
            project_config["parentExperimentId"] = parent_experiment_id

    def project(self):
        if "projects" not in self.config:
            self.config["projects"] = {}

        return ProjectConfig(
            path=self.path, parent=self, config=self.config["projects"]
        )


class ProjectConfig(Config):
    def update_parent_experiment_id(self, parent_experiment_id):
        self.config["parentExperimentId"] = parent_experiment_id
        self.save()

    def _get_missing_option_message(self, key):
        return (
            f"Configuration option '{key}' in project '{self.alias}' "
            f"required but not found. "
            f"Refer to README.md to learn more about required options."
        )
