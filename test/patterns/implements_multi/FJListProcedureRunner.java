/*
 * SPDX-FileCopyrightText: Copyright (c) 2016 Goldman Sachs.
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */

package org.eclipse.collections.impl.forkjoin;

import java.io.Serializable;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.ForkJoinTask;

import org.eclipse.collections.api.block.function.Function;
import org.eclipse.collections.api.block.procedure.Procedure;
import org.eclipse.collections.impl.list.mutable.FastList;
import org.eclipse.collections.impl.parallel.Combiner;
import org.eclipse.collections.impl.parallel.ProcedureFactory;

public class FJListProcedureRunner<T, PT extends Procedure<? super T>> implements Serializable
{
    private static final long serialVersionUID = 1L;

    private Throwable error;
    private final Combiner<PT> combiner;
    private final int taskCount;
    private final BlockingQueue<PT> outputQueue;

    public FJListProcedureRunner(Combiner<PT> newCombiner, int taskCount)
    {
        this.combiner = newCombiner;
        this.taskCount = taskCount;
        this.outputQueue = this.combiner.useCombineOne() ? new ArrayBlockingQueue<>(taskCount) : null;
    }

    private FastList<ForkJoinTask<PT>> createAndExecuteTasks(ForkJoinPool executor, ProcedureFactory<PT> procedureFactory, List<T> list)
    {
        FastList<ForkJoinTask<PT>> tasks = FastList.newList(this.taskCount);
        int sectionSize = list.size() / this.taskCount;
        int taskCountMinusOne = this.taskCount - 1;
        for (int index = 0; index < this.taskCount; index++)
        {
            ForkJoinTask<PT> task = this.createTask(procedureFactory, list, sectionSize, taskCountMinusOne, index);
            tasks.add(task);
            executor.execute(task);
        }
        return tasks;
    }

    protected FJListProcedureTask<T, PT> createTask(ProcedureFactory<PT> procedureFactory, List<T> list, int sectionSize, int taskCountMinusOne, int index)
    {
        return new FJListProcedureTask<>(this, procedureFactory, list, index, sectionSize, index == taskCountMinusOne);
    }

    public void setFailed(Throwable newError)
    {
        this.error = newError;
    }

    public void taskCompleted(ForkJoinTask<PT> task)
    {
        if (this.combiner.useCombineOne())
        {
            this.outputQueue.add(task.getRawResult());
        }
    }

    public void executeAndCombine(ForkJoinPool executor, ProcedureFactory<PT> procedureFactory, List<T> list)
    {
        FastList<ForkJoinTask<PT>> tasks = this.createAndExecuteTasks(executor, procedureFactory, list);
        if (this.combiner.useCombineOne())
        {
            this.join();
        }
        if (this.error != null)
        {
            throw new RuntimeException("One or more parallel tasks failed", this.error);
        }
        if (!this.combiner.useCombineOne())
        {
            this.combiner.combineAll(tasks.asLazy().collect(new ProcedureExtractor()));
        }
    }

    private void join()
    {
        try
        {
            int remainingTaskCount = this.taskCount;
            while (remainingTaskCount > 0)
            {
                this.combiner.combineOne(this.outputQueue.take());
                remainingTaskCount--;
            }
        }
        catch (InterruptedException e)
        {
            throw new RuntimeException("Combine failed", e);
        }
    }

    private final class ProcedureExtractor implements Function<ForkJoinTask<PT>, PT>
    {
        private static final long serialVersionUID = 1L;

        @Override
        public PT valueOf(ForkJoinTask<PT> object)
        {
            try
            {
                return object.get();
            }
            catch (InterruptedException | ExecutionException e)
            {
                throw new RuntimeException(e);
            }
        }
    }
}
