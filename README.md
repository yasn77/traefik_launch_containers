# Launch containers with Traefik

This is a simple POC that I wanted to try out. The basic idea is to auto
launch containers when request comes in.

## Why do it?

Mainly to 'scratch an itch', but also because I am looking to replace a system we are currently using to auto launch containers with minimal overhead.

## Getting started

Couple of things need to be done before running:
  1. Docker compose is needed
  1. Add `tstapp1.foo.com`, `tstapp2.foo.com`, `app-status.foo.com` to you hosts file (pointing to `127.0.0.1`)
  2. Create a docker network : `docker network create traefik_tst`
  3. Docker pull `training/webapp`... The launching of containers is not async...
    This of course is not ideal (and can easily be implemented using Celery) but
    for the purpose of the POC it's good enough


To launch simply use `docker-compose`:

```bash
docker-compose up -d --force-recreate --build
```

Once it's up and running, simply browse to either or both http://tstapp1.foo.com
and http://tstapp2.foo.com

You should see a holding page and then shortly the page should reload with
the sample 'Hello World' app.

You can view Traefik page by browsing to [http://127.0.0.1:8181](http://127.0.0.1:8181)

## How does it work?

It's pretty simple... Docker compose launches two containers:

1. Traefik Server
2. A simple Flask App for launching containers

The Flask app is configured to listen for all hosts coming in but is set with a low priority. This means that if a new container comes up with host rules of a higher priority, then that container is what is returned.

When no higher priority host rule exists, the Flask app will launch a container and using the URL it will construct Docker labels that will be read by Traefik. The labels will container routing rules and set high priority on them.

The Flask app simply returns a reload to the user... so after 3 seconds the site is reloaded and if the container comes up, Traefik will reroute the user.

## How can this be improved?

It seems to work pretty well, but as previously mentioned, launching the container should be done asynchronously. Also I could add some more intelligence around things like health checks (i.e only redirect if app is healthy).

I am sure there are lots more that could be done.... Happy to hear about suggestions

