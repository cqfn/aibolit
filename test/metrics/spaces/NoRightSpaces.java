// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Test                                                                   {
                                                         public void start() {
final JndiService jndiService = serviceRegistry.getService(JndiService.class);
final ConnectionFactory jmsConnectionFactory = jndiService.locate(aaaaaaaaaa);

                 this.jmsConnection = jmsConnectionFactory.createConnection();
this.jmsSession = jmsConnection.createSession(true, Session.AUTO_ACKNOWLEDGE);
          final Destination destination = jndiService.locate(destinationName);

                      this.publisher = jmsSession.createProducer(destination);
                                                                             }
                                                                             }
