"""
Tests of the application view
"""
import pathlib
import shutil
from unittest.mock import patch

from pytest import fixture

from apps.applications import views as applications_views


@fixture
def application_files_dir(tmp_path) -> pathlib.Path:
    """
    A collection of real application files
    """
    try:
        app = tmp_path / "app"
        app.mkdir()
        (app / "jobbergate.py").write_text("1 + 1")
        (app / "jobbergate.yaml").write_text("{'config': 'world'}")
        templates = app / "templates"
        templates.mkdir()
        (templates / "java-generic-template.j2").write_text("# hello")
        (templates / "starccm-generic-template.j2").write_text("# hello")
        yield tmp_path
    finally:
        shutil.rmtree(tmp_path)


def test_tardir(application_files_dir: pathlib.Path):
    """
    Do we preserve a tar directory structure as we're packaging?
    """
    app = application_files_dir / "app"
    with patch('apps.applications.views.TEMP_DIR', str(app)):
        tf = applications_views.tardir(
            path=str(app),
            tar_name=str(application_files_dir / "test.tar.gz"),
        )
    reopened = tf.open(tf.name, "r|gz")
    assert reopened.getnames() == [
        "",
        "jobbergate.py",
        "jobbergate.yaml",
        "templates",
        "templates/java-generic-template.j2",
        "templates/starccm-generic-template.j2",
    ]
