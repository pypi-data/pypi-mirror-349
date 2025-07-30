import click
from click.testing import CliRunner
from nimmunize.cli import main

runner = CliRunner()


def test_survey_command(tmp_path):
    df_path = tmp_path / "s.csv"
    df_path.write_text("dob,bcg\n2024-01-01,2024-01-01")
    result = runner.invoke(main, ["survey", str(df_path)])
    assert result.exit_code == 0
    assert "coverage_" in result.output
