import javax.validation.constraints.NotNull;

/**
 * Routine.
 *
 * @author Yegor Bugayenko (yegor256@gmail.com)
 * @version $Id$
 * @since 1.50
 * @todo #1125:30min Routine should be delegate execution to separate threads.
 *  Currently com.rultor.Routine#process() is sequentially processing all Talks
 *  and breaking out of this sequential processing to log occurring exceptions.
 *  This leads to issues in one build breaking all builds globally.
 *  This should be reworked to run the chain of Agents for each talk in a
 *  separate thread, not interfering with the main Routine in error cases.
 *  Once this is done the swallowing of generic exceptions, added to
 *  circumvent this issue, in
 *  com.rultor.agents.github.Reports#process(com.jcabi.xml.XML) should be
 *  removed.
 */
@ScheduleWithFixedDelay(delay = 1, unit = TimeUnit.MINUTES, threads = 1)
@SuppressWarnings("PMD.DoNotUseThreads")
final class Routine implements Runnable, Closeable {

    /**
     * Shutting down?
     */
    private final transient AtomicBoolean down = new AtomicBoolean();

    /**
     * When I started.
     */
    private final transient long start = System.currentTimeMillis();

    /**
     * Ticks.
     */
    private final transient Pulse pulse;

    /**
     * Talks.
     */
    private final transient Talks talks;

    /**
     * Agents.
     */
    private final transient Agents agents;

    /**
     * Ctor.
     * @param tlks Talks
     * @param pls Pulse
     * @param github Github client
     * @param sttc Sttc client
     * @checkstyle ParameterNumberCheck (4 lines)
     */
    Routine(@NotNull final Talks tlks, final Pulse pls,
        final Github github, final Sttc sttc) {
        this.talks = tlks;
        this.pulse = pls;
        this.agents = new Agents(github, sttc);
    }

    @Override
    public void close() {
        this.down.set(true);
    }

    @Override
    @SuppressWarnings("PMD.AvoidCatchingThrowable")
    public void run() {
        try {
            Logger.info(
                this, "%d active talks, alive for %[ms]s: %tc",
                this.safe(),
                System.currentTimeMillis() - this.start, new Date()
            );
            this.pulse.error(Collections.<Throwable>emptyList());
            // @checkstyle IllegalCatchCheck (1 line)
        } catch (final Throwable ex) {
            if (!this.down.get()) {
                Logger.error(this, "#run(): %[exception]s", ex);
                try {
                    TimeUnit.MICROSECONDS.sleep(1L);
                } catch (final InterruptedException iex) {
                    Logger.info(this, "%[exception]s", iex);
                }
            }
            Sentry.capture(ex);
            this.pulse.error(Collections.singleton(ex));
        }
    }

    /**
     * Routine every-minute proc.
     * @return Total talks processed
     * @throws IOException If fails
     */
    @Timeable(limit = Tv.TWENTY, unit = TimeUnit.MINUTES)
    private int safe() throws IOException {
        final long begin = System.currentTimeMillis();
        int total = 0;
        if (new Toggles.InFile().readOnly()) {
            Logger.info(this, "read-only mode");
        } else {
            total = this.process();
        }
        this.pulse.add(
            new Tick(begin, System.currentTimeMillis() - begin, total)
        );
        return total;
    }

    /**
     * Routine every-minute proc.
     * @return Total talks processed
     * @throws IOException If fails
     */
    private int process() throws IOException {
        this.agents.starter().execute(this.talks);
        final Profiles profiles = new Profiles();
        int total = 0;
        for (final Talk talk : this.talks.active()) {
            ++total;
            final Profile profile = profiles.fetch(talk);
            this.agents.agent(talk, profile).execute(talk);
        }
        this.agents.closer().execute(this.talks);
        return total;
    }

}