# stechuhr

stechuhr is a python application and library to append to and analyze files in the
[timeclock.el](https://doc.endlessparentheses.com/Fun/timeclock-log-data.html)
format.

## Installation

Use [pipx](https://pipx.pypa.io/stable/) to install stechuhr.

```bash
pipx install stechuhr
```

## Usage

stechuhr has a sensible commandline interface (CLI).

### Clock in

To append a clock in for the account "acc:sub" line invoke the following command.

```bash
stechuhr clock in acc sub
```

### Help

To find out more about the general usage invoke

```bash
stechuhr --help
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Tests are, in any case, essential.

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
