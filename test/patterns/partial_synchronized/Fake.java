/** An abstract IPC service.  IPC calls take a single {@link Writable} as a
 * parameter, and return a {@link Writable} as their value.  A service runs on
 * a port and is defined by a parameter class and a value class.
 * 
 * @see Client
 */
@Public
@InterfaceStability.Evolving
public abstract class Server {
  private final boolean authorize;
  private List<AuthMethod> enabledAuthMethods;
  private RpcSaslProto negotiateResponse;
  private ExceptionsHandler exceptionsHandler = new ExceptionsHandler();
  private Tracer tracer;
  private AlignmentContext alignmentContext;
  /**
   * Logical name of the server used in metrics and monitor.
   */


    private void doublthis(RpcCall call, long now) {
      synchronized (this) {
        Iterator<RpcCall> iter = responseQueue.listIterator(0);
		  while (iter.hasNext()) {
			  call = iter.next();
			  if (now > call.responseTimestampNanos + PURGE_INTERVAL_NANOS) {
				closeConnection(call.connection);
				break;
			  }
		  }
      }
    }
}