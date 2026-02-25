// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
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

package org.netbeans.editor;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.Reader;
import java.io.Writer;
import java.io.IOException;
import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.prefs.PreferenceChangeEvent;
import javax.swing.Action;
import javax.swing.InputMap;
import javax.swing.JEditorPane;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.event.AncestorEvent;
import javax.swing.text.Document;
import javax.swing.text.DefaultEditorKit;
import javax.swing.text.BadLocationException;
import javax.swing.text.Element;
import javax.swing.text.ViewFactory;
import javax.swing.text.Caret;
import javax.swing.text.JTextComponent;
import java.util.Set;
import java.util.WeakHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.prefs.PreferenceChangeListener;
import java.util.prefs.Preferences;
import javax.swing.JComponent;
import javax.swing.JScrollPane;
import javax.swing.JViewport;
import javax.swing.KeyStroke;
import javax.swing.event.AncestorListener;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.plaf.TextUI;
import javax.swing.text.AbstractDocument;
import static javax.swing.text.DefaultEditorKit.selectionBackwardAction;
import static javax.swing.text.DefaultEditorKit.selectionBeginLineAction;
import static javax.swing.text.DefaultEditorKit.selectionDownAction;
import static javax.swing.text.DefaultEditorKit.selectionEndLineAction;
import static javax.swing.text.DefaultEditorKit.selectionForwardAction;
import static javax.swing.text.DefaultEditorKit.selectionUpAction;
import javax.swing.text.EditorKit;
import javax.swing.text.Position;
import javax.swing.text.View;
import javax.swing.undo.AbstractUndoableEdit;
import javax.swing.undo.CannotRedoException;
import javax.swing.undo.CannotUndoException;
import javax.swing.undo.UndoableEdit;
import org.netbeans.api.editor.caret.CaretInfo;
import org.netbeans.api.editor.EditorActionRegistration;
import org.netbeans.api.editor.EditorActionRegistrations;
import org.netbeans.api.editor.EditorUtilities;
import org.netbeans.api.editor.caret.EditorCaret;
import org.netbeans.api.editor.mimelookup.MimeLookup;
import org.netbeans.api.editor.mimelookup.MimePath;
import org.netbeans.api.editor.settings.KeyBindingSettings;
import org.netbeans.api.editor.settings.SimpleValueNames;
import org.netbeans.lib.editor.util.CharSequenceUtilities;
import org.netbeans.lib.editor.util.ListenerList;
import org.netbeans.lib.editor.util.swing.DocumentUtilities;
import org.netbeans.modules.editor.indent.api.Indent;
import org.netbeans.modules.editor.indent.api.IndentUtils;
import org.netbeans.modules.editor.indent.api.Reformat;
import org.netbeans.modules.editor.indent.spi.CodeStylePreferences;
import org.netbeans.modules.editor.lib2.EditorPreferencesDefaults;
import org.netbeans.modules.editor.lib2.EditorPreferencesKeys;
import org.netbeans.modules.editor.lib.KitsTracker;
import org.netbeans.api.editor.NavigationHistory;
import org.netbeans.api.editor.caret.CaretMoveContext;
import org.netbeans.api.editor.caret.MoveCaretsOrigin;
import org.netbeans.spi.editor.caret.CaretMoveHandler;
import org.netbeans.lib.editor.util.swing.PositionRegion;
import org.netbeans.modules.editor.lib.SettingsConversions;
import org.netbeans.modules.editor.lib2.CaretUndo;
import org.netbeans.modules.editor.lib2.RectangularSelectionCaretAccessor;
import org.netbeans.modules.editor.lib2.RectangularSelectionUtils;
import org.netbeans.modules.editor.lib2.actions.KeyBindingsUpdater;
import org.netbeans.modules.editor.lib2.typinghooks.DeletedTextInterceptorsManager;
import org.netbeans.modules.editor.lib2.typinghooks.TypedBreakInterceptorsManager;
import org.netbeans.modules.editor.lib2.typinghooks.TypedTextInterceptorsManager;
import org.netbeans.spi.editor.typinghooks.CamelCaseInterceptor;
import org.openide.awt.StatusDisplayer;
import org.openide.util.HelpCtx;
import org.openide.util.Lookup;
import org.openide.util.LookupEvent;
import org.openide.util.LookupListener;
import org.openide.util.NbBundle;
import org.openide.util.Pair;
import org.openide.util.WeakListeners;
import org.openide.util.WeakSet;

/**
* Editor kit implementation for base document
*
* @author Miloslav Metelka
* @version 1.00
*/

public class BaseKit extends DefaultEditorKit {

    /**
     * Flag indicating that the JTextComponent.paste() is in progress.
     * Checked in BaseDocument.read() to ignore clearing of the regions
     * for trailing-whitespace-removal.
     */
    static ThreadLocal<Boolean> IN_PASTE = new ThreadLocal<Boolean>();

    // -J-Dorg.netbeans.editor.BaseKit.level=FINEST
    private static final Logger LOG = Logger.getLogger(BaseKit.class.getName());

    /** split the current line at cursor position */
    public static final String splitLineAction = "split-line"; // NOI18N

    /** Cycle through annotations on the current line */
    public static final String annotationsCyclingAction = "annotations-cycling"; // NOI18N

    /** Collapse a fold. Depends on the current caret position. */
    public static final String collapseFoldAction = "collapse-fold"; //NOI18N

    /** Expand a fold. Depends on the current caret position. */
    public static final String expandFoldAction = "expand-fold"; //NOI18N

    /** Collapse all existing folds in the document. */
    public static final String collapseAllFoldsAction = "collapse-all-folds"; //NOI18N

    /** Expand all existing folds in the document. */
    public static final String expandAllFoldsAction = "expand-all-folds"; //NOI18N

    /** Move one page up and make or extend selection */
    public static final String selectionPageUpAction = "selection-page-up"; // NOI18N

    /** Move one page down and make or extend selection */
    public static final String selectionPageDownAction = "selection-page-down"; // NOI18N

    /** Remove indentation */
    public static final String removeTabAction = "remove-tab"; // NOI18N

    /** Remove selected block or do nothing - useful for popup menu */
    public static final String removeSelectionAction = "remove-selection"; // NOI18N

    /** Expand the abbreviation */
    public static final String abbrevExpandAction = "abbrev-expand"; // NOI18N

    /** Reset the abbreviation accounting string */
    public static final String abbrevResetAction = "abbrev-reset"; // NOI18N

    /** Remove characters to the beginning of the word or
     *  the previous word if caret is not directly at word */
    public static final String removePreviousWordAction = "remove-word-previous"; // NOI18N

    /** Remove characters to the end of the word or
     *  the next word if caret is not directly at word */
    public static final String removeNextWordAction = "remove-word-next"; // NOI18N

    /** Remove to the beginning of the line */
    public static final String removeLineBeginAction = "remove-line-begin"; // NOI18N

    /** Remove line */
    public static final String removeLineAction = "remove-line"; // NOI18N

    public static final String moveSelectionElseLineUpAction = "move-selection-else-line-up"; // NOI18N

    public static final String moveSelectionElseLineDownAction = "move-selection-else-line-down"; // NOI18N

    public static final String copySelectionElseLineUpAction = "copy-selection-else-line-up"; // NOI18N

    public static final String copySelectionElseLineDownAction = "copy-selection-else-line-down"; // NOI18N

    /** Toggle the typing mode to overwrite mode or back to insert mode */
    public static final String toggleTypingModeAction = "toggle-typing-mode"; // NOI18N

    /** Change the selected text or current character to uppercase */
    public static final String toUpperCaseAction = "to-upper-case"; // NOI18N

    /** Change the selected text or current character to lowercase */
    public static final String toLowerCaseAction = "to-lower-case"; // NOI18N

    /** Switch the case of the selected text or current character */
    public static final String switchCaseAction = "switch-case"; // NOI18N

    /** Find next occurence action */
    public static final String findNextAction = "find-next"; // NOI18N

    /** Find previous occurence action */
    public static final String findPreviousAction = "find-previous"; // NOI18N

    /** Toggle highlight search action */
    public static final String toggleHighlightSearchAction = "toggle-highlight-search"; // NOI18N

    /** Find current word */
    public static final String findSelectionAction = "find-selection"; // NOI18N

    /** Undo action */
    public static final String undoAction = "undo"; // NOI18N

    /** Redo action */
    public static final String redoAction = "redo"; // NOI18N

    /** Word match next */
    public static final String wordMatchNextAction = "word-match-next"; // NOI18N

    /** Word match prev */
    public static final String wordMatchPrevAction = "word-match-prev"; // NOI18N

    /** Reindent Line action */
    public static final String reindentLineAction = "reindent-line"; // NOI18N

    /** Reformat Line action */
    public static final String reformatLineAction = "reformat-line"; // NOI18N

    /** Shift line right action */
    public static final String shiftLineRightAction = "shift-line-right"; // NOI18N

    /** Shift line left action */
    public static final String shiftLineLeftAction = "shift-line-left"; // NOI18N

    /** Action that scrolls the window so that caret is at the center of the window */
    public static final String adjustWindowCenterAction = "adjust-window-center"; // NOI18N

    /** Action that scrolls the window so that caret is at the top of the window */
    public static final String adjustWindowTopAction = "adjust-window-top"; // NOI18N

    /** Action that scrolls the window so that caret is at the bottom of the window */
    public static final String adjustWindowBottomAction = "adjust-window-bottom"; // NOI18N

    /** Action that moves the caret so that caret is at the center of the window */
    public static final String adjustCaretCenterAction = "adjust-caret-center"; // NOI18N

    /** Action that moves the caret so that caret is at the top of the window */
    public static final String adjustCaretTopAction = "adjust-caret-top"; // NOI18N

    /** Action that moves the caret so that caret is at the bottom of the window */
    public static final String adjustCaretBottomAction = "adjust-caret-bottom"; // NOI18N

    /** Format part of the document text using Indent */
    public static final String formatAction = "format"; // NOI18N

    /** Indent part of the document text using Indent */
    public static final String indentAction = "indent"; // NOI18N

    /** First non-white character on the line */
    public static final String firstNonWhiteAction = "first-non-white"; // NOI18N

    /** Last non-white character on the line */
    public static final String lastNonWhiteAction = "last-non-white"; // NOI18N

    /** First non-white character on the line */
    public static final String selectionFirstNonWhiteAction = "selection-first-non-white"; // NOI18N

    /** Last non-white character on the line */
    public static final String selectionLastNonWhiteAction = "selection-last-non-white"; // NOI18N

    /** Select the nearest identifier around caret */
    public static final String selectIdentifierAction = "select-identifier"; // NOI18N

    /** Select the next parameter (after the comma) in the given context */
    public static final String selectNextParameterAction = "select-next-parameter"; // NOI18N

    /** Go to the previous position stored in the jump-list */
    public static final String jumpListNextAction = "jump-list-next"; // NOI18N

    /** Go to the next position stored in the jump-list */
    public static final String jumpListPrevAction = "jump-list-prev"; // NOI18N

    /** Go to the last position in the previous component stored in the jump-list */
    public static final String jumpListNextComponentAction = "jump-list-next-component"; // NOI18N

    /** Go to the next position in the previous component stored in the jump-list */
    public static final String jumpListPrevComponentAction = "jump-list-prev-component"; // NOI18N

    /** Scroll window one line up */
    public static final String scrollUpAction = "scroll-up"; // NOI18N

    /** Scroll window one line down */
    public static final String scrollDownAction = "scroll-down"; // NOI18N

    /** Prefix of all macro-based actions */
    public static final String macroActionPrefix = "macro-"; // NOI18N

    /** Start recording of macro. Only one macro recording can be active at the time */
    public static final String startMacroRecordingAction = "start-macro-recording"; //NOI18N

    /** Stop the active recording */
    public static final String stopMacroRecordingAction = "stop-macro-recording"; //NOI18N

    /** Name of the action moving caret to the first column on the line */
    public static final String lineFirstColumnAction = "caret-line-first-column"; // NOI18N

    /** Insert the current Date and Time  */
    public static final String insertDateTimeAction = "insert-date-time"; // NOI18N

    /** Name of the action moving caret to the first
     * column on the line and extending the selection
     */
    public static final String selectionLineFirstColumnAction = "selection-line-first-column"; // NOI18N

    /** Name of the action for generating of Glyph Gutter popup menu*/
    public static final String generateGutterPopupAction = "generate-gutter-popup"; // NOI18N

    /** Toggle visibility of line numbers*/
    public static final String toggleLineNumbersAction = "toggle-line-numbers"; // NOI18N

    /** Paste and reformat code */
    public static final String pasteFormatedAction = "paste-formated"; // NOI18N

    /** Starts a new line in code */
    public static final String startNewLineAction = "start-new-line"; // NOI18N

    /** Cut text from caret position to line beginning action. */
    public static final String cutToLineBeginAction = "cut-to-line-begin"; // NOI18N

    /** Cut text from caret position to line end action. */
    public static final String cutToLineEndAction = "cut-to-line-end"; // NOI18N

    /** Remove all trailing spaces in the document. */
    public static final String removeTrailingSpacesAction = "remove-trailing-spaces"; //NOI18N

    public static final String DOC_REPLACE_SELECTION_PROPERTY = "doc-replace-selection-property"; //NOI18N

    private static final int KIT_CNT_PREALLOC = 7;

    static final long serialVersionUID = -8570495408376659348L;

    private static final Map<Class, BaseKit> kits = new HashMap<Class, BaseKit>(KIT_CNT_PREALLOC);

    private static final Object KEYMAPS_AND_ACTIONS_LOCK = new String("BaseKit.KEYMAPS_AND_ACTIONS_LOCK"); //NOI18N
    private static final Map<MimePath, KeybindingsAndPreferencesTracker> keymapTrackers = new WeakHashMap<MimePath, KeybindingsAndPreferencesTracker>(KIT_CNT_PREALLOC);
    private static final Map<MimePath, MultiKeymap> kitKeymaps = new WeakHashMap<MimePath, MultiKeymap>(KIT_CNT_PREALLOC);
    private static final Map<MimePath, Action[]> kitActions = new WeakHashMap<MimePath, Action[]>(KIT_CNT_PREALLOC);
    private static final Map<MimePath, Map<String, Action>> kitActionMaps = new WeakHashMap<MimePath, Map<String, Action>>(KIT_CNT_PREALLOC);

    private static CopyAction copyActionDef = new CopyAction();
    private static CutAction cutActionDef = new CutAction();
    private static PasteAction pasteActionDef = new PasteAction(false);
    private static DeleteCharAction deletePrevCharActionDef = new DeleteCharAction(deletePrevCharAction, false);
    private static DeleteCharAction deleteNextCharActionDef = new DeleteCharAction(deleteNextCharAction, true);
    private static ActionFactory.RemoveSelectionAction removeSelectionActionDef = new ActionFactory.RemoveSelectionAction();
    private static final Action insertTabActionDef = new InsertTabAction();
    private static final Action removeTabActionDef = new ActionFactory.RemoveTabAction();
    private static final Action insertBreakActionDef = new InsertBreakAction();

    private static ActionFactory.UndoAction undoActionDef = new ActionFactory.UndoAction();
    private static ActionFactory.RedoAction redoActionDef = new ActionFactory.RedoAction();

    public static final int MAGIC_POSITION_MAX = Integer.MAX_VALUE - 1;

    private final SearchableKit searchableKit;

    private boolean keyBindingsUpdaterInited;

    /**
     * Navigational boundaries for "home" and "end" actions. If defined on the target component,
     * home/end will move the caret first to the boundary, and only after that proceeds as usual (to the start/end of line).
     * The property must contain {@link PositionRegion} instance
     */
    private static final String PROP_NAVIGATE_BOUNDARIES = "NetBeansEditor.navigateBoundaries"; // NOI18N


    /**
     * Creates a new instance of <code>BaseKit</code>.
     *
     * <div class="nonnormative">
     * <p>You should not need to instantiate editor kits
     * directly under normal circumstances. There is a few ways how you can get
     * instance of <code>EditorKit</code> depending on what you already have
     * available:
     *
     * <ul>
     * <li><b>mime type</b> - Use <code>CloneableEditorSupport.getEditorKit(yourMimeType)</code>
     * to get the <code>EditorKit</code> registered for your mime type or use
     * the following code <code>MimeLookup.getLookup(MimePath.parse(yourMimeType)).lookup(EditorKit.class)</code>
     * and check for <code>null</code>.
     * <li><b>JTextComponent</b> - Simply call
     * <code>JTextComponent.getUI().getEditorKit(JTextComponent)</code> passing
     * in the same component.
     * </ul>
     * </div>
     */
    public BaseKit() {
        // possibly register
        synchronized (kits) {
            if (kits.get(this.getClass()) == null) {
                kits.put(this.getClass(), this); // register itself
            }
        }
        // Directly implementing searchable editor kit would require module dependency changes
        // of any modules using BaseKit reference so make a wrapper instead
        org.netbeans.modules.editor.lib2.actions.EditorActionUtilities.registerSearchableKit(this,
                searchableKit = new SearchableKit(this));
    }
}
