// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Test {
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
					list = new ArrayList<>();

	if (true) {

		for (int i = 0; i < 10; i++)
			for (int k = 0; k < 10; k++)
				list.add(Boolean.FALSE);
		list = new ArrayList<>();
		this.jmsConnection = jmsConnectionFactory.createConnection(jmsConnectionFactory,jmsConnectionFactory, jmsConnectionFactory, jmsConnectionFactory)

		for (int i = 0; i < 10; i++)
			list.add(Boolean.FALSE);

	}

	list = new ArrayList<>();
	for (int i = 0; i < 10; i++)
		for (int i = 0; i < 10; i++)
			list.add(Boolean.FALSE);
					final Destination destination = jndiService.locate(destinationName);
		int a = 0;
					this.publisher = jmsSession.createProducer(destination);
	this.jmsConnection = jmsConnectionFactory.createConnection(jmsConnectionFactory,jmsConnectionFactory, jmsConnectionFactory, jmsConnectionFactory, jmsConnectionFactory)

    }
}
