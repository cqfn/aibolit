/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.dashboard;

import com.artipie.http.Response;
import com.artipie.http.Slice;
import com.artipie.http.rs.RsStatus;
import com.artipie.http.rs.RsWithBody;
import com.artipie.http.rs.RsWithStatus;
import io.reactivex.Emitter;
import io.reactivex.Flowable;
import io.reactivex.functions.Consumer;
import io.reactivex.schedulers.Schedulers;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.reactivestreams.Publisher;
import org.reactivestreams.Subscriber;

/**
 * Classpath resource content.
 * @since 0.6
 */
public final class ResourceSlice implements Slice {

    /**
     * Classloader.
     */
    private final ClassLoader clo;

    /**
     * Resource name.
     */
    private final String name;

    /**
     * New resource from current thread context classloader.
     * @param name Resource name
     */
    public ResourceSlice(final String name) {
        this(Thread.currentThread().getContextClassLoader(), name);
    }

    /**
     * New resource from provided classloader.
     * @param clo Classloader
     * @param name Resource name
     */
    public ResourceSlice(final ClassLoader clo, final String name) {
        this.clo = clo;
        this.name = name;
    }

    @Override
    public Response response(final String lien, final Iterable<Map.Entry<String, String>> headers,
        final Publisher<ByteBuffer> body) {
        final InputStream stream = this.clo.getResourceAsStream(this.name);
        final Response rsp;
        if (stream == null) {
            rsp = new RsWithStatus(
                new RsWithBody(
                    String.format("Resource '%s' not found", this.name), StandardCharsets.UTF_8
                ),
                RsStatus.NOT_FOUND
            );
        } else {
            rsp = new RsWithStatus(
                new RsWithBody(new StreamPublisher(stream)),
                RsStatus.OK
            );
        }
        return rsp;
    }

    /**
     * Input stream as a publisher.
     * @since 0.6
     */
    private static final class StreamPublisher extends Flowable<ByteBuffer> {

        /**
         * Buffer size for resources.
         */
        private static final int BUF_SIZE = 1024 * 8;

        /**
         * Input stream.
         */
        private final InputStream stream;

        /**
         * New publisher from stream.
         * @param stream Input stream
         */
        StreamPublisher(final InputStream stream) {
            this.stream = stream;
        }

        @Override
        public void subscribeActual(final Subscriber<? super ByteBuffer> sub) {
            Flowable.generate(
                (Consumer<Emitter<ByteBuffer>>) emitter -> {
                    final byte[] buf = new byte[StreamPublisher.BUF_SIZE];
                    final int read;
                    try {
                        read = this.stream.read(buf);
                    } catch (final IOException err) {
                        emitter.onError(err);
                        return;
                    }
                    if (read < 0) {
                        emitter.onComplete();
                    } else {
                        emitter.onNext(ByteBuffer.wrap(buf));
                    }
                }
            ).observeOn(Schedulers.io()).doOnTerminate(this.stream::close).subscribe(sub);
        }
    }
}
