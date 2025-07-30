"""
Command-line interface for nimmunize.
"""

import click
from datetime import datetime

from .schedule import next_due, overdue, reference
from .catchup import plan as catchup_plan
from .survey import (
    load,
    audit,
    metrics,
    list_missed,
    list_complete,
    route_coverage,
    disease_coverage,
    diseases_at_risk,
)


@click.group()
def main():
    """nimmunize: schedule, survey, catchup, audit & metrics CLI."""
    pass


# ─── Survey / Audit ──────────────────────────────────────────────────────────
@main.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option("--outfile", "-o", type=click.Path(), help="Save annotated CSV")
def survey(infile, outfile):
    """
    Audit a survey CSV/Excel: adds missed_*, delay_*, next_due_* columns
    and prints coverage metrics if no outfile is given.
    """
    df = load(infile)
    audited = audit(df)
    if outfile:
        audited.to_csv(outfile, index=False)
        click.echo(f"Annotated data written to {outfile}")
    else:
        click.echo(audited.to_string(index=False))
        click.echo("\nCoverage metrics:")
        click.echo(metrics(audited))


@main.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option("-a", "--antigen", type=str, help="Filter to missed_<ANTIGEN> only")
def missed(infile, antigen):
    """
    List individuals with any missed dose (or only MISSED_<ANTIGEN>).
    """
    df = audit(load(infile))
    miss = list_missed(df, antigen)
    click.echo(miss.to_csv(index=False))


@main.command()
@click.argument("infile", type=click.Path(exists=True))
def complete(infile):
    """
    List individuals fully immunised (no missed doses).
    """
    df = audit(load(infile))
    comp = list_complete(df)
    click.echo(comp.to_csv(index=False))


@main.command()
@click.argument("infile", type=click.Path(exists=True))
def stats(infile):
    """
    Print coverage metrics, route & disease coverage, and diseases at risk.
    """
    df = audit(load(infile))
    m = metrics(df)
    rc = route_coverage(df)
    dc = disease_coverage(df)
    risk = diseases_at_risk(df)
    click.echo(f"Overall coverage: {m['coverage_%']}")
    click.echo(f"Fully immunised (FIC): {m['FIC_%']:.1f}%")
    click.echo(f"Median delays (days): {m['median_delay_days']}")
    click.echo(f"Route coverage: {rc}")
    click.echo(f"Disease coverage: {dc}")
    click.echo(f"Diseases at risk (<80%): {risk}")


# ─── Schedule helpers ─────────────────────────────────────────────────────────
@main.command()
@click.argument("dob", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option(
    "-t",
    "--taken",
    multiple=True,
    nargs=2,
    type=(str, click.DateTime(formats=["%Y-%m-%d"])),
    help="Antigen and date taken, e.g. -t bcg 2024-01-01",
)
@click.option(
    "--as-of",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Reference date (YYYY-MM-DD)",
)
@click.option(
    "--include-details", is_flag=True, help="Include dosage, route & diseases prevented"
)
def nextdose(dob, taken, as_of, include_details):
    """
    Show next due date for each antigen.
    """
    taken_dict = {}
    for antigen, dt_obj in taken:
        taken_dict.setdefault(antigen.lower(), []).append(dt_obj.date())
    nd = next_due(
        dob.date(),
        taken_dict,
        as_of=as_of.date() if as_of else None,
        include_details=include_details,
    )
    for ag, info in nd.items():
        click.echo(f"{ag}: {info}")


@main.command()
@click.argument("dob", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option(
    "-t",
    "--taken",
    multiple=True,
    nargs=2,
    type=(str, click.DateTime(formats=["%Y-%m-%d"])),
    help="Antigen and date taken",
)
@click.option(
    "--as-of", type=click.DateTime(formats=["%Y-%m-%d"]), help="Reference date"
)
def catchup(dob, taken, as_of):
    """
    Generate a WHO-style catch-up schedule for each antigen.
    """
    taken_dict = {}
    for antigen, dt_obj in taken:
        taken_dict.setdefault(antigen.lower(), []).append(dt_obj.date())
    plan_dict = catchup_plan(
        dob.date(), taken_dict, as_of=as_of.date() if as_of else None
    )
    for ag, dates in plan_dict.items():
        dates_str = ", ".join(str(d) for d in dates)
        click.echo(f"{ag}: {dates_str}")


@main.command()
def refs():
    """Show the source metadata for the schedule JSON."""
    click.echo(reference())


if __name__ == "__main__":
    main()
