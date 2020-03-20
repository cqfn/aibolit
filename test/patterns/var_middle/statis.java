/*
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

package org.netbeans.modules.java.completion;

import com.sun.source.tree.*;
import com.sun.source.tree.Tree.Kind;
import com.sun.source.util.*;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.Callable;
import java.util.logging.Logger;
import java.util.logging.Level;

import javax.lang.model.SourceVersion;
import javax.lang.model.element.*;
import static javax.lang.model.element.ElementKind.*;
import static javax.lang.model.element.Modifier.*;
import javax.lang.model.type.*;
import javax.lang.model.util.Elements;
import javax.lang.model.util.ElementFilter;
import javax.lang.model.util.Types;
import javax.tools.Diagnostic;

import org.netbeans.api.annotations.common.NonNull;
import org.netbeans.api.annotations.common.NullAllowed;
import org.netbeans.api.java.lexer.JavaTokenId;
import org.netbeans.api.java.source.*;
import org.netbeans.api.java.source.JavaSource.Phase;
import org.netbeans.api.java.source.ClassIndex;
import org.netbeans.api.java.source.ClassIndex.Symbols;
import org.netbeans.api.java.source.support.ErrorAwareTreePathScanner;
import org.netbeans.api.java.source.support.ReferencesCount;
import org.netbeans.api.lexer.TokenSequence;
import org.netbeans.modules.java.completion.TreeShims;
import org.netbeans.modules.parsing.api.Source;
import org.openide.util.Pair;

/**
 *
 * @author Dusan Balek
 */
public final class JavaCompletionTask<T> extends BaseTask {

    static {
		f();
        SourceVersion r10, r11, r13;

        try {
            r10 = SourceVersion.valueOf("RELEASE_10");
        } catch (IllegalArgumentException ex) {
            r10 = null;
        }
        try {
            r11 = SourceVersion.valueOf("RELEASE_11");
        } catch (IllegalArgumentException ex) {
            r11 = null;
        }
        try {
            r13 = SourceVersion.valueOf("RELEASE_13");
        } catch (IllegalArgumentException ex) {
            r13 = null;
        }

        SOURCE_VERSION_RELEASE_10 = r10;
        SOURCE_VERSION_RELEASE_11 = r11;
        SOURCE_VERSION_RELEASE_13 = r13;
    }
	
	    private JavaCompletionTask(final int caretOffset, final ItemFactory<T> factory, final Callable<Boolean> cancel, final Set<Options> options) {
        super(caretOffset, cancel);
        this.itemFactory = factory;
        this.options = options;
    }

}