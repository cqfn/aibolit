// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed.

// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.pulsar.io.kafka.connect;

import static com.google.common.base.Preconditions.checkArgument;
import static java.nio.charset.StandardCharsets.UTF_8;
import static org.apache.commons.lang.StringUtils.isBlank;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.ByteBufUtil;
import io.netty.buffer.Unpooled;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Future;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.connect.runtime.WorkerConfig;
import org.apache.kafka.connect.storage.OffsetBackingStore;
import org.apache.kafka.connect.util.Callback;
import org.apache.pulsar.client.api.Message;
import org.apache.pulsar.client.api.MessageId;
import org.apache.pulsar.client.api.Producer;
import org.apache.pulsar.client.api.PulsarClient;
import org.apache.pulsar.client.api.PulsarClientException;
import org.apache.pulsar.client.api.Reader;
import org.apache.pulsar.client.api.Schema;

/**
 * Implementation of {@link OffsetBackingStore} that uses a Pulsar topic to store offset data.
 */
@Slf4j
public class PulsarOffsetBackingStore implements OffsetBackingStore {

    private Map<ByteBuffer, ByteBuffer> data;
    private PulsarClient client;
    private String serviceUrl;
    private String topic;
    private Producer<byte[]> producer;
    private Reader<byte[]> reader;
    private volatile CompletableFuture<Void> outstandingReadToEnd = null;

    @Override
    public void configure(WorkerConfig workerConfig) {
        this.topic = workerConfig.getString(PulsarKafkaWorkerConfig.OFFSET_STORAGE_TOPIC_CONFIG);
        checkArgument(!isBlank(topic), "Offset storage topic must be specified");
        this.serviceUrl = workerConfig.getString(PulsarKafkaWorkerConfig.PULSAR_SERVICE_URL_CONFIG);
        checkArgument(!isBlank(serviceUrl), "Pulsar service url must be specified at `"
            + WorkerConfig.BOOTSTRAP_SERVERS_CONFIG + "`");
        this.data = new HashMap<>();

        log.info("Configure offset backing store on pulsar topic {} at cluster {}",
            topic, serviceUrl);
    }

    void readToEnd(CompletableFuture<Void> future) {
        synchronized (this) {
            if (outstandingReadToEnd != null) {
                outstandingReadToEnd.whenComplete((result, cause) -> {
                    if (null != cause) {
                        future.completeExceptionally(cause);
                    } else {
                        future.complete(result);
                    }
                });
                // return if the outstanding read has been issued
                return;
            } else {
                outstandingReadToEnd = future;
                future.whenComplete((result, cause) -> {
                    synchronized (PulsarOffsetBackingStore.this) {
                        outstandingReadToEnd = null;
                    }
                });
            }
        }
        producer.flushAsync().whenComplete((ignored, cause) -> {
            if (null != cause) {
                future.completeExceptionally(cause);
            } else {
                checkAndReadNext(future);
            }
        });
    }

    private void checkAndReadNext(CompletableFuture<Void> endFuture) {
        reader.hasMessageAvailableAsync().whenComplete((hasMessageAvailable, cause) -> {
            if (null != cause) {
                endFuture.completeExceptionally(cause);
            } else {
                if (hasMessageAvailable) {
                    readNext(endFuture);
                } else {
                    endFuture.complete(null);
                }
            }
        });
    }

    private void readNext(CompletableFuture<Void> endFuture) {
        reader.readNextAsync().whenComplete((message, cause) -> {
            if (null != cause) {
                endFuture.completeExceptionally(cause);
            } else {
                processMessage(message);
                checkAndReadNext(endFuture);
            }
        });
    }

    void processMessage(Message<byte[]> message) {
        synchronized (data) {
            data.put(
                ByteBuffer.wrap(message.getKey().getBytes(UTF_8)),
                ByteBuffer.wrap(message.getValue()));
        }
    }

    @Override
    public void start() {
        try {
            client = PulsarClient.builder()
                .serviceUrl(serviceUrl)
                .build();
            log.info("Successfully created pulsar client to {}", serviceUrl);
            producer = client.newProducer(Schema.BYTES)
                .topic(topic)
                .create();
            log.info("Successfully created producer to produce updates to topic {}", topic);
            reader = client.newReader(Schema.BYTES)
                .topic(topic)
                .startMessageId(MessageId.earliest)
                .create();
            log.info("Successfully created reader to replay updates from topic {}", topic);
            CompletableFuture<Void> endFuture = new CompletableFuture<>();
            readToEnd(endFuture);
            endFuture.join();
        } catch (PulsarClientException e) {
            log.error("Failed to create pulsar client to cluster at {}", serviceUrl, e);
            throw new RuntimeException("Failed to create pulsar client to cluster at " + serviceUrl, e);
        }
    }

    @Override
    public void stop() {
        if (null != producer) {
            try {
                producer.close();
            } catch (PulsarClientException e) {
                log.warn("Failed to close producer", e);
            }
        }
        if (null != reader) {
            try {
                reader.close();
            } catch (IOException e) {
                log.warn("Failed to close reader", e);
            }
        }
        if (null != client) {
            try {
                client.close();
            } catch (IOException e) {
                log.warn("Failed to close client", e);
            }
        }
    }

    @Override
    public Future<Map<ByteBuffer, ByteBuffer>> get(Collection<ByteBuffer> keys,
                                                   Callback<Map<ByteBuffer, ByteBuffer>> callback) {
        CompletableFuture<Void> endFuture = new CompletableFuture<>();
        readToEnd(endFuture);
        return endFuture.thenApply(ignored -> {
            Map<ByteBuffer, ByteBuffer> values = new HashMap<>();
            for (ByteBuffer key : keys) {
                ByteBuffer value;
                synchronized (data) {
                    value = data.get(key);
                }
                if (null != value) {
                    values.put(key, value);
                }
            }
            if (null != callback) {
                callback.onCompletion(null, values);
            }
            return values;
        }).whenComplete((ignored, cause) -> {
            if (null != cause && null != callback) {
                callback.onCompletion(cause, null);
            }
        });
    }

    @Override
    public Future<Void> set(Map<ByteBuffer, ByteBuffer> values, Callback<Void> callback) {
        values.forEach((key, value) -> {
            ByteBuf bb = Unpooled.wrappedBuffer(key);
            byte[] keyBytes = ByteBufUtil.getBytes(bb);
            bb = Unpooled.wrappedBuffer(value);
            byte[] valBytes = ByteBufUtil.getBytes(bb);
            producer.newMessage()
                .key(new String(keyBytes, UTF_8))
                .value(valBytes)
                .sendAsync();
        });
        return producer.flushAsync().whenComplete((ignored, cause) -> {
            if (null != callback) {
                callback.onCompletion(cause, ignored);
            }
            if (null == cause) {
                readToEnd(new CompletableFuture<>());
            }
        });
    }
}
