The configuration is a JSON structure. We'll use the following for the
coming examples.

```JSON
{
  "courses": {
    "datintro22": {
      "timesheet": {
        "url": "https://sheets.google..."
      },
      "schedule": {
        "url": "https://timeedit.net/..."
      }
    }
  }
}
```

The format is actually irrelevant to anyone outside of this library,
since it will never be accessed directly anyway. But it will be used to
illustrate the examples.

We can access values by dot-separated addresses. For instance, we can
use `courses.datintro22.schedule.url` to access the TimeEdit URL of the
datintro22 course.

Let's have a look at some usage examples.

### A command-line application

Say we have the program `nytid` that wants to use this config module and
subcommand. We want the CLI command to have the following form when used
with `nytid`.

```bash
  nytid config courses.datintro22.schedule.url --set https://timeedit.net/...
```

will set the configuration value at the path, whereas

```bash
  nytid config courses.datintro22.schedule.url
```

will return it.

We can do this with both `typer` (and `click`) and `argparse`. With
`typer`:

```python
import typer
import typerconf as config

cli = typer.Typer()
config.add_config_cmd(cli)
```

With `argparse`:

```python
import argparse
import typerconf as config
import sys

cli = argparse.ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")
config.add_config_cmd(subparsers)

args = cli.parse_args()
if args.subcommand == "config":
  args.func(args)
```

Internally, `nytid`'s different parts can access the config through the
following API.

```python
import typerconf as config

url = config.get("courses.datintro22.schedule.url")
```

### Without the CLI

We can also use it without the CLI and application features. Then it's
the `typerconf.Config` class that is of interest.

Let's assume that we have the structure from above in the file 
`~/.config/app.config`. Consider the following code.

```python
defaults = {
  "courses": {
    "datintro22": {
      "root": "/afs/kth.se/..."
    }
  }
}

conf = Config(json_data=defaults, conf_file="~/.config/app.config")

print(f"datintro22 root directory = {conf.get('courses.datintro22.root')}")
print(f"datintro22 schedule = {conf.get('courses.datintro22.schedule')}")
```

When we construct `conf` above, we merge the default config
with the values set in the config file that was loaded.

We note that the construction of `conf` above, can be replaced
by the equivalent

```python
conf = Config(defaults)
conf.read_config("~/.config/app.config", writeback=True)
```

The meaning of `writeback` is that whenever we change the
config, it will automatically be written back to the file from which it
was read. Writeback is enabled by default when supplying the file to the
constructor. It's disabled by default for the method
`conf.read_config`, but we can turn it on by passing the
`writeback=True`.

We can change the config by using the `conf.set` method.

```python
conf.set("courses.datintro22.root", "/home/dbosk/...")
```

That would change the root that we got from the default config. Since we
enabled writeback above, this would automatically update the config file
with the new values.
