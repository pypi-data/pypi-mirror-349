from importlib import metadata as im

name = "pyeio"
version = im.version(name)
metadata = im.metadata(name).json
urls = dict(map(lambda s: s.split(", "), metadata["project_url"]))
homepage = urls["homepage"]
documentation = urls["homepage"]
repository = urls["homepage"]
