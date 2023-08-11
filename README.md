# no-webp
### A daemon that convert .webp files to another image type on selected directories for systemd systems

Tired to download .webp files that are not usefull until you convert them? no-webp does it for you without removing the original file, capable to monitor multiple directories and with other configurable options!

## Installation
To install and run the daemon, run this command:
```bash
sudo bash install.sh
```
Note: I suggest you to install the <a href="https://imagemagick.org/index.php">imagemagick</a> package to be able to use `convert` or another similar package.

## Configuration
Configuration options are modifiable in the `/opt/no-webp/config.yml` file.
<br />
Here are the possible options:

### conversion

##### conversion.extension (Mandatory)

This is the type of the file that you want the .webp image to be converted to, it should be compatible with `context.converter_package`
<br />
Example:
```yaml
conversion:
  extension: .jpg
```
##### conversion.prefix

Prefix for the output file
<br />
Example:
```yaml
conversion:
  prefix: convert-
```
##### conversion.suffix

Suffix for the output file
<br />
Example:
```yaml
conversion:
  suffix: .converted
```

### context

##### context.directories (Mendatory)

Directories to monitor, every .webp file created in those directories will be converted.
<br />
Example:
```yaml
context:
  directories:
  - /home/username/Downloads
  - /home/username/Pictures
```


##### context.converter_package (Mendatory)

Which package to use to convert the files, should be like this: `package <file to convert> <output file>`. I suggest `convert` for this package
<br />
Example:
```yaml
context:
  converter_package: /usr/bin/convert
```

### Exemples

There are examples in the [example_config](example_config) folder
