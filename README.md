# gsrest

GeoServer python REST API client.

## About

This package is on an early stage, but may be functional for your needs.

At this point, the only documentation is the one on source files and the tests
themself.

## Features

  * HTTP only. *Warning*: your geoserver credentials may be publicly exposed.
  * Python >= 3.7.
  * Static setup of the connection for all GeoServer elements.
  * Easily extendable.
  * Support to load elements from a YAML file.
  * Just PyYAML as runtime dependency.

## Installation

```
pip install gsrest
```

## Sample usage

To test the client, you need a geoserver instance. For simplicity, in this
example we will use the [geoserver docker image from
kartoza](https://hub.docker.com/r/kartoza/geoserver/):

```
$ docker run -d --rm -p 8080:8080 --name geoserver kartoza/geoserver:2.17.0
```

Let's setup the client credentials. Default values work fine with the docker
instance.

```
$ python
>>> from gsrest import client
>>> client.GsClient()  # will setup the connection for all elements
```

Next, let's create a local workspace and sync (upload) it to the server.

```
>>> from gsrest.elements import workspace
>>> wsp = workspace.WorkSpace("wsp1")
>>> wsp.uri = "http://my.uri/"
>>> wsp.sync()
```

Then, you can check the new workspace at http://localhost:8080/geoserver
(user `admin` / password `geoserver`).

Finally, do not forget to kill the docker instance.

```
$ docker kill geoserver
```

## License

Licensed under the term of `GPL-3.0-or-later LICENSE`. See [LICENSE](LICENSE).
