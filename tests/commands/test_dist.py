import os
import json
from visivo.commands.dist import dist
from visivo.parsers.file_names import PROJECT_FILE_NAME
from visivo.commands.utils import create_file_database
from click.testing import CliRunner
from tests.support.utils import temp_yml_file, temp_folder
from tests.factories.model_factories import ProjectFactory

runner = CliRunner()


def test_dist():
    output_dir = temp_folder()
    project = ProjectFactory()

    create_file_database(url=project.sources[0].url(), output_dir=output_dir)
    tmp = temp_yml_file(
        dict=json.loads(project.model_dump_json()), name=PROJECT_FILE_NAME
    )
    working_dir = os.path.dirname(tmp)

    response = runner.invoke(
        dist, ["-w", working_dir, "-o", output_dir, "-s", "source"]
    )

    assert "Created dist folder" in response.output
    assert response.exit_code == 0
    assert os.path.exists(f"dist/data/trace/data.json")
    assert os.path.exists(f"dist/data/error.json")
    assert os.path.exists(f"dist/data/project.json")
    with open("dist/data/project.json") as project_json:
        assert '"created_at"' in project_json.read()
