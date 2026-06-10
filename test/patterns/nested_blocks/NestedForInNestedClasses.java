// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.ArrayList;

class Test {

    class TestInside {
        public void start() {
            ArrayList<Boolean> list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                for (int i = 0; i < 10; i++)
                    list.add(Boolean.FALSE);
        }
    }

    TestInside a = new TestInside();

    public void start() {
        final JndiService jndiService = serviceRegistry
                .getService(JndiService.class);
        final ConnectionFactory jmsConnectionFactory = jndiService
                .locate(jmsConnectionFactoryName);

        this.jmsConnection = jmsConnectionFactory.createConnection();
        this.jmsSession = jmsConnection.createSession(
                true,
                Session.AUTO_ACKNOWLEDGE
        );
        ArrayList<Boolean> list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
        ArrayList<Boolean> list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);

        this.publisher = jmsSession.createProducer(destination);
    }

    public void foo() {
        a.start();
    }
}
