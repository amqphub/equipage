# Kerberos with the properties login module

## General

 - No changes to artemis-users.properties

## login.config ##

    activemq {
       org.apache.activemq.artemis.spi.core.security.jaas.Krb5LoginModule optional
           debug=true;

       org.apache.activemq.artemis.spi.core.security.jaas.PropertiesLoginModule sufficient
           debug=true
           reload=true
           org.apache.activemq.jaas.properties.user="artemis-users.properties"
           org.apache.activemq.jaas.properties.role="artemis-roles.properties";
    };

    amqp-sasl-gssapi {
        com.sun.security.auth.module.Krb5LoginModule required
        isInitiator=false
        storeKey=true
        useKeyTab=true
        keyTab="/home/jross/test.keytab"
        principal="amqp/upto.nogood.industries@NOGOOD.INDUSTRIES"
        debug=true;
    };

## artemis-roles.properties ##

    admin = admin,jgecko@NOGOOD.INDUSTRIES

## logging.properties ##

Not necessary, but it helps to see what's going on.

    loggers=org.eclipse.jetty,org.jboss.logging,org.apache.activemq.artemis.core.server,org.apache.activemq.artemis.utils,org.apache.activemq.artemis.journal,org.apache.activemq.artemis.jms.server,org.apache.activemq.artemis.integration.bootstrap,org.apache.activemq.artemis.spi.core.security

    [...]

    logger.org.apache.activemq.artemis.spi.core.security.level=DEBUG
