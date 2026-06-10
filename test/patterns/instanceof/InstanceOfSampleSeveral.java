// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Test
{
    public static void main(String[] args)
    {
        Child cobj = new Child();
        // A simple case
        if (cobj instanceof String)
           System.out.println("cobj is instance of Child");

        final JndiService jndiService = serviceRegistry
                .getService(JndiService.class);
        final ConnectionFactory jmsConnectionFactory = jndiService
                .locate(jmsConnectionFactoryName);

        this.jmsConnection = jmsConnectionFactory.createConnection();
        this.jmsSession = jmsConnection.createSession(
                true,
                Session.AUTO_ACKNOWLEDGE
        );
        if (cobj instanceof String)
           System.out.println("cobj is instance of Child");

        this.jmsConnection = jmsConnectionFactory.createConnection();
        this.jmsSession = jmsConnection.createSession(
                true,
                Session.AUTO_ACKNOWLEDGE
        );

        if (cobj instanceof String)
           System.out.println("cobj is instance of Child");
    }
}
