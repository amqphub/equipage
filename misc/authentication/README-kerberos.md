# Skylla

Test code for AMQP clients using Kerberos

## Running the tests

1. Configure your Kerberos realm.  Ensure the default ticket cache
   naming scheme is in use.

2. Log in.

        $ kinit <user>@<realm>

3. Check your status.

        $ klist

3. Run the test code.

        $ cd cpp
        $ make test

        $ cd java
        $ make test

The make test targets run against a test service I have setup,
upto.nogood.industries.  Edit the Makefiles to hit a different
service.

## Files you may need to draw from

    misc/krb5.config                       # Kerberos settings
    misc/login.config                      # Broker config
    java/src/main/resources/login.config   # Java client config
