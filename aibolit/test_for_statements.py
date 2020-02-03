# -*- encoding: utf-8 -*-
import unittest
import javalang


def foo(tree):
    return 1


class TestForStatement(unittest.TestCase):
    """
    Test function which returns number of for statements
    """

    def test_single_loop(self):
        class_txt = """
      class Test {
      @Override
      public void start() {
          final JndiService jndiService = serviceRegistry
              .getService( JndiService.class );
          final ConnectionFactory jmsConnectionFactory = jndiService
              .locate( jmsConnectionFactoryName );

          this.jmsConnection = jmsConnectionFactory.createConnection();
          this.jmsSession = jmsConnection.createSession(
              true,
              Session.AUTO_ACKNOWLEDGE
          );
  		list = new ArrayList<>();
          for (int i=0; i<10; i++)
              list.add(Boolean.FALSE);
          final Destination destination = jndiService.locate( destinationName );

          this.publisher = jmsSession.createProducer( destination );
          }
      }
      """
        tree = javalang.parse.parse(class_txt)
        assert foo(tree) == 1

    def test_nested_loops(self):
        class_txt = """
          class Test {
          @Override
          public void start() {
              final JndiService jndiService = serviceRegistry
                  .getService( JndiService.class );
              final ConnectionFactory jmsConnectionFactory = jndiService
                  .locate( jmsConnectionFactoryName );

              this.jmsConnection = jmsConnectionFactory.createConnection();
              this.jmsSession = jmsConnection.createSession(
                  true,
                  Session.AUTO_ACKNOWLEDGE
              );
      		list = new ArrayList<>();
              for (int i=0; i<10; i++)
                  list.add(Boolean.FALSE);
      		list = new ArrayList<>();
              for (int i=0; i<10; i++)
                  list.add(Boolean.FALSE);

      		list = new ArrayList<>();
              for (int i=0; i<10; i++)
      			for (int i=0; i<10; i++)
      				list.add(Boolean.FALSE);
              final Destination destination = jndiService.locate( destinationName );

              this.publisher = jmsSession.createProducer( destination );
              }
          }
          """
        tree = javalang.parse.parse(class_txt)
        assert foo(tree) == 2

    def test_loops_in_different_methods(self):
        class_txt = """
          class Test {
          @Override
          public void start() {
              final JndiService jndiService = serviceRegistry
                  .getService( JndiService.class );
              final ConnectionFactory jmsConnectionFactory = jndiService
                  .locate( jmsConnectionFactoryName );

              this.jmsConnection = jmsConnectionFactory.createConnection();
              this.jmsSession = jmsConnection.createSession(
                  true,
                  Session.AUTO_ACKNOWLEDGE
              );
      		list = new ArrayList<>();
              for (int i=0; i<10; i++)
                  list.add(Boolean.FALSE);
      		list = new ArrayList<>();
              for (int i=0; i<10; i++)
                  list.add(Boolean.FALSE);

      		list = new ArrayList<>();
              for (int i=0; i<10; i++)
      			for (int i=0; i<10; i++)
      				list.add(Boolean.FALSE);
              final Destination destination = jndiService.locate( destinationName );

              this.publisher = jmsSession.createProducer( destination );
              }
          }

          public void doNothing() {
              for (int i=0; i<10; i++)
      			for (int i=0; i<10; i++)
      			    for (int i=0; i<10; i++)
      				    list.add(Boolean.FALSE);
          }
      """
        tree = javalang.parse.parse(class_txt)
        assert foo(tree) == 3


if __name__ == '__main__':
    unittest.main()
