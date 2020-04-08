# Qpid JMS tracing examples

## Setting up your environment for tracing

Configuration of tracing is typically done using environment
variables.  See the [Jaeger client
docs](https://github.com/jaegertracing/jaeger-client-java/blob/master/jaeger-core/README.md#configuration-via-environment)
for more information.

For example, this is how you would set up your environment to force
tracing:

```sh
export JAEGER_SAMPLER_TYPE=const
export JAEGER_SAMPLER_PARAM=1
```
