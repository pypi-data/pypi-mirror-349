# pytest-dashboard

## example
- Download project
- Run some pytest with `--progress-path` option. The value should end with `-progress.yaml`.
    - i.e.) `pytest <path_to_project>\sample-tests --progress-path=<path_to_project>\sample-tests\sample-progress.yaml`
    - You will get a `sample-progress.yaml` file.
- Run pytest dashboard
    - i.e.) `tally-pytest <path_to_project>\sample-tests`
    - You will get a `entire-progress.yaml` file in working folder.

## usage
`pytest`

By this command, you get `[datetime]-progress.yaml` file on working directory as realtime pytest progress report.

---

`pytest --progress-path=[path/to/some-progress.yaml]`

By this command, you get `path/to/some-progress.yaml` file.
The value should end with `-progress.yaml`.

---

`tally-pytest PROGRESSES_DIR --entire_progress_path=[path/to/entire-progress.yaml]`

By this command, you get started to monitor changes of
the progress files (ends with `-progress.yaml`)
inside `PROGRESS_DIR` and save the state summary
to `path/to/entire-progress.yaml`.

So it is necessary to set `--progress-path` option of pytest
ending with `-progress.yaml`.
For example, `2024-04-22-progress.yaml`,

> [!NOTE]
> if your `entire_progress_path` is ends with `-progress.yaml`,
> you cannot save the entire progress file to
> the same directory with each progress file.

---

`tally-pytest PROGRESS_DIR --notification=True`

By this command, you will get mail notification when entire progress is finished.
> [!NOTE]
> Please implement pytest_dashboard.config
> that contains information abaout mail address and SMTP server.
> This command works with powershell `Send-MailMessage` command.

---

`tally-pytest PROGRESS_DIR --dashboart=True`

Not implemented!
